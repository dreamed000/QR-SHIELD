# Quick Start Guide

This guide gets QR-SHIELD running locally with the current repository layout.

## 1. Install prerequisites

- Python 3.10 or newer

- Firefox installed and available on PATH, or a known path via the environment variable described below

## 2. Create and activate a virtual environment

```bash
python -m venv .venv
source .venv/bin/activate
```

On Windows PowerShell:

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
```

## 3. Install dependencies

```bash
pip install -r requirements.txt
```

For development tooling, install the optional extra:

```bash
pip install -e ".[dev]"
```

## 4. Start QR-SHIELD

```bash
python qrshield.py
```

You should see the QR-SHIELD banner and the interactive prompt.

## 5. Try a grabber module

```text
qrshield> list
qrshield> use grabber/discord
qrshield> run
```

The grabber opens a Firefox session and waits for the QR-based sign-in flow.

## 6. Reopen a captured session

```text
qrshield> sessions -l
qrshield> use post/discord
qrshield> set session_id <session-id>
qrshield> run
```

## 7. Troubleshooting

If Firefox is not found, point the application at the executable explicitly:

```bash
export QRSHIELD_FIREFOX_BINARY="/path/to/firefox"
python qrshield.py
```

On Windows PowerShell:

```powershell
$env:QRSHIELD_FIREFOX_BINARY = "C:\path\to\firefox.exe"
python qrshield.py
```

If you need more diagnostics:

```bash
python qrshield.py --debug --verbose
```

---

Last Updated: July 2026
