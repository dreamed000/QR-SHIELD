# Installation Guide

Complete platform-specific installation instructions for QR-SHIELD.

## System Requirements

- Python 3.10, 3.11, or 3.12

- Firefox browser (4.20+)

- Git

- pip package manager

- Virtual environment (recommended)

## Prerequisites

### Windows

1. Install Python from [python.org](https://www.python.org/downloads/)

   - Check "Add Python to PATH"

   - Disable "PATH length limit" if prompted

1. Install Firefox from [mozilla.org](https://www.mozilla.org/firefox/)

1. Install Git from [git-scm.com](https://git-scm.com/)

### macOS

```bash
# Install Homebrew if not installed
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Install Python, Firefox, and Git
brew install python@3.11 firefox git
```

### Linux (Ubuntu/Debian)

```bash
sudo apt update
sudo apt install python3.11 python3.11-venv firefox git pip
```

### Linux (Fedora/RHEL)

```bash
sudo dnf install python3.11 firefox git python3-pip
```

## Installation Steps

### 1. Clone Repository

```bash
git clone https://github.com/dreamed000/QR-SHIELD.git
cd QR-SHIELD
```

### 2. Create Virtual Environment

**Windows:**

```bash
python -m venv venv
.\venv\Scripts\activate
```

**macOS/Linux:**

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### 4. Verify Installation

```bash
python qrshield.py -x "help"
```

You should see the QR-SHIELD banner and help text.

## First Run

```bash
python qrshield.py
```

This launches the interactive CLI.

## Troubleshooting

### Python Not Found

Set Python path explicitly or ensure it's in PATH:

**Windows:**

```bash
C:\Python311\python.exe qrshield.py
```

**macOS/Linux:**

```bash
/usr/local/bin/python3 qrshield.py
```

### Firefox Not Found

Export Firefox location:

**Windows:**

```powershell
$env:QRSHIELD_FIREFOX_BINARY="C:\Program Files\Mozilla Firefox\firefox.exe"
```

**macOS:**

```bash
export QRSHIELD_FIREFOX_BINARY="/Applications/Firefox.app/Contents/MacOS/firefox"
```

**Linux:**

```bash
export QRSHIELD_FIREFOX_BINARY="/usr/bin/firefox"
```

### Permission Denied

Make script executable:

**macOS/Linux:**

```bash
chmod +x qrshield.py
```

### ModuleNotFoundError

Ensure virtual environment is activated and dependencies installed:

```bash
source venv/bin/activate  # macOS/Linux
pip install -r requirements.txt
```

## Next Steps

- [Quick Start](quick-start.md)

- [Usage Guide](../USAGE.md)

- [Architecture](architecture.md)

---

**Last Updated:** July 2026
