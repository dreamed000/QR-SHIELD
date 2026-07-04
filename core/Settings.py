"""Compatibility shim for the new configuration package.

This module keeps the historical `core.Settings` import working while the
implementation has moved to `core.config`.
"""

from .config.loader import load_settings

# Instantiate the application-wide settings object. Existing code imports
# `Settings` from `core.Settings` (via `from core import Settings`). By
# keeping the same variable name here we preserve backward compatibility.
Settings = load_settings()
