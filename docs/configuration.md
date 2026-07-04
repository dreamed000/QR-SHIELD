# Configuration Guide

QR-SHIELD currently uses a small, code-driven configuration model rather than a persistent config file.

## Supported startup flags

The launcher in [core/app.py](../core/app.py) supports these flags:

```bash
python qrshield.py
python qrshield.py -q
python qrshield.py --debug
python qrshield.py --dev
python qrshield.py --verbose
python qrshield.py -x "list"
python qrshield.py -r commands.rc
```

## Runtime toggles

The interactive CLI supports these toggles:

```text
qrshield> debug
qrshield> dev
qrshield> verbose
```

## Environment variables

The browser layer uses these environment variables when present:

```bash
# Preferred Firefox binary path
export QRSHIELD_FIREFOX_BINARY="/path/to/firefox"

# Legacy fallback name
export FIREFOX_BINARY="/path/to/firefox"

# Optional geckodriver override
export QRSHIELD_GECKODRIVER="/path/to/geckodriver"

# Legacy fallback name
export GECKODRIVER_PATH="/path/to/geckodriver"
```

On Windows PowerShell, use the equivalent syntax:

```powershell
$env:QRSHIELD_FIREFOX_BINARY = "C:\path\to\firefox.exe"
$env:QRSHIELD_GECKODRIVER = "C:\path\to\geckodriver.exe"
```

The WSL detection path also uses the WSL_DISTRO_NAME environment variable.

## Module options

Module-specific options are configured at runtime through the CLI.

### Grabber modules

```text
qrshield> use grabber/discord
qrshield> set port 8080
qrshield> set host 127.0.0.1
qrshield> set useragent (random)
qrshield> run
```

### Post modules

```text
qrshield> use post/discord
qrshield> set session_id discord_2025_01_01_120000
qrshield> run
```

## Current limitations

There is no implemented user config file or profile store at this time. Configuration is currently limited to:

- CLI flags

- interactive mode toggles

- module options

- Firefox and geckodriver discovery variables

## Troubleshooting

If Firefox is not found, confirm that the browser is installed and that the environment variable points to the correct executable.

```bash
python qrshield.py --debug
```

---

Last Updated: July 2026
