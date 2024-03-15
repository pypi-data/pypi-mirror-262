import logging
from copy import copy
from functools import partial
from pathlib import Path
from typing import (
    Any,
    Callable,
    Dict,
    Iterable,
    List,
    MutableMapping,
    Optional,
    Tuple,
    Type,
    Union,
)

import pint
import yaml

from genno import operator
from genno.core.computer import Computer
from genno.core.exceptions import KeyExistsError, MissingKeyError
from genno.core.key import Key, iter_keys
from genno.util import REPLACE_UNITS

log = logging.getLogger(__name__)

#: Registry of configuration section handlers.
HANDLERS: Dict[str, Any] = {}

#: Configuration sections/keys to be stored with no action.
STORE = set(["cache_path", "cache_skip"])


def configure(path: Optional[Union[Path, str]] = None, **config):
    """Configure :mod:`.genno` globally.

    Modifies global variables that affect the behaviour of *all* Computers and
    operators. Configuration keys loaded from file are superseded by keyword arguments.
    Messages are logged at level :obj:`logging.INFO` if `config` contains unhandled
    sections.

    Parameters
    ----------
    path : pathlib.Path, optional
        Path to a configuration file in JSON or YAML format.
    **config :
        Configuration keys/sections and values.
    """
    if path:
        config["path"] = Path(path)
    # The value of fail= doesn't matter, since no Computer is given
    parse_config(None, data=config, fail="raise")


def handles(section_name: str, iterate: bool = True, discard: bool = True):
    """Decorator to register a configuration section handler in :data:`HANDLERS`.

    Parameters
    ----------
    section_name: str
        The name of the configuration section to handle. Using a name already present
        in :data:`HANDLERS` overrides that handler.
    iterate : bool, optional
        If :obj:`True`, the handler is called once for each item (either list item, or
        (key, value) tuple) in the section. If :obj:`False`, the entire section
        contents, of whatever type, are passed to tha handler.
    discard : bool, optional
        If :obj:`True`, configuration section data is discarded after the handler is
        called. If :obj:`False`, the data is retained and stored on the Computer.
    """

    def wrapper(f: Callable):
        if section_name in HANDLERS:
            log.debug(
                f"Override handler {repr(HANDLERS[section_name])} for "
                f" '{section_name}:'"
            )
        HANDLERS[section_name] = f
        setattr(f, "_iterate", iterate)
        setattr(f, "_discard", discard)
        return f

    return wrapper


def parse_config(  # noqa: C901  FIXME reduce complexity from 14 → ≤10
    c: Optional[Computer],
    data: MutableMapping[str, Any],
    fail: Optional[Union[str, int]] = None,
):
    # Assemble a queue of (args, kwargs) for Computer.add_queue()
    queue: List[Tuple[Tuple, Dict]] = []

    try:
        path = data.pop("path")
    except KeyError:
        pass
    else:
        # Load configuration from file
        path = Path(path)
        with open(path, "r") as f:
            new_data = yaml.safe_load(f)

        # Overwrite the file content with direct configuration values
        new_data.update(data)
        data = new_data

        # Also store the directory where the configuration file was located
        if c is None:
            data["config_dir"] = path.parent
        else:
            # Early add to the graph
            c.graph["config"]["config_dir"] = path.parent

    # Sections to discard, e.g. with handler._store = False
    discard = set()

    for section_name, section_data in data.items():
        handler = HANDLERS.get(section_name)
        if not handler:
            if section_name not in STORE:
                log.info(
                    f"No handler for configuration section '{section_name}:'; ignored"
                )
            continue

        if handler._discard:
            discard.add(section_name)

        if handler._iterate:
            if isinstance(section_data, dict):
                iterator: Iterable = section_data.items()
            elif isinstance(section_data, list):
                iterator = section_data
            else:  # pragma: no cover
                raise NotImplementedError(handler.expected_type)
            queue.extend((("apply", handler), dict(info=item)) for item in iterator)
        else:
            handler(c, section_data)

    for section_name in discard:
        data.pop(section_name)

    if c:
        # Process the entries
        c.add_queue(queue, max_tries=2, fail=fail)

        # Store configuration in the graph itself
        c.graph["config"].update(data)
    elif len(queue):
        raise RuntimeError("Cannot apply non-global configuration without a Computer")


