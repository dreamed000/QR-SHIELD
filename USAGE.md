# Usage Guide

## Overview

QR-SHIELD is a modular, terminal-driven framework for researching QR-based authentication flows. The current implementation exposes:

- a small interactive CLI

- grabber modules for browser-based QR capture

- post modules for reopening previously captured sessions

- a Firefox-based browser automation layer

## Start the application

```bash
python qrshield.py
```

## Main commands

```text
qrshield> help
qrshield> list
qrshield> info <module>
qrshield> use <module>
qrshield> options
qrshield> set <option> <value>
qrshield> run
qrshield> back
qrshield> exit
```

## Non-interactive execution

```bash
# one command
python qrshield.py -x "list"

# multiple commands
python qrshield.py -x "use grabber/discord; info; run"

# run from a resource file
python qrshield.py -r commands.rc
```

## Module workflow

### Grabber modules

Grabber modules automate a QR-based login page and wait to capture a session.

```text
qrshield> use grabber/discord
qrshield> options
qrshield> run
```

### Post modules

Post modules reopen a previously captured session in a visible browser window.

```text
qrshield> sessions -l
qrshield> use post/discord
qrshield> set session_id <session-id>
qrshield> run
```

## Available module families

### Grabbers

- grabber/discord

- grabber/whatsapp

- grabber/signal

- grabber/telegram

### Posts

- post/discord

- post/whatsapp

- post/signal

- post/telegram

## Module options

The current runtime module options are:

- port: local port for the grabber web server

- host: local host interface for the grabber web server

- useragent: (default), (random), or a custom string

- session_id: session identifier for post modules

## Session commands

```text
qrshield> sessions -l
qrshield> sessions -s <type>
qrshield> sessions -i <id>
qrshield> sessions -k <id>
qrshield> sessions -K
```

## Debugging

```bash
python qrshield.py --debug --verbose
```

Or interactively:

```text
qrshield> debug
qrshield> verbose
```

## Firefox configuration

If Firefox is not resolved automatically, point the app to the binary explicitly.

```bash
export QRSHIELD_FIREFOX_BINARY="/path/to/firefox"
python qrshield.py
```

---

Last Updated: July 2026
