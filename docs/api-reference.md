# API Reference

This page documents the current internal interfaces that are most relevant when extending or debugging QR-SHIELD.

## Entry points

### qrshield.main

The console entry point is defined in [qrshield.py](../qrshield.py):

```python
from core.app import main

if __name__ == "__main__":
    main()
```

### QRShieldApp

Defined in [core/app.py](../core/app.py), this class:

- parses the supported CLI arguments

- initializes runtime settings

- dispatches the session to the CLI

### QRShieldCLI

Defined in [core/Cli.py](../core/Cli.py), this class implements the interactive shell and the built-in commands:

- help, list, show, info, use, options, set, run, back

- sessions, jobs, history, makerc, resource, database

- debug, dev, verbose, reload, refresh

## Module loading

### discover_modules

Implemented in [core/plugin_manager.py](../core/plugin_manager.py), this function walks the modules tree and returns discoverable module paths.

### load_module

Loads a module by its dotted import path and optionally reloads it in development mode.

## Module execution context

### ModuleContext

Defined in [core/module.py](../core/module.py), this context:

- loads the currently selected module

- exposes module options through the CLI

- runs the module with the appropriate browser backend

## Module contract

Each module is expected to provide:

```python
class info:
    author = "..."
    short_description = "..."
    full_description = None

class execution:
    module_type = types.grabber  # or types.post
    name = "platform"
    url = "https://example.com"
```

Grabber modules also define QR selectors and success identifiers; post modules resolve a session ID and load it into a visible browser.

## Browser helpers

### headless_browsers

Implemented in [core/browser.py](../core/browser.py), this class manages Firefox sessions used by grabber modules.

### visible_browsers

Also implemented in [core/browser.py](../core/browser.py), this class restores visible browser windows for post modules.

## Shared utilities

### types

The module type definitions live in [core/module_utils.py](../core/module_utils.py):

- types.grabber

- types.post

### session helpers

The same module also provides helpers for:

- resolving a post-session ID

- loading localStorage, cookies, or profile-based sessions

- rendering the HTML templates used by the grabber flow

## Configuration objects

### AppConfig

Defined in [core/config/models.py](../core/config/models.py), this dataclass stores runtime state such as:

- current working path

- debug, development, and verbose flags

- the active module name

- browser instances

- history and previous-module tracking

### load_settings

Defined in [core/config/loader.py](../core/config/loader.py), this returns the default AppConfig instance.

---

Last Updated: July 2026
