# Architecture

## System Architecture

QR-SHIELD implements a modular, extensible architecture for QR code security research and session capture. This document describes the runtime architecture, core components, extension points, and system boundaries.

## High-Level Architecture

QR-SHIELD is organized as a layered application with a CLI front end, plugin-based module execution, and core automation services.

```text
QR-SHIELD Application
├─ CLI Framework (Interactive Shell)
│  ├─ Command dispatch
│  ├─ Module context
│  └─ Session management
├─ Plugin Module System
│  ├─ Grabber Modules (Session Acquisition)
│  │  ├─ Discord
│  │  ├─ WhatsApp
│  │  ├─ Signal
│  │  └─ Telegram
│  └─ Post Modules (Session Interaction)
│     ├─ Discord
│     ├─ WhatsApp
│     ├─ Signal
│     └─ Telegram
├─ Core Services
│  ├─ Browser Automation (Selenium 4)
│  ├─ HTTP Server (Jinja2 Templates)
│  ├─ Session Manager
│  └─ Configuration System
└─ External Systems
   ├─ Firefox Browser
   ├─ Target platforms (Discord, WhatsApp, etc.)
   └─ Filesystem (sessions, profiles, logs)
```

## Core Components

### 1. CLI Framework

**Files:** `core/app.py`, `core/Cli.py`, `core/module.py`

**Responsibility:** Command-line interface and command dispatch

**Key Features:**

- Interactive shell with history

- Command parsing and execution

- Module context management

- Resource file execution

- Debug/development modes

**Architecture:**

```text
QRShieldApp (app.py)
  ↓
  Parse arguments
  ↓
  Initialize Settings
  ↓
  ModuleContext (module.py)
    ↓
    Load module
    ↓
    Execute command
    ↓
  QRShieldCLI (Cli.py)
    ↓
    Handle CLI keywords
    ↓
    Manage state
```

**Key Classes:**

- `QRShieldApp` - Application orchestrator

- `ModuleContext` - Module execution context

- `QRShieldCLI` - Command handler and shell interface

### 2. Plugin Module System

**Files:** `core/plugin_manager.py`, `core/registry/modules.py`

**Responsibility:** Dynamic module discovery and loading

**Key Features:**

- Automatic module discovery

- Lazy module loading

- Development mode with reload

- Module type system

**Module Structure:**

```python
# Module Template
class info:
    author = "Author Name"
    short_description = "Brief description"
    full_description = "Detailed description"

class execution:
    module_type = types.grabber  # or types.post
    name = "module_name"

    # Platform-specific selectors
    image_xpath = '//xpath/to/qr'
    change_identifier = '//xpath/to/login/success'

    @staticmethod
    def run(global_options, visible_browser):
        # Module implementation
        pass
```

**Module Types:**

- `grabber` - Captures sessions from QR login

- `post` - Interacts with captured sessions

### 3. Browser Automation Layer

**File:** `core/browser.py`

**Responsibility:** Selenium 4 integration and Firefox automation

**Key Features:**

- Firefox binary resolution

- User agent rotation

- WebDriver creation

- Page interaction

- QR code extraction

**Key Functions:**

- `resolve_firefox_binary()` - Find Firefox executable

- `create_driver()` - Create WebDriver instance

- `extract_qr_image()` - Get QR code from page

- `wait_for_element()` - Wait for page elements

**Selenium 4 Specifics:**

- Selenium Manager (automatic driver management)

- No manual geckodriver configuration

- Options-based Firefox configuration

- Modern wait patterns

### 4. Session Management

**Files:** `core/module_utils.py`, `sessions/` directory

**Responsibility:** Session capture and storage

**Session Types:**

- **localStorage** - Discord, Signal, Telegram

  - JSON file storage

  - Direct browser storage restoration

- **Profile** - WhatsApp

  - Firefox profile storage

  - Entire profile restoration

**Session Structure:**

```text
sessions/
├── discord/
│   └── [session_id]/
│       └── localstorage.json
├── whatsapp/
│   └── [session_id]/
│       └── firefox_profile/
├── signal/
│   └── [session_id]/
│       └── localstorage.json
└── telegram/
    └── [session_id]/
        └── localstorage.json
```

### 5. HTTP Server

**Files:** `core/module_utils.py` (server class)

**Responsibility:** Template-based web page serving

**Key Features:**

- Jinja2 template rendering

- Thread-safe operation

- Dynamic port binding

- Graceful cleanup

- SimpleHTTPRequestHandler integration

**Features:**

- Serve custom HTML pages

- Template variable rendering

- Static file serving

- Error handling

### 6. Configuration System

**Files:** `core/config/models.py`, `core/config/loader.py`, `core/Settings.py`

**Responsibility:** Application configuration management

**Configuration Hierarchy:**

1. Default values defined in code

1. Environment variables

1. Configuration loader defaults

1. Runtime settings from CLI and module context

**Configuration Data:**

```python
AppConfig:
  path: str                    # Working directory
  debug: bool                  # Debug mode
  development: bool            # Development mode
  verbose: bool                # Verbose output
  running_module: str          # Current module
  headless_browser: Browser    # Background Firefox
  visible_browser: Browser     # Visible Firefox
  previous: list[str]          # Module history
  history: list[str]           # Command history
```

### 7. UI and Output

**Files:** `core/ui.py`, `core/color.py`

