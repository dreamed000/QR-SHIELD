# Installation Guide

## System Requirements

Before installing QR-SHIELD, ensure your system meets the following requirements:

### Operating System

- **Windows:** Windows 10/11 with PowerShell or CMD

- **macOS:** macOS 10.14+ (Intel or Apple Silicon)

- **Linux:** Ubuntu 18.04+, Debian 10+, CentOS 7+, RHEL 7+, or similar

### Software Requirements

- **Python:** 3.10, 3.11, or 3.12

- **Firefox:** Latest or ESR version

- **pip:** Python package manager (included with Python)

- **git:** For cloning the repository

### Hardware Requirements

- **CPU:** 2+ cores

- **RAM:** 2+ GB available

- **Disk:** 500 MB free space (plus session storage)

- **Network:** Internet connection (for target platform access)

### Browser

Firefox must be installed:

- **Windows:** Mozilla Firefox (standard installation)

- **macOS:** Mozilla Firefox (Homebrew or direct)

- **Linux:** Firefox (apt, yum, or direct)

---

## Pre-Installation Steps

### 1. Install Python

#### Windows

```bash
# Download from python.org or use Chocolatey
choco install python@3.12
```

**Verify:**

```powershell
python --version
# Should output: Python 3.12.x
```

#### macOS

```bash
# Using Homebrew (recommended)
brew install python@3.12

# Or download from python.org
```

**Verify:**

```bash
python3 --version
# Should output: Python 3.12.x
```

#### Linux (Ubuntu/Debian)

```bash
sudo apt update
sudo apt install python3.12 python3.12-venv python3-pip
```

**Verify:**

```bash
python3 --version
# Should output: Python 3.12.x
```

#### Linux (RHEL/CentOS)

```bash
sudo yum install python312 python312-pip
```

### 2. Install Firefox

#### Windows

