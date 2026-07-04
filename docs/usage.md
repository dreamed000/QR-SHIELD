# Usage Guide

This guide reflects the current QR-SHIELD CLI and module system as implemented in the repository.

## Requirements

- Python 3.10 or newer

- Firefox installed and reachable on your system

- The Python dependencies from requirements.txt

## Start the application

```bash
python qrshield.py
```

The interactive prompt starts with the QR-SHIELD banner and available module list.

## Core CLI commands

```text
qrshield> help
qrshield> list
qrshield> show
qrshield> info <module>
qrshield> use <module>
qrshield> options
qrshield> set <option> <value>
qrshield> run
qrshield> back
qrshield> exit
```

### Non-interactive startup

```bash
# Run a single command
python qrshield.py -x "list"

# Run several commands in sequence
python qrshield.py -x "use grabber/discord; info; run"

# Execute commands from a resource file
python qrshield.py -r commands.rc
```

## Module types

### Grabber modules

Grabber modules open a browser to a login page and wait for a QR-code-based sign-in flow.

Available modules include:

- grabber/discord

- grabber/whatsapp

- grabber/signal

- grabber/telegram

Typical flow:

```text
qrshield> use grabber/discord
qrshield> options
qrshield> run
```

### Post modules

Post modules reopen a previously captured session in a visible Firefox window.

Available modules include:

- post/discord

- post/whatsapp

- post/signal

- post/telegram

Typical flow:

```text
qrshield> sessions -l
qrshield> use post/discord
qrshield> set session_id <session-id>
qrshield> run
```

## Module options

The runtime options exposed by the current module system are:

- port: local port for the grabber web server

- host: local host interface for the grabber web server

- useragent: default, random, or a custom user-agent string

- session_id: identifier of a previously captured session for post modules

Examples:

```text
qrshield> use grabber/discord
qrshield> set host 127.0.0.1
qrshield> set port 8080
qrshield> set useragent (random)
```

```text
qrshield> use post/discord
qrshield> set session_id discord_2025_01_01_120000
```

## Session management

The current session commands are:

```text
qrshield> sessions -l
qrshield> sessions -s <type>
qrshield> sessions -i <id>
qrshield> sessions -k <id>
qrshield> sessions -K
```

Examples:

```text
qrshield> sessions -l
qrshield> sessions -i discord_2025_01_01_120000
qrshield> sessions -k discord_2025_01_01_120000
```

## Debugging and troubleshooting

Use the built-in debug and verbose toggles when you need more detail:

```bash
python qrshield.py --debug --verbose
```

Or from the interactive prompt:

```text
qrshield> debug
qrshield> verbose
```

If Firefox is not detected, set the binary path before launching:

```bash
export QRSHIELD_FIREFOX_BINARY="/path/to/firefox"
python qrshield.py
```

On Windows, use the equivalent PowerShell syntax or set the environment variable in the shell before starting the app.

---

Last Updated: July 2026
