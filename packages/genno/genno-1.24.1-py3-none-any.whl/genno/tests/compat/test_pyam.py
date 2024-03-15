import logging
import re
from collections import namedtuple
from functools import partial

import pandas as pd
import pytest
from pandas.testing import assert_frame_equal, assert_series_equal

from genno import Computer, Key, Quantity
from genno.compat.pyam import operator, util
from genno.operator import add, load_file

# Skip this entire file if pyam is not installed
pyam = pytest.importorskip("pyam", reason="pyam-iamc not installed")

# Warning emitted by pandas ≥ 2.1.0 with pyam 1.9.0
pytestmark = pytest.mark.filterwarnings(
    "ignore:.*unique with argument that is not.*:FutureWarning:pyam.core"
)


@pytest.fixture(scope="session")
def scenario():
    """Mock object which resembles ixmp.Scenario."""
    Scenario = namedtuple("Scenario", ["model", "scenario"])
    yield Scenario(model="Canning problem (MESSAGE scheme)", scenario="standard")


# Session scope so that ureg.define() is only called once
@pytest.fixture(scope="session")
def dantzig_computer(test_data_path, scenario, ureg):
    """Computer with minimal contents for below tests."""
    c = Computer()

    # Load files and add to graph
    for name, units in (("ACT", ""), ("var_cost", "USD/case"), ("vom", "USD")):
        # NB need to load the file here in order to identify the dims of each quantity
        qty = load_file(test_data_path / f"dantzig-{name}.csv", name=name, units=units)
        c.add(Key(name, qty.dims), qty, sums=True)

    # Reduced version of the "total operation & maintenance" calculation in MESSAGEix;
    # for test_concat()
    vom = c.full_key("vom")
    fom = Key("fom", dims=vom.dims)
    c.add(fom, c.get(vom)[0:0], sums=True)
    c.add(Key("tom", dims=vom.dims), add, fom, vom, sums=True)

    # Mock scenario object
    c.add("scenario", scenario)

    yield c


def test_require_compat():
    # New object does not understand "as_pyam" as the name of a computation
    c = Computer()
    assert c.get_operator("as_pyam") is None

    # require_compat() loads it
    c.require_compat("pyam")
    assert c.get_operator("as_pyam") is not None


def test_config(test_data_path):
    """iamc: section in configuration files is parsed correctly."""
    """Test handling configuration file syntax using test data files."""
    c = Computer()

    c.add(Key("X", list("abcdefy")), None, sums=True)
    c.add("message:default", tuple())

    c.configure(path=test_data_path / "config-pyam.yaml")


def test_as_pyam(dantzig_computer, scenario):
    c = dantzig_computer

    # Quantities for 'ACT' variable at full resolution
    qty = c.get(c.full_key("ACT"))

    # Call as_pyam() with an empty quantity
    p = operator.as_pyam(scenario, qty[0:0], rename=dict(nl="region", ya="year"))
    assert isinstance(p, pyam.IamDataFrame)

    input = Quantity(
        pd.DataFrame(
            [["f1", "b1", 2021, 42], ["f1", "b1", 2021, 42]],
            columns=["foo", "bar", "year", "value"],
        ).set_index(["foo", "bar", "year"])
    )

    with pytest.raises(ValueError, match="Duplicate IAMC indices cannot be converted"):
        operator.as_pyam(scenario, input)