Download from [mozilla.org](https://www.mozilla.org/en-US/firefox/new/):

```powershell
# Or use Chocolatey
choco install firefox
```

#### macOS

```bash
# Using Homebrew
brew install firefox

# Or download from mozilla.org
```

#### Linux

```bash
# Ubuntu/Debian
sudo apt install firefox

# CentOS/RHEL
sudo yum install firefox
```

**Verify:**

```bash
firefox --version
# Should output: Mozilla Firefox version
```

### 3. Install Git

#### Windows

Download from [git-scm.com](https://git-scm.com/):

```powershell
choco install git
```

#### macOS

```bash
brew install git
```

#### Linux

```bash
# Ubuntu/Debian
sudo apt install git

# CentOS/RHEL
sudo yum install git
```

**Verify:**

```bash
git --version
# Should output: git version x.x.x
```

---

## Installation Methods

### Method 1: Direct Installation (Recommended)

#### Step 1: Clone Repository

```bash
git clone https://github.com/dreamed000/QR-SHIELD.git
cd qr-shield
```

#### Step 2: Create Virtual Environment (Optional but Recommended)

```bash
# Create venv
python3 -m venv venv

# Activate venv

# On Windows (PowerShell):
.\venv\Scripts\Activate.ps1

# On Windows (CMD):
venv\Scripts\activate

# On macOS/Linux:
source venv/bin/activate
```

#### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

**Output should show successful installation of:**

- selenium

- requests

- urllib3

- Pillow

- Jinja2

- user-agent

#### Step 4: Verify Installation

```bash
python qrshield.py --help
```

**Expected output:**

```text
usage: qrshield [-h] [-r] [-x] [--debug] [--dev] [--verbose] [-q]

QR Shield: Security Research Framework
  ...
```

### Method 2: Development Installation

For developers contributing to QR-SHIELD:

```bash
# Clone repository
git clone https://github.com/dreamed000/QR-SHIELD.git
cd qr-shield

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # or .\venv\Scripts\activate on Windows

# Install in development mode
pip install -e ".[dev]"
```

### Method 3: Docker Installation (Future)

Docker support is planned for a future release. Check [ROADMAP.md](ROADMAP.md).

---

## Configuration

### Firefox Binary Path

QR-SHIELD automatically locates Firefox. If you have a non-standard installation:

```bash
# Set environment variable
export QRSHIELD_FIREFOX_BINARY="/path/to/firefox"

# Or
export FIREFOX_BINARY="/path/to/firefox"

# Then run
python qrshield.py
```

#### Finding Firefox Path

**Windows:**

```powershell
# Usually at:
C:\Program Files\Mozilla Firefox\firefox.exe
# or
C:\Program Files (x86)\Mozilla Firefox\firefox.exe
```

**macOS:**

```bash
/Applications/Firefox.app/Contents/MacOS/firefox
```

**Linux:**

```bash
which firefox
# or
/usr/bin/firefox
```

### Python Virtual Environment

Virtual environments isolate QR-SHIELD dependencies:

**Create:**

```bash
python3 -m venv qrshield_env
```

**Activate:**

- **Windows (PowerShell):** `.\qrshield_env\Scripts\Activate.ps1`

- **Windows (CMD):** `qrshield_env\Scripts\activate`

- **macOS/Linux:** `source qrshield_env/bin/activate`

**Deactivate:**

```bash
deactivate
```

**Recommended:** Always use a virtual environment.

---

## Troubleshooting Installation

### Issue: Python Not Found

**Solution:**

```bash
# Check Python is installed
python --version
# or
python3 --version

# Windows: Check PATH
echo %PATH%

# macOS/Linux: Check PATH
echo $PATH
```

If not found, reinstall Python and ensure it's in PATH.

### Issue: pip Not Found

**Solution:**

```bash
# Use Python's pip module
python -m pip install -r requirements.txt
# or
python3 -m pip install -r requirements.txt
```

### Issue: Permission Denied (Linux/macOS)

**Solution:**

Use `sudo` or virtual environment:

```bash
# Option 1: Virtual environment (recommended)
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Option 2: User install (not recommended)
pip install --user -r requirements.txt

# Option 3: Sudo (least recommended)
sudo pip install -r requirements.txt
```

### Issue: Firefox Not Found

**Solution:**

```bash
# Install Firefox
# Windows: choco install firefox
# macOS: brew install firefox
# Linux: sudo apt install firefox

# Verify installation
firefox --version

# Set Firefox path
export QRSHIELD_FIREFOX_BINARY="/path/to/firefox"
```

### Issue: Selenium Error

**Solution:**

```bash
# Verify Selenium installed
pip show selenium

# Reinstall Selenium
pip install --upgrade 'selenium>=4.20'

# Verify WebDriver
python -c "from selenium import webdriver; print('OK')"
```

### Issue: Module Import Error

**Solution:**

```bash
# Check Python path
python -c "import sys; print('\n'.join(sys.path))"

# Ensure you're in the qr-shield directory
cd /path/to/qr-shield

# Run with verbose output
python qrshield.py --verbose --debug
```

### Issue: Virtual Environment Not Activating

**Solution:**

```bash
# Windows (PowerShell): Enable script execution
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

# Then activate
.\venv\Scripts\Activate.ps1

# Or use CMD instead of PowerShell
venv\Scripts\activate
```

---

## Platform-Specific Notes

### Windows

**Prerequisites:**

- Visual C++ Build Tools (for some Python packages)

- PowerShell 5.0+

**Installation:**

```powershell
# Use PowerShell as Administrator
python -m pip install --upgrade pip
pip install -r requirements.txt

# Run
python qrshield.py
```

**Common Issues:**

- Execution policy restricts scripts - Run PowerShell as admin and execute: `Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser`

### macOS

**Prerequisites:**

- Xcode Command Line Tools: `xcode-select --install`

- Homebrew (optional but recommended)

**Installation:**

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python qrshield.py
```

**Common Issues:**

- M1/M2 Macs may need native Python 3.10+

- Check architecture: `uname -m` (should be arm64)

### Linux (Ubuntu/Debian)

**Prerequisites:**

- Build tools: `sudo apt install build-essential python3-dev`

- Development files: `sudo apt install python3.12-dev`

**Installation:**

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python3 qrshield.py
```

### Linux (RHEL/CentOS)

**Prerequisites:**

- Development tools: `sudo yum groupinstall 'Development Tools'`

- Python dev: `sudo yum install python312-devel`

**Installation:**

```bash
python3.12 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python3 qrshield.py
```

### WSL (Windows Subsystem for Linux)

QR-SHIELD supports WSL2:

```bash
# On WSL2 (Ubuntu/Debian)
sudo apt update
sudo apt install python3.12 python3-pip firefox

# Install QR-SHIELD
git clone https://github.com/dreamed000/QR-SHIELD.git
cd qr-shield
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Run
python3 qrshield.py
```

---

## Verifying Installation

### Quick Verification

```bash
# Navigate to qr-shield directory
cd /path/to/qr-shield

# Run help
python qrshield.py --help

# Show available modules
python qrshield.py -x "list"

# Show module info
python qrshield.py -x "info grabber/discord"
```

### Comprehensive Verification

```bash
# Check Python
python --version

# Check Firefox
firefox --version

# Check dependencies
pip list | grep -E "selenium|requests|Pillow|Jinja2"

# Check imports
python -c "from core import app; print('Core imports OK')"

# Check modules
python -c "from core.plugin_manager import discover_modules; print(discover_modules())"

# Test browser creation
python qrshield.py --verbose --debug
```

---

## Post-Installation Setup

### 1. Create Session Directory

Sessions are stored by default in `sessions/`:

```bash
mkdir -p sessions/{discord,whatsapp,signal,telegram}
```

This is created automatically on first run.

### 2. Set Firefox Binary (if needed)

```bash
# Linux/macOS
export QRSHIELD_FIREFOX_BINARY="/path/to/firefox"

# Windows PowerShell
$env:QRSHIELD_FIREFOX_BINARY="C:\Program Files\Mozilla Firefox\firefox.exe"

# Windows CMD
set QRSHIELD_FIREFOX_BINARY=C:\Program Files\Mozilla Firefox\firefox.exe
```

### 3. Verify Browser Automation

```bash
python qrshield.py -x "help"
# Should display help without errors
```

### 4. Test Module Loading

```bash
python qrshield.py -x "list"
# Should display available modules
```

---

## Updating QR-SHIELD

### Pull Latest Changes

```bash
cd /path/to/qr-shield
git pull origin main
```

### Update Dependencies

```bash
pip install --upgrade -r requirements.txt
```

### Verify After Update

```bash
python qrshield.py --help
```

---

## Uninstallation

### Remove QR-SHIELD

```bash
# If using virtual environment, just delete the directory
rm -rf qr-shield
rm -rf venv  # if separate

# If installed system-wide
pip uninstall qr-shield

# On Linux/macOS
sudo pip uninstall qr-shield
```

### Keep Session Data

Sessions are stored in `sessions/` directory:

```bash
# Backup before deletion
cp -r sessions/ sessions.backup/

# Then safely delete installation
rm -rf qr-shield
```

---

## Next Steps

After successful installation:

1. Read [USAGE.md](USAGE.md) to learn how to use QR-SHIELD

1. Review [ETHICS.md](ETHICS.md) for ethical guidelines

1. Check [FAQ.md](FAQ.md) for common questions

1. See [THREAT_MODEL.md](THREAT_MODEL.md) for understanding threats

1. Review [SECURITY.md](SECURITY.md) for security considerations

---

## Getting Help

### Troubleshooting

See [SUPPORT.md](SUPPORT.md) for troubleshooting steps.

### Common Issues

See [FAQ.md](FAQ.md) for frequently asked questions.

### Report Issues

Create an issue on [GitHub Issues](https://github.com/dreamed000/QR-SHIELD/issues).

---

**Last Updated:** July 2026

**Installation problems? Check [SUPPORT.md](SUPPORT.md) or open an issue.**
