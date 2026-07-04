#!/usr/bin/env python3
# QR Shield plugin discovery and loader
import importlib
import os

from . import utils

MODULE_ROOT = os.path.join("core", "modules")


def discover_modules():
    """Discover available module plugins under core/modules."""
    modules = []
    for path, _, files in os.walk(MODULE_ROOT):
        for name in files:
            if not name.endswith(".py") or name.startswith("__"):
                continue
            module_path = os.path.join(path, name).replace("\\", "/")
            modules.append(module_path)

    modules = [x[:-3] for x in modules if x.endswith(".py")]
    prefix = "core/modules/"
    modules = [x[len(prefix) :] if x.startswith(prefix) else x for x in modules]
    return modules


def module_import_path(module_name):
    return utils.pythonize("core.modules." + module_name)


def load_module(module_name, development=False):
    module_name = str(module_name).strip()
    if not module_name:
        raise ValueError("Module name is required")
    import_path = module_import_path(module_name)
    module = importlib.import_module(import_path)
    if development:
        module = utils.reload(module)
    return module


def get_module_info(module_name, development=False):
    module = load_module(module_name, development=development)
    return getattr(module, "info")