**Responsibility:** Console interface and formatting

**Key Features:**

- ANSI color output

- Table rendering

- Readline integration

- Status messages

- Error reporting

**UI Functions:**

- `clear_screen()` - Clear terminal

- `info()`, `status()`, `error()`, `warning()` - Colored messages

- `title()` - Section headers

- `create_table()` - Formatted tables

- `init_readline()` - Tab completion

## Data Flow

### Grabber Module Execution Flow

```text
User: use grabber/discord
  ↓
Load module via plugin_manager
  ↓
Create headless browser (Selenium)
  ↓
Navigate to Discord login page
  ↓
Wait for QR code (XPath: image_xpath)
  ↓
Extract QR image from canvas
  ↓
Loop:
  - Check if user scanned QR (change_identifier)
  - If not, wait and check refresh button
  - If found, capture session data
  ↓
Save session to sessions/discord/[id]/
  ↓
Close browser
  ↓
Report success and session ID
```

### Post Module Execution Flow

```text
User: use post/discord
User: set session_id [id]
User: run
  ↓
Load session from sessions/discord/[id]/
  ↓
Create visible browser (Selenium)
  ↓
Load session data into browser
  ↓
Navigate to Discord app
  ↓
Browser window displays logged-in session
  ↓
User can interact with account
```

## Module Extension Points

### Creating Custom Modules

Modules extend QR-SHIELD capability. Structure:

```text
core/modules/
├── custom/
│   ├── __init__.py
│   └── telegram.py         # Custom implementation
```

**Module Guidelines:**

1. **Discovery** - Place in `core/modules/category/`

1. **Naming** - Use lowercase, underscore-separated names

1. **Structure** - Follow standard module template

1. **XPath** - Use cascading selectors with fallbacks

1. **Error Handling** - Graceful degradation

1. **Documentation** - Clear comments and docstrings

### Extending Core Services

Common extension points:

1. **Add Module Type**

   - Define in `core/module_utils.py`

   - Register in module system

   - Add CLI command handler

2. **Custom Browser Factory**

   - Override `core/browser.py` functions

   - Implement custom WebDriver creation

3. **Session Storage Backend**

   - Implement custom storage driver

   - Register with session manager

4. **CLI Command**

   - Add handler in `core/Cli.py`

   - Register keyword in `all_keywords`

## Performance Considerations

### Bottlenecks

1. **Browser Launch** - ~5-10 seconds per browser

1. **Page Load** - ~2-5 seconds per page

1. **XPath Queries** - Cascading selectors add latency

1. **Image Extraction** - Canvas operations are synchronous

### Optimization Strategies

1. **Reuse Browsers** - Keep browsers running when possible

1. **Headless Mode** - Faster than visible mode

1. **Optimize XPath** - Primary selector should match most cases

1. **Async Operations** - Threading for background tasks

## Security Architecture

### Security Boundaries

```text
Trusted:
  - Local filesystem
  - QR-SHIELD code
  - User configuration

Untrusted:
  - Target platforms (may be malicious)
  - Network traffic (may be MITM)
  - Session data (may be compromised)
  - User input (may be injection)
```

### Security Controls

1. **Input Validation** - Validate module names, paths, ports

1. **Error Handling** - No credential leakage in errors

1. **Session Protection** - File permissions on session storage

1. **Isolation** - Separate browser instances

1. **Cleanup** - Destroy browsers and close ports

## Deployment Architecture

### Development

```text
Local Machine
├── Python 3.10+
├── Firefox
├── QR-SHIELD code
└── Session storage
```

### Testing

```text
CI/CD Pipeline
├── Lint checks
├── Unit tests
├── Integration tests
└── Security scans
```

### Distribution

```text
Package Distribution
├── PyPI (Python Package Index)
├── GitHub Releases
└── Direct installation via git
```

## Scalability Considerations

### Limitations

- Single-threaded CLI (by design)

- Sequential module execution

- Limited by browser count

- File-based session storage

### Scaling Strategies (Future)

- Background job system

- Distributed session storage

- API server interface

- Containerization support

## Documentation Architecture

```text
docs/
├── index.md              # Documentation home
├── architecture.md       # This document
├── installation.md       # Install guide
├── usage.md             # Usage documentation
├── threat-model.md      # Threat analysis
├── security.md          # Security guide
├── faq.md               # Frequently asked questions
└── images/              # Diagrams and screenshots
```

## Technology Stack

| Component | Technology | Version | Purpose |
| --- | --- | --- | --- |
| Runtime | Python | 3.10+ | Core language |
| Browser | Selenium | 4.20+ | Automation |
| Browser Engine | Firefox | Latest | Headless rendering |
| Templates | Jinja2 | 2.10+ | Page rendering |
| HTTP | requests | 2.28.2 | HTTP requests |
| Images | Pillow | 5.4.1+ | QR code extraction |
| User Agent | user-agent | 0.1.9 | Random UA generation |

## Version History

### Version 1.0.0 (Current)

- ✅ Selenium 4 migration complete

- ✅ Python 3.10+ support

- ✅ Core module system stable

- ✅ Multi-platform support

See [CHANGELOG.md](CHANGELOG.md) for full history.

## Future Architecture Improvements

See [ROADMAP.md](ROADMAP.md) for planned enhancements.

---

**Last Updated:** July 2026

For technical questions, see [FAQ.md](FAQ.md) or open an issue.
