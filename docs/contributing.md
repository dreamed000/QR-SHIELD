# Contributing Guide

How to contribute to QR-SHIELD development.

This is a comprehensive guide for developers who want to contribute to QR-SHIELD.

See the root [CONTRIBUTING.md](../CONTRIBUTING.md) for complete details.

## Getting Started

### Prerequisites

- Python 3.10, 3.11, or 3.12

- Firefox browser

- Git

- GitHub account

### Setup Development Environment

```bash
# Clone your fork
git clone https://github.com/your-username/QR-SHIELD.git
cd QR-SHIELD

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # or .\venv\Scripts\activate on Windows

# Install development dependencies
pip install -e ".[dev]"

# Add upstream remote
git remote add upstream https://github.com/dreamed000/QR-SHIELD.git
```

## Development Workflow

### 1. Create Feature Branch

```bash
git fetch upstream
git checkout -b feature/your-feature-name upstream/main
```

Branch naming conventions:

- `feature/description` - New feature

- `bugfix/description` - Bug fix

- `docs/description` - Documentation

- `refactor/description` - Code refactoring

- `test/description` - Tests

### 2. Make Changes

**Code Style:** Follow PEP 8

```bash
# Format code
python -m black core/ tests/

# Check imports
python -m isort core/ tests/

# Lint with Ruff
python -m ruff check --fix core/ tests/
```

### 3. Write Tests

```bash
# Add test case to tests/
# Run tests
pytest tests/ -v

# Check coverage
pytest tests/ --cov=core --cov-report=html
```

### 4. Commit Changes

```bash
git add .
git commit -m "type: subject

- Detailed explanation
- Why this change
- What problem it solves"
```

Commit types:

- `feat:` - New feature

- `fix:` - Bug fix

- `docs:` - Documentation

- `refactor:` - Code refactoring

- `test:` - Tests

- `chore:` - Build, deps, etc.

### 5. Push and Submit PR

```bash
git push origin feature/your-feature-name
# Then create PR on GitHub
```

## Code Review

### Expectations

- Respond to feedback professionally

- Make requested changes

- Provide context and reasoning

- Ask for clarification if unclear

### Review Criteria

- Code follows style guidelines

- Changes are well-tested

- Documentation updated

- No breaking changes (without discussion)

- Security considerations addressed

## Adding Modules

### Create Grabber Module

**File:** `core/modules/grabber/platform.py`

```python
class info:
    author = "Your Name"
    short_description = "Platform name grabber"
    description = "Detailed description"

class execution:
    module_type = types.grabber
    name = "platform"
    url = "https://platform.url/login"
    image_xpath = '//xpath/to/qr/image'
    change_identifier = '//xpath/post-login/element'
    
    options = {
        # Optional: module-specific options
    }
    
    @staticmethod
    def run(global_options, visible_browser):
        # 1. Navigate to login page
        # 2. Wait for QR code
        # 3. Detect user action (scan)
        # 4. Capture session
        # 5. Return session info
        return {
            'status': 'success',
            'session_id': session_id,
            'platform': 'platform'
        }
```

### Create Post Module

**File:** `core/modules/post/platform.py`

```python
class info:
    author = "Your Name"
    short_description = "Platform name session controller"

class execution:
    module_type = types.post
    name = "platform"
    
    options = {
        'session_id': {
            'Description': 'Session ID to load',
            'Required': True,
            'Value': ''
        }
    }
    
    @staticmethod
    def run(global_options, visible_browser):
        session_id = execution.options['session_id']['Value']
        # 1. Load session from disk
        # 2. Initialize browser
        # 3. Restore session
        # 4. Navigate to platform
        # 5. Return control to user
        pass
```

## Testing

### Unit Tests

```python
# tests/test_module.py
import pytest
from core.modules.grabber.discord import execution

def test_grabber_discord():
    # Test implementation
    pass
```

### Running Tests

```bash
# All tests
pytest tests/ -v

# Specific test
pytest tests/test_module.py::test_grabber_discord -v

# With coverage
pytest tests/ --cov=core --cov-report=html
```

### Test Coverage

Aim for:

- ≥80% overall coverage

- ≥90% for critical paths

- ≥70% for edge cases

## Documentation

### Code Comments

- Comment complex logic

- Explain "why", not "what"

- Document non-obvious decisions

- Use docstrings for functions

```python
def extract_qr_code(element):
    """Extract QR code image from DOM element.
    
    Args:
        element: Selenium element containing QR code
        
    Returns:
        PIL Image object or None if not found
        
    Raises:
        Exception: If image extraction fails
    """
```

### Docstrings

Use Google-style docstrings:

```python
def function(arg1, arg2):
    """Brief description.
    
    Longer description if needed.
    
    Args:
        arg1: Description of arg1
        arg2: Description of arg2
        
    Returns:
        Description of return value
        
    Raises:
        ValueError: When validation fails
    """
```

### Markdown Documentation

- Keep clear and concise

- Use code examples

- Include cross-references

- Update related docs

## Version Management

### Semantic Versioning

Version format: `MAJOR.MINOR.PATCH`

- `MAJOR`: Breaking changes

- `MINOR`: New features (backward compatible)

- `PATCH`: Bug fixes

### Changelog

Update [CHANGELOG.md](../CHANGELOG.md):

```markdown
## [1.0.0] - 2026-07-03

### Added
- First public release entry

### Fixed
- Initial release baseline

### Changed
- Initial release baseline

### Security
- Initial release baseline
```

## Release Process

### Prepare Release

1. Update version in `core/Data/version.txt`

1. Update `CHANGELOG.md`

1. Create release branch

1. Submit PR for review

### After Merge

1. Tag release: `git tag v1.0.0`

1. Create GitHub release

1. Generate release notes

1. Announce release

## Community Guidelines

### Be Respectful

- Treat everyone with respect

- Use professional language

- Assume good intent

- Address disagreements constructively

### Ask for Help

- Questions are welcome

- Ask in discussions

- Comment on issues

- Reach out to maintainers

### Share Knowledge

- Document learning

- Help others

- Share solutions

- Contribute examples

## Issue Reporting

### Report Bugs

Include:

- Clear description

- Steps to reproduce

- Expected vs actual behavior

- Error messages/logs

- Environment info

### Suggest Features

Include:

- Problem statement

- Proposed solution

- Alternative approaches

- Use cases

## Resources

- [Architecture.md](architecture.md) - System design

- [ETHICS.md](../ETHICS.md) - Ethical guidelines

- [SECURITY.md](../SECURITY.md) - Security guidelines

- [Development.md](development.md) - Dev setup

## Getting Help

- Check documentation

- Search existing issues

- Ask in discussions

- Comment on issues

- Email maintainers

---

**Thank you for contributing to QR-SHIELD!**

---

**Last Updated:** July 2026
