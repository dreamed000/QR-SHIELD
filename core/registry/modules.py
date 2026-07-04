"""Module registry helpers (replacement for `core.db`)."""

from typing import Any, List

from ..plugin_manager import discover_modules, load_module


def index_modules() -> List[str]:
    """Return a list of discovered module import paths."""
    return discover_modules()


def grab(module_name: str) -> Any:
    """Load a module and return its `info` attribute.

    Raises ImportError or AttributeError if the module does not expose `info`.
    """
    module = load_module(module_name)
    return getattr(module, "info")
