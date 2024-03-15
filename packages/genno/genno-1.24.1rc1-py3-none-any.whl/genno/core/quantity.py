import operator
from functools import update_wrapper
from numbers import Number
from typing import Any, Hashable, Optional

import pandas as pd
import pint

from genno.compat.xarray import DataArrayLike

#: Name of the class used to implement :class:`.Quantity`.
CLASS = "AttrSeries"
# CLASS = "SparseDataArray"


class Quantity(DataArrayLike["Quantity"]):
    """A sparse data structure that behaves like :class:`xarray.DataArray`.

    Depending on the value of :data:`.CLASS`, Quantity is either :class:`.AttrSeries` or
    :class:`.SparseDataArray`.
    """

    _name: Optional[Hashable]

    def __new__(cls, *args, **kwargs):
        # Use _get_class() to retrieve either AttrSeries or SparseDataArray
        return object.__new__(Quantity._get_class(cls))

    @classmethod
    def from_series(cls, series, sparse=True):
        """Convert `series` to the Quantity class given by :data:`.CLASS`."""
        # NB signature is the same as xr.DataArray.from_series(); except sparse=True
        assert sparse
        return cls._get_class().from_series(series, sparse)

    @property
    def name(self) -> Optional[Hashable]:
        """The name of this quantity."""
        return self._name  # pragma: no cover

    @name.setter
    def name(self, value: Optional[Hashable]) -> None:
        self._name = value  # pragma: no cover

    @property
    # def units(self) -> pint.Unit:  # NB can't do this currently; see python/mypy#3004
    def units(self):
        """Retrieve or set the units of the Quantity.

        Examples
        --------
        Create a quantity without units:

        >>> qty = Quantity(...)

        Set using a string; automatically converted to pint.Unit:

        >>> qty.units = "kg"
        >>> qty.units
        <Unit('kilogram')>

        """
        return self.attrs.setdefault(
            "_unit", pint.get_application_registry().dimensionless
        )

    @units.setter
    def units(
        self,
        value,
        # value: Union[pint.Unit, str], # NB ditto re: python/mypy#3004
    ):
        self.attrs["_unit"] = pint.get_application_registry().Unit(value)

    # Internal methods

    @staticmethod
    def _get_class(cls=None):
        """Get :class:`.AttrSeries` or :class:`.SparseDataArray`, per :data:`.CLASS`."""
        if cls in (Quantity, None):
            if CLASS == "AttrSeries":
                from .attrseries import AttrSeries as cls
            elif CLASS == "SparseDataArray":
                from .sparsedataarray import SparseDataArray as cls
            else:  # pragma: no cover
                raise ValueError(CLASS)

        return cls

    @staticmethod
    def _single_column_df(data, name):
        """Handle `data` and `name` arguments to Quantity constructors."""
        if isinstance(data, pd.DataFrame):
            if len(data.columns) != 1:
                raise TypeError(
                    f"Cannot instantiate Quantity from {len(data.columns)}-D data frame"
                )

            # Unpack a single column; use its name if not overridden by `name`
            return data.iloc[:, 0], (name or data.columns[0])
        else:
            return data, name

    @staticmethod
    def _collect_attrs(data, attrs_arg, kwargs):
        """Handle `attrs` and 'units' `kwargs` to Quantity constructors."""
        # Use attrs, if any, from an existing object, if any
        new_attrs = getattr(data, "attrs", dict()).copy()

        # Overwrite with values from an explicit attrs argument
        new_attrs.update(attrs_arg or dict())

        # Store the "units" keyword argument as an attr
        units = kwargs.pop("units", None)
        if units is not None:
            new_attrs["_unit"] = pint.Unit(units)

        return new_attrs

    def _binop_units(self, name: str, other) -> pint.Unit:
        """Determine result units for a binary operation between `self` and `other`."""
        if name == "pow":
            # Currently handled by operator.pow()
            return self.units

        # Retrieve units of `other`
        other_units = other.units

        # Ensure there is not a mix of pint.Unit and pint.registry.Unit; this throws
        # off pint's internal logic
        if other_units.__class__ is not self.units.__class__:
            other_units = self.units.__class__(other_units)

        # Allow pint to determine the output units
        return getattr(operator, name)(self.units, other_units)


def assert_quantity(*args):
    """Assert that each of `args` is a Quantity object.

    Raises
    ------
    TypeError
        with a indicative message.
    """
    for i, arg in enumerate(args):
        if not isinstance(arg, Quantity):
            raise TypeError(
                f"arg #{i+1} ({repr(arg)}) is not Quantity; likely an incorrect key"
            )


def maybe_densify(func):
    """Wrapper for operations that densifies :class:`.SparseDataArray` input."""

    def wrapped(*args, **kwargs):
        if CLASS == "SparseDataArray":

            def densify(arg):
                return arg._sda.dense if isinstance(arg, Quantity) else arg

            def sparsify(result):
                return result._sda.convert()

        else:

            def densify(arg):
                return arg

            sparsify = densify

        return sparsify(func(*map(densify, args), **kwargs))

    update_wrapper(wrapped, func)

    return wrapped


def possible_scalar(value) -> Quantity:
    """Convert `value`, possibly a scalar, to :class:`Quantity`."""
    return Quantity(value) if isinstance(value, Number) else value


def unwrap_scalar(qty: Quantity) -> Any:
    """Unwrap `qty` to a scalar, if it is one."""
    return qty if len(qty.dims) else qty.item()
