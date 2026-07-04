# Changelog

All notable changes to QR-SHIELD are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/), and this project adheres to [Semantic Versioning](https://semver.org/).

## [Unreleased]

### Planned

- Additional platform modules (Instagram, LinkedIn)

- Automated selector validation

- Enhanced session management

- To be completed

---

## [1.0.0] - 2026-07-03

### First Public Release

This release marks the first public GitHub release of QR-SHIELD, with a modern Python packaging setup, documentation updates, and release-ready citation metadata.

### Added

- **Selenium 4.20+ Support**

  - Automated driver management via Selenium Manager

  - No manual geckodriver configuration required

  - Improved Firefox integration

  - Modern WebDriver API

- **Python 3.10+ Full Support**

  - Native pathlib library (removed pathlib2)

  - Type hints throughout codebase

  - Modern string formatting

  - Improved error messages

- **Enhanced Module System**

  - Plugin architecture for extensibility

  - Dynamic module discovery

  - Cascading XPath fallbacks

  - Development mode with module reload

- **Multi-Platform Grabber Modules**

  - Discord QR-session grabber (localStorage)

  - WhatsApp QR-session grabber (profile-based)

  - Signal QR-session grabber

  - Telegram QR-session grabber

  - Platform-specific DOM selectors

- **Post-Exploitation Modules**

  - Discord session replay

  - WhatsApp session replay

  - Signal session replay

  - Telegram session replay

  - Session restoration in isolated browsers

- **Browser Automation**

  - Firefox-based Selenium automation

  - User agent rotation

  - Headless and visible browser modes

  - Custom Firefox binary resolution

  - WSL2 detection and support

- **CLI Framework**

  - Interactive command shell

  - Command history and readline integration

  - Resource file execution

  - Module context management

  - Debug, development, and verbose modes

- **HTTP Server Integration**

  - Thread-safe Jinja2 template serving

  - Dynamic port binding

  - Graceful socket reuse

  - Custom HTML rendering

- **Session Management**

  - localStorage-based session capture

  - Profile-based session capture

  - Session isolation

  - Session restoration

- **Configuration System**

  - Environment variable support

  - Runtime configuration flags

  - Development mode options

  - Custom settings per execution

### Changed

- **Removed Deprecated Dependencies**

  - Removed pathlib2 (Python 3.10+ native)

  - Removed FirefoxProfile (Selenium 4 uses Options)

  - Removed legacy urllib2 code

- **Module System Redesign**

  - New plugin_manager with discover_modules()

  - Unified module type system (grabber/post)

  - Registry-based module indexing

  - Lazy module loading with development reload

- **Browser Automation Overhaul**

  - Selenium 4 compatibility layer

  - Options-based configuration

  - Modern wait patterns

  - Improved error handling

- **Configuration Architecture**

  - AppConfig dataclass model

  - Loader-based initialization

  - Environment-aware configuration

  - Cleaner settings hierarchy

### Fixed

- Firefox binary resolution on multiple platforms

- XPath selector cascading for DOM changes

- Session data protection

- Browser cleanup on errors

- Command history persistence

- UI color output formatting

### Security

- Secure session file permissions

- No credential leakage in error messages

- Input validation on all module parameters

- Safe browser cleanup and process termination

- [SECURITY] See SECURITY.md for details

### Documentation

- [NEW] Complete architecture documentation

- [NEW] Threat model analysis

- [NEW] Security policy

- [NEW] Ethical guidelines

- [NEW] Responsible disclosure process

- [NEW] Installation and usage guides

- [NEW] FAQ and troubleshooting

### Dependencies

- Selenium >=4.20 (upgraded from 4.x)

- urllib3 ==1.26.15 (maintained)

- requests ==2.28.2 (maintained)

- Pillow >=5.4.1 (maintained)

- Jinja2 >=2.10 (maintained)

- user-agent >=0.1.9 (maintained)

### Upgrade Instructions

```bash
# Backup existing sessions
cp -r sessions/ sessions.backup/

# Update QR-SHIELD
git pull origin main
pip install -r requirements.txt

# Verify installation
python qrshield.py --help
```

### Known Issues

To be completed

### Contributors

Puneet Chandra Chaudhary (@dreamed000)

---

## Version Numbering

QR-SHIELD follows [Semantic Versioning](https://semver.org/):

- **MAJOR** version for breaking changes

- **MINOR** version for new features (backward compatible)

- **PATCH** version for bug fixes (backward compatible)

---

## Release Notes

### How to Get This Version

- **Release Date:** July 3, 2026

- **Git Tag:** `v1.0.0`

- **PyPI:** `qr-shield==1.0.0`

- **Installation:** `pip install -r requirements.txt`

### Support

- **Status:** Active development

- **Support until:** TBD

- **Python versions:** 3.10, 3.11, 3.12

- **Firefox versions:** ESR and Latest

---

## Previous Releases

### Archives

Older releases and their documentation are available at:

- [GitHub Releases](https://github.com/dreamed000/QR-SHIELD/releases)

- [GitHub Tags](https://github.com/dreamed000/QR-SHIELD/tags)

---

## Roadmap

For planned features and upcoming releases, see [ROADMAP.md](ROADMAP.md).

---

## Security Updates

For security-related changes, see [SECURITY.md](SECURITY.md).

Security releases are marked with `[SECURITY]` tag:

- [SECURITY] Critical vulnerability fix

- [SECURITY] High-severity patch

- [SECURITY] Security hardening

---

## Contributing

We welcome contributions! See [CONTRIBUTING.md](CONTRIBUTING.md) for details.

---

## License

QR-SHIELD is distributed under a professional Dual Licensing Model. See [LICENSE](LICENSE) and [COMMERCIAL-LICENSE.md](COMMERCIAL-LICENSE.md) for complete licensing information.

---

**Last Updated:** July 2026

**Changelog Format:** [Keep a Changelog](https://keepachangelog.com/)

**Version Format:** [Semantic Versioning](https://semver.org/)
