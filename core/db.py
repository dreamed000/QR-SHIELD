"""Compatibility shim delegating to `core.registry.modules`.

Existing imports like `from core import db` or `import core.db` will continue
to work. The implementation has been moved to `core.registry.modules` to
support a clearer registry architecture.
"""

from .registry.modules import grab, index_modules

__all__ = ["index_modules", "grab"]