@handles("aggregate")
def aggregate(c: Computer, info):
    """Handle one entry from the ``aggregate:`` config section."""
    # Copy for destructive .pop()
    info = copy(info)

    # Unpack `info`
    quantities = c.infer_keys(info.pop("_quantities"))
    tag = info.pop("_tag")
    # Keyword arguments for add()
    kw = dict(
        fail=info.pop("_fail", None),
        groups={info.pop("_dim"): info},
        strict=True,
        sums=True,
    )

    def _log_or_raise(exc: Exception, default_level: str, message: str):
        """Either raise `exc` if ``kw["fail"]`` > `default_level`, or log `message`."""
        fail_level = getattr(logging, (kw["fail"] or default_level).upper())
        if fail_level >= logging.ERROR:
            raise exc
        else:
            log.log(fail_level, message)

    try:
        quantities = c.check_keys(*quantities)
    except MissingKeyError as e:
        # Default to fail="error" here: stricter
        _log_or_raise(e, "error", f"No key(s) {e.args!r} to aggregate")

    # Iterate over quantities to be aggregated
    for qty in map(Key, quantities):
        try:
            result = c.add(qty.add_tag(tag), "aggregate", qty, **kw)
        except KeyExistsError:
            pass
        except MissingKeyError as e:
            # Default to fail="warning": more permissive
            _log_or_raise(e, "warning", repr(e))
        else:
            if keys := list(iter_keys(result)):
                log.info(f"Add {repr(keys[0])} + {len(keys)-1} partial sums")


@handles("alias")
def alias(c: Computer, info):
    """Handle one entry from the ``alias:`` config section."""
    c.add(info[0], info[1])


@handles("combine")
def combine(c: Computer, info):
    """Handle one entry from the ``combine:`` config section."""
    # Split inputs into three lists
    quantities, select, weights = [], [], []

    # Key for the new quantity
    key = Key(info["key"])

    # Loop over inputs to the combination
    for i in info["inputs"]:
        # Required dimensions for this input: output key's dims, plus any
        # dims that must be selected on
        selector = i.get("select", {})
        dims = set(key.dims) | set(selector.keys())
        quantities.append(c.infer_keys(i["quantity"], dims))

        select.append(selector)
        weights.append(i.get("weight", 1))

    # Check for malformed input
    assert len(quantities) == len(select) == len(weights)

    # Computation
    task = tuple(
        [partial(operator.combine, select=select, weights=weights)] + quantities
    )

    added = iter_keys(c.add(key, task, strict=True, sums=True))

    log.info(f"Add {repr(key)} + {len(list(added))-1} partial sums")
    log.debug("    as combination of")
    log.debug(f"    {repr(quantities)}")


@handles("default", iterate=False)
def default(c: Computer, info):
    """Handle the ``default:`` config section."""
    c.default_key = info


@handles("files")
def files(c: Computer, info):
    """Handle one entry from the ``files:`` config section."""
    # Files with exogenous data
    path = Path(info["path"])
    if not path.is_absolute():
        # Resolve relative paths relative to the directory containing the configuration
        # file
        path = c.graph["config"].get("config_dir", Path.cwd()) / path

    info["path"] = path

    c.add("load_file", **info)


@handles("general")
def general(c: Computer, info):
    """Handle one entry from the ``general:`` config section."""
    # Inputs
    # TODO allow to specify a more narrow key and *not* have infer_keys applied; perhaps
    #      using "*"
    inputs = c.infer_keys(info.get("inputs", []))

    if info["comp"] in ("mul", "product"):
        result = c.add(info["key"], "mul", *inputs)
        log.info(f"Add {repr(result)} using .add_product()")
    else:
        # The resulting key
        key = info["key"]
        key = key if Key.bare_name(key) else Key(key)

        # Infer the dimensions of the resulting key if ":*:" is given for the dims
        if isinstance(key, Key) and key.dims == ("*",):
            key = Key.product(key.name, *inputs, tag=key.tag)
            # log.debug(f"Inferred dimensions ({', '.join(key.dims)}) for '*'")

        # If info["comp"] is None, the task is a list that collects other keys
        _seq: Type = list
        task = []

        if info["comp"] is not None:
            _seq = tuple  # Task is a computation
            # Retrieve the function for the computation
            f = c.get_operator(info["comp"])
            if f is None:
                raise ValueError(info["comp"])
            task = [partial(f, **info.get("args", {}))]

            log.info(f"Add {repr(key)} using {f.__module__}.{f.__name__}(…)")

        task.extend(inputs)

        added = c.add(key, _seq(task), strict=True, sums=info.get("sums", False))

        if isinstance(added, tuple):
            log.info(f"    + {len(added)-1} partial sums")


@handles("report")
def report(c: Computer, info):
    """Handle one entry from the ``report:`` config section."""
    log.info(f"Add report {info['key']} with {len(info['members'])} table(s)")

    # Concatenate pyam data structures
    c.add(info["key"], tuple([c.get_operator("concat")] + info["members"]), strict=True)


@handles("units", iterate=False)
def units(c: Computer, info):
    """Handle the ``units:`` config section."""

    # Define units
    registry = pint.get_application_registry()
    try:
        defs = info["define"].strip()
        registry.define(defs)
    except KeyError:
        pass
    except (TypeError, pint.DefinitionSyntaxError, pint.RedefinitionError) as e:
        log.warning(e)
    else:
        log.info(f"Apply global unit definitions {defs}")

    # Add replacements
    for old, new in info.get("replace", {}).items():
        log.info(f"Replace unit {repr(old)} with {repr(new)}")
        REPLACE_UNITS[old] = new
