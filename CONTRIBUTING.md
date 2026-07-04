# Contributing to QR-SHIELD

Thank you for your interest in contributing to QR-SHIELD. This document provides guidelines for participation in this security research project.

## Code of Conduct

By participating in QR-SHIELD, you agree to uphold our [Code of Conduct](CODE_OF_CONDUCT.md). We are committed to providing a welcoming environment for all contributors.

## Our Commitment

QR-SHIELD exists to advance defensive security and threat detection. Contributors commit to:

- Using the project only for authorized, legal, and research-oriented purposes

- Promoting ethical security practices

- Advancing defensive capabilities

- Respecting privacy and legal boundaries

- Supporting the broader security community

## Before You Contribute

### Understand the Project

- Read [ETHICS.md](ETHICS.md) - Understand ethical boundaries

- Read [SECURITY.md](SECURITY.md) - Review security considerations

- Read [DISCLAIMER.md](DISCLAIMER.md) - Understand legal implications

- Read [THREAT_MODEL.md](THREAT_MODEL.md) - Understand threat analysis

### Verify Your Use Case

Contributions must align with authorized security research and defensive purposes. If uncertain, open a discussion issue before implementing changes.

## Types of Contributions

### Bug Reports

**Submit via:** [GitHub Issues](https://github.com/dreamed000/QR-SHIELD/issues)

Include:

- Clear description of the bug

- Steps to reproduce

- Expected behavior

- Actual behavior

- Environment details (Python version, OS, Firefox version)

- Error messages and logs

See bug report template: [.github/ISSUE_TEMPLATE/bug_report.md](.github/ISSUE_TEMPLATE/bug_report.md)

### Feature Requests

**Submit via:** [GitHub Issues](https://github.com/dreamed000/QR-SHIELD/issues)

Include:

- Clear use case for the feature

- How it advances defensive security or research

- Implementation approach (if known)

- Potential impact or concerns

See feature request template: [.github/ISSUE_TEMPLATE/feature_request.md](.github/ISSUE_TEMPLATE/feature_request.md)

### Code Contributions

#### Process

1. **Fork the repository**

   ```bash
   git clone https://github.com/YOUR-USERNAME/QR-SHIELD.git
   cd qr-shield
   git remote add upstream https://github.com/dreamed000/QR-SHIELD.git
   ```

1. **Create a feature branch**

   ```bash
   git checkout -b feature/your-feature-name
   ```

1. **Make your changes**

   - Follow code style guidelines

   - Write clear commit messages

   - Add tests for new functionality

   - Update documentation

1. **Commit with clear messages**

   ```bash
   git commit -m "Add feature X for defensive Y"
   ```

1. **Keep your fork in sync**

   ```bash
   git fetch upstream
   git rebase upstream/main
   ```

1. **Push to your fork**

   ```bash
   git push origin feature/your-feature-name
   ```

1. **Submit a Pull Request**

   - Reference any related issues

   - Describe your changes clearly

   - Explain the benefit for the project

See PR template: [.github/PULL_REQUEST_TEMPLATE.md](.github/PULL_REQUEST_TEMPLATE.md)

### Documentation Contributions

Documentation improvements are valuable contributions:

- Fix typos and unclear explanations

- Clarify complex concepts

- Add examples and tutorials

- Translate documentation

- Improve architecture documentation

### Module Contributions

QR-SHIELD's module system is designed for extension.

#### Module Structure

New grabber/post modules should follow the existing pattern:

```python
# -*- coding: utf-8 -*-
# Description and platform info
from core.module_utils import types

class info:
    author = "Your Name"
    short_description = "Brief description"
    full_description = None

class execution:
    module_type = types.grabber  # or types.post
    name = "platform_name"
    url = "https://platform.url"
    session_type = "localstorage"  # or "profile"

    # XPath definitions with cascading fallbacks
    image_xpath = '//your/xpath/here'
    image_xpath_alt1 = '//fallback/1'
    # ... additional fallbacks

    change_identifier = '//post-login/detector'
```

#### Module Guidelines

- Use cascading XPath selectors (primary + fallbacks)

- Include clear comments explaining selectors

- Test against current platform DOM

- Document selector maintenance notes

- Add user agent rotation support

- Handle session detection gracefully

#### Before Submitting

- Test thoroughly with current platform versions

- Verify selectors with multiple DOM states

- Add error handling for failing selectors

- Include documentation comments

- Update session storage appropriately

## Code Style

### Python Style Guide

QR-SHIELD follows PEP 8 with these specifics:

```python
# Imports: standard library, then third-party, then local
import os
import sys
import traceback

import requests
from selenium import webdriver

from core import Settings, ui

# Type hints where helpful
def process_session(session_id: str) -> bool:
    """Process a captured session."""
    pass

# Clear comments explaining complex logic
# Use descriptive variable names
# Keep functions focused and testable

# Line length: 88 characters (Black style)
```

### Naming Conventions

- `ClassName` - Classes use PascalCase

- `function_name()` - Functions use snake_case

- `CONSTANT_VALUE` - Constants use UPPER_CASE

- `_private_var` - Private variables lead with underscore

### Comments and Docstrings

```python
def capture_session(module_name: str) -> dict:
    """
    Capture a session using the specified module.

    Args:
        module_name: Name of the grabber module to use.

    Returns:
        Dictionary containing session data or error information.

    Raises:
        ValueError: If module_name is empty or invalid.
    """
```

## Testing

### Test Requirements

- All new features should include tests

- Tests should verify core functionality

- Tests should handle error conditions

- Use descriptive test names

### Running Tests

```bash
python -m pytest tests/
python -m pytest tests/test_settings.py -v
```

### Test Structure

```python
# tests/test_feature.py
import unittest
from core import module

class TestFeature(unittest.TestCase):
    def setUp(self):
        """Set up test fixtures."""
        pass

    def test_core_functionality(self):
        """Test primary feature behavior."""
        result = module.function()
        self.assertTrue(result)

    def test_error_handling(self):
        """Test error conditions."""
        with self.assertRaises(ValueError):
            module.function(invalid_input)
```

## Commit Messages

Write clear, descriptive commit messages:

```text
Add XPath fallbacks for platform update (Closes #42)

- Add three additional XPath fallbacks for QR detection
- Improve selector stability for June 2025 DOM changes
- Test with current platform version
- Include maintenance documentation
```

Format:

- First line: 50 characters max, imperative tense

- Blank line

- Body: Explain what and why

- References: Link to related issues

## Pull Request Process

### Before Submitting

1. **Code Review Checklist:**

   - [ ] Code follows PEP 8 style

   - [ ] All tests pass

   - [ ] New tests added for new functionality

   - [ ] Documentation updated

   - [ ] Commit messages are clear

   - [ ] No debugging code or print statements

   - [ ] No hardcoded credentials or secrets

1. **Security Checklist:**

   - [ ] No unintended side effects

   - [ ] No new security vulnerabilities

   - [ ] Error handling is appropriate

   - [ ] Follows responsible disclosure principles

1. **Testing:**

   ```bash
   python -m pytest tests/
   python qrshield.py --help
   python qrshield.py -x "help"
   ```

### During Review

- Be responsive to feedback

- Be willing to make changes

- Ask clarifying questions

- Provide context when needed

### After Approval

- Ensure CI/CD passes

- Await maintainer approval

- PR will be merged to main branch

## Reporting Security Issues

**Do not open public issues for security vulnerabilities.**

See [SECURITY.md](SECURITY.md) and [RESPONSIBLE_DISCLOSURE.md](RESPONSIBLE_DISCLOSURE.md) for reporting procedures.

## Attribution

Contributors will be recognized in:

- [ACKNOWLEDGEMENTS.md](ACKNOWLEDGEMENTS.md)

- Release notes and CHANGELOG

- Git commit history

## Questions?

- Check [FAQ.md](FAQ.md) for common questions

- Open a discussion issue

- Review existing issues and PRs

- Check documentation

## Recognition

Contributions are valued and recognized. Contributors are thanked in:

- Project releases

- ACKNOWLEDGEMENTS file

- Community discussions

## License

By contributing, you agree that your contributions will be licensed under the Community Research License. See [LICENSE](LICENSE).

---

**Thank you for contributing to security research and defensive capability.**
