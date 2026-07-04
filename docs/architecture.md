# Architecture Guide

This document summarizes the architecture of the current QR-SHIELD codebase.

## High-level structure

```text
qrshield.py
  └─ core/app.py
       └─ QRShieldApp
            ├─ parses CLI flags
            ├─ initializes settings
            └─ dispatches to the CLI layer

core/Cli.py
  └─ QRShieldCLI
       ├─ interactive command loop
       ├─ built-in commands (help, list, use, run, sessions, jobs)
       └─ module context control

core/module.py
  └─ ModuleContext
       ├─ loads the selected module
       ├─ exposes module options
       └─ runs the selected module

core/plugin_manager.py
  └─ module discovery and import helpers

core/modules/
  ├─ grabber/
  └─ post/

core/browser.py
  └─ Selenium-based Firefox automation for grabbers and post sessions

core/module_utils.py
  └─ shared helpers for session resolution, storage, templates, and screenshots
```

## Main components

### Bootstrap and entry point

- [qrshield.py](../qrshield.py) imports the main application entry point.

- [core/app.py](../core/app.py) parses the supported CLI flags and starts the app.

### CLI layer

- [core/Cli.py](../core/Cli.py) provides the interactive shell and command handlers.

- [core/module.py](../core/module.py) handles module-specific commands such as options, set, run, and back.

### Module system

- [core/plugin_manager.py](../core/plugin_manager.py) discovers Python modules under [core/modules](../core/modules).

- [core/registry/modules.py](../core/registry/modules.py) provides the compatibility registry helpers used by the rest of the app.

- Each module exposes an info class and an execution class.

### Browser automation

- [core/browser.py](../core/browser.py) manages Firefox launch, session monitoring, and browser lifecycle.

- Grabber modules use headless browsers to open login pages and wait for QR-based authentication.

- Post modules use visible browsers to reopen stored sessions.

### Session persistence

- Sessions are stored under the sessions directory.

- The current implementation uses a sessions.json index plus platform-specific session folders.

- Post modules resolve a session ID using the shared helpers in [core/module_utils.py](../core/module_utils.py).

## Configuration model

The current configuration path is intentionally simple:

- [core/config/models.py](../core/config/models.py) defines the AppConfig dataclass.

- [core/config/loader.py](../core/config/loader.py) returns the default configuration.

- There is no persistent configuration file implementation in the current repository.

Runtime state is therefore influenced by:

- CLI flags passed at startup

- environment variables for Firefox and geckodriver discovery

- module options set at runtime via the CLI

## Execution flow

1. The app starts and initializes the main settings object.

1. The CLI discovers available modules from the modules tree.

1. The user selects a module with use.

1. The module context loads the module and exposes its options.

1. The user runs the module, which launches Firefox and either:

   - captures a new QR-based session, or

   - restores a previously captured session

## Notes

The architecture is intentionally lightweight and extension-oriented. New platforms can be added by creating a new module under the grabber or post tree and exposing the expected info and execution classes.

---

Last Updated: July 2026