def test_computer_as_pyam(caplog, tmp_path, test_data_path, dantzig_computer):
    caplog.set_level(logging.INFO)
    c = dantzig_computer

    # Key for 'ACT' variable at full resolution
    ACT = c.full_key("ACT")

    # Add a computation that converts ACT to a pyam.IamDataFrame
    # NB drop={} is provided to mimic the test in message_ix and allow the log assertion
    #    below to work
    rename = dict(nl="region", ya="year")
    c.add(
        "ACT IAMC",
        (partial(operator.as_pyam, rename=rename, drop=["yv"]), "scenario", ACT),
    )

    # Result is an IamDataFrame
    idf1 = c.get("ACT IAMC")
    assert isinstance(idf1, pyam.IamDataFrame)

    # …of expected length
    assert len(idf1) == 8

    # …in which variables are not renamed
    assert idf1["variable"].unique() == "ACT"

    # Warning was logged because of extra columns
    assert (
        "genno.compat.pyam.util",
        logging.INFO,
        "Extra columns ['h', 'm', 't'] when converting to IAMC format",
    ) in caplog.record_tuples

    # Repeat, using the convert_pyam() convenience function
    def add_tm(df, name="Activity"):
        """Callback for collapsing ACT columns."""
        df["variable"] = f"{name}|" + df["t"] + "|" + df["m"]
        return df.drop(["t", "m"], axis=1)

    # Use the convenience function to add the node
    with pytest.warns(DeprecationWarning):
        key2 = c.convert_pyam(ACT, rename=rename, collapse=add_tm)

    key2 = c.add(ACT, "as_pyam", rename=rename, collapse=add_tm)

    # Keys of added node(s) are returned
    assert ACT.name + "::iamc" == key2

    caplog.clear()

    # Result
    idf2 = c.get(key2)
    df2 = idf2.as_pandas()

    # Extra columns have been removed:
    # - m and t by the collapse callback.
    # - h automatically, because 'ya' was used for the year index.
    assert not any(c in df2.columns for c in ["h", "m", "t"])

    # Variable names were formatted by the callback
    reg_var = pd.DataFrame(
        [
            ["san-diego", "Activity|canning_plant|production"],
            ["san-diego", "Activity|transport_from_san-diego|to_chicago"],
            ["san-diego", "Activity|transport_from_san-diego|to_new-york"],
            ["san-diego", "Activity|transport_from_san-diego|to_topeka"],
            ["seattle", "Activity|canning_plant|production"],
            ["seattle", "Activity|transport_from_seattle|to_chicago"],
            ["seattle", "Activity|transport_from_seattle|to_new-york"],
            ["seattle", "Activity|transport_from_seattle|to_topeka"],
        ],
        columns=["region", "variable"],
    )
    assert_frame_equal(df2[["region", "variable"]], reg_var)

    # pyam.operator.write_report() is used, calling pyam.IamDataFrame.to_csv()
    path = tmp_path / "activity.csv"
    c.write(key2, path)

    # File contents are as expected
    assert test_data_path.joinpath("pyam-write.csv").read_text() == path.read_text()

    # File can be written as .xlsx
    c.write(key2, tmp_path / "activity.xlsx")

    # Other file extensions raise exceptions
    with pytest.raises(ValueError, match=".csv or .xlsx, not .foo"):
        c.write(key2, tmp_path / "activity.foo")

    # Giving keyword arguments raises exception
    with pytest.raises(NotImplementedError):
        c.write(key2, tmp_path / "activity.csv", index=False)

    # Non-pyam objects are written using base write_file()
    c.write(ACT, tmp_path / "ACT.csv")

    # Use a name map to replace variable names
    replacements = {re.escape("Activity|canning_plant|production"): "Foo"}
    kw = dict(rename=rename, replace=dict(variable=replacements), collapse=add_tm)
    with pytest.warns(DeprecationWarning):
        key3 = c.convert_pyam(ACT, **kw)
    key3 = c.add(ACT, "as_pyam", **kw)
    df3 = c.get(key3).as_pandas()

    # Values are the same; different names
    exp = df2[df2.variable == "Activity|canning_plant|production"][
        "value"
    ].reset_index()
    assert all(exp == df3[df3.variable == "Foo"]["value"].reset_index())

    # Now convert variable cost
    cb = partial(add_tm, name="Variable cost")
    kw = dict(rename=rename, collapse=cb)
    with pytest.warns(DeprecationWarning):
        key4 = c.convert_pyam("var_cost", **kw)
    key4 = c.add("var_cost", "as_pyam", **kw)
    df4 = c.get(key4).as_pandas().drop(["model", "scenario"], axis=1)

    # Results have the expected units
    assert all(df4["unit"] == "USD / case")

    # Also change units
    kw = dict(rename=rename, collapse=cb, unit="centiUSD / case")
    with pytest.warns(DeprecationWarning):
        key5 = c.convert_pyam("var_cost", **kw)
    key5 = c.add("var_cost", "as_pyam", **kw)

    df5 = c.get(key5).as_pandas().drop(["model", "scenario"], axis=1)

    # Results have the expected units
    assert all(df5["unit"] == "centiUSD / case")
    assert_series_equal(df4["value"], df5["value"] / 100.0)

    # Convert multiple quantities at once
    keys = c.add("as_pyam", ["var_cost", "var_cost"], **kw)
    assert ("var_cost::iamc", "var_cost::iamc") == keys


def test_deprecated_convert_pyam():
    """Test deprecated usage of `replace` parameter to as_pyam."""
    c = Computer()

    c.add("foo", None)

    with pytest.warns(
        DeprecationWarning,
        match=re.escape(
            "replace must be nested dict(), e.g. {'variable': {'bar': 'baz'}}"
        ),
    ):
        c.convert_pyam("foo", replace=dict(bar="baz"))


def test_concat(dantzig_computer):
    """pyam.operator.concat() passes through to base concat()."""
    c = dantzig_computer

    # Uses pyam.concat() for suitable types
    input = pd.DataFrame([["foo"] * len(pyam.IAMC_IDX)], columns=pyam.IAMC_IDX).assign(
        year=2021, value=42.0, unit="kg"
    )

    with pytest.warns(DeprecationWarning):
        result = operator.concat(
            pyam.IamDataFrame(input), pyam.IamDataFrame(input.assign(year=2022))
        )
    assert isinstance(result, pyam.IamDataFrame)

    # Other types pass through to base concat()
    with pytest.warns(DeprecationWarning):
        key = c.add(
            "test", operator.concat, "fom:nl-t-ya", "vom:nl-t-ya", "tom:nl-t-ya"
        )

    c.get(key)


def test_clean_units():
    input = pd.DataFrame([["kg"], ["km"]], columns=["unit"])
    with pytest.raises(
        ValueError, match=re.escape("cannot convert non-unique units ['kg', 'km']")
    ):
        util.clean_units(input, unit="tonne")


def test_collapse():
    data = []
    columns = ["value"] + list("abcdef")
    for row in range(10):
        data.append([row])
        for col in columns[1:]:
            data[-1].append(f"{col}{row}")
    input = pd.DataFrame(data, columns=columns)

    # No arguments = pass through
    assert_frame_equal(input, util.collapse(input))

    with pytest.raises(ValueError, match="non-IAMC column 'foo'"):
        util.collapse(input, columns=dict(foo=["a", "b"]))

    # Collapse multiple columns
    columns = dict(variable=["f", "a", "d"])
    df1 = util.collapse(input, columns=columns)
    assert df1.loc[0, "variable"] == "f0|a0|d0"

    # Two targets
    columns["region"] = ["e", "b"]
    df2 = util.collapse(input, columns=columns)
    assert df2.loc[9, "region"] == "e9|b9"

    # String entries
    columns["scenario"] = ["foo", "c", "bar"]
    df3 = util.collapse(input, columns=columns)
    assert df3.loc[0, "scenario"] == "foo|c0|bar"
    assert df3.loc[9, "scenario"] == "foo|c9|bar"


def test_drop():
    with pytest.raises(ValueError, match="foo"):
        util.drop(pd.DataFrame, "foo")
