# Development Setup

Setting up a complete development environment for QR-SHIELD.

## System Requirements

- Python 3.10, 3.11, or 3.12

- Firefox latest version

- Git

- Text editor or IDE (VS Code, PyCharm, etc.)

- At least 5GB free disk space

## Complete Setup

### 1. Clone Repository

```bash
# Clone your fork first
git clone https://github.com/your-username/QR-SHIELD.git
cd QR-SHIELD

# Add upstream remote
git remote add upstream https://github.com/dreamed000/QR-SHIELD.git
```

### 2. Create Virtual Environment

```bash
# Create environment
python3 -m venv venv

# Activate environment
# macOS/Linux:
source venv/bin/activate

# Windows:
.\venv\Scripts\activate
```

### 3. Install Dependencies

```bash
# Upgrade pip
pip install --upgrade pip

# Install project dependencies
pip install -r requirements.txt

# Install development tools
pip install -e ".[dev]"
```

### 4. IDE Setup

#### VS Code

Install extensions:

- Python

- Pylance

- Black Formatter

- isort

- Ruff

- Pytest

- Mypy

- Python Docstring Generator

Create `.vscode/settings.json`:

```json
{
  "python.defaultInterpreterPath": "${workspaceFolder}/venv/bin/python",
  "python.formatting.provider": "black",
  "[python]": {
    "editor.formatOnSave": true,
    "editor.defaultFormatter": "ms-python.python",
    "editor.codeActionsOnSave": {
      "source.organizeImports": true
    }
  },
  "python.testing.pytestEnabled": true,
  "python.testing.pytestPath": "${workspaceFolder}/venv/bin/pytest"
}
```

#### PyCharm

1. Open project

1. Set Python interpreter to venv

1. Enable pytest

1. Configure code inspections

1. Enable reformat on save

### 5. Pre-commit Hooks

Use the repository's `.pre-commit-config.yaml` and install Git hooks locally:

```bash
python -m pip install pre-commit
python -m pre_commit install
python -m pre_commit run --all-files
```

This ensures Black, isort, Ruff, and mypy run consistently before commits.

## Development Workflow

### Running the Application

```bash
# Run normally
python qrshield.py

# Debug mode
python qrshield.py --debug --verbose

# Development mode (auto-reload)
python qrshield.py --dev

# Execute command
python qrshield.py -x "list"
```

### Code Quality Checks

```bash
# Format code
python -m black core/ tests/ qrshield.py

# Sort imports
python -m isort core/ tests/ qrshield.py

# Lint code
python -m ruff check --fix core/ tests/ qrshield.py

# Type checking
python -m mypy --ignore-missing-imports --python-version=3.10 core tests/ qrshield.py

# Security scan
python -m bandit -r core/
```

### Running Tests

```bash
# All tests
pytest tests/ -v

# Specific test file
pytest tests/test_settings.py -v

# Specific test function
pytest tests/test_settings.py::test_function -v

# With coverage
pytest tests/ --cov=core --cov-report=html

# Watch mode (requires pytest-watch)
ptw tests/
```

### Debugging

#### Using pdb

```python
import pdb
pdb.set_trace()  # Breakpoint
```

#### VS Code Debugging

Create `.vscode/launch.json`:

```json
{
  "version": "0.2.0",
  "configurations": [
    {
      "name": "Python: QR-SHIELD",
      "type": "python",
      "request": "launch",
      "program": "${workspaceFolder}/qrshield.py",
      "console": "integratedTerminal"
    }
  ]
}
```

## Project Structure for Development

```text
QR-SHIELD/
├── core/                   # Main codebase
│   ├── __init__.py
│   ├── app.py             # Main application
│   ├── Cli.py             # CLI framework
│   ├── module.py          # Module system
│   ├── browser.py         # Selenium wrapper
│   ├── plugin_manager.py  # Module loading
│   ├── Settings.py        # Configuration
│   ├── db.py              # Database shim
│   ├── ui.py              # UI utilities
│   ├── color.py           # ANSI colors
│   ├── utils.py           # Utilities
│   ├── module_utils.py    # Server utilities
│   ├── config/            # Configuration
│   │   ├── models.py
│   │   ├── loader.py
│   │   └── defaults.py
│   ├── modules/           # Plugins
│   │   ├── grabber/
│   │   ├── post/
│   │   └── registry/
│   ├── templates/         # HTML templates
│   ├── www/               # Web assets
│   └── Data/              # Data files
├── tests/                 # Test code
│   ├── __init__.py
│   └── test_*.py
├── docs/                  # Documentation
├── .github/               # GitHub config
├── qrshield.py            # Entry point
├── requirements.txt       # Dependencies
└── pyproject.toml         # Project config
```

## Common Development Tasks

### Add a New Module

```bash
# Create module file
touch core/modules/grabber/newplatform.py

# Edit and implement
vim core/modules/grabber/newplatform.py

# Test it
python qrshield.py -x "use grabber/newplatform; run"

# Add tests
echo "def test_newplatform(): pass" >> tests/test_modules.py

# Run tests
pytest tests/test_modules.py
```

### Update Dependencies

```bash
# Show outdated packages
pip list --outdated

# Update specific package
pip install --upgrade package-name

# Update all
pip install --upgrade -r requirements.txt

# Update requirements.txt
pip freeze > requirements.txt
```

### Generate Documentation

```bash
# Build docs (requires mkdocs)
pip install mkdocs
mkdocs serve

# Check markdown
mdl docs/
```

## Troubleshooting Development

### Import Errors

```bash
# Reinstall virtual environment
deactivate
rm -rf venv
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Firefox Not Found

```bash
export QRSHIELD_FIREFOX_BINARY="/path/to/firefox"
python qrshield.py
```

### Port Already in Use

```text
qrshield> set port 8001
qrshield> run
```

### Test Failures

```bash
# Run with verbose output
pytest tests/ -vv -s

# Run with logging
pytest tests/ --log-cli-level=DEBUG

# Run single test
pytest tests/test_file.py::test_name -v
```

## Performance Profiling

### Memory Profiling

```bash
pip install memory_profiler

python -m memory_profiler qrshield.py
```

### CPU Profiling

```bash
pip install cProfile

python -m cProfile -s cumtime qrshield.py
```

## Security Analysis

### Static Analysis

```bash
# Bandit (security)
bandit -r core/

# MyPy (type checking)
mypy core/

# Ruff (code quality)
ruff check core/
```

### Dependency Check

```bash
pip install safety
safety check

pip install pip-audit
pip-audit
```

## Documentation Generation

### API Documentation

```bash
pip install pdoc
pdoc -o docs/api core
```

### Changelog

Keep `CHANGELOG.md` updated with each change.

## Release Preparation

### Version Bump

```bash
# Update version
echo "1.0.0" > core/Data/version.txt

# Update CHANGELOG
# Commit changes
git add .
git commit -m "chore: bump version to 1.0.0"

# Tag release
git tag v1.0.0
git push origin v1.0.0
```

---

**Last Updated:** July 2026

**Enjoy developing for QR-SHIELD!**
