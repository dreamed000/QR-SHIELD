#!/usr/bin/env python3
"""QR Shield terminal UI helpers.

Provides simple ANSI color constants and small helpers for printing
consistent status/error/warning lines to the terminal. When the
`NO_COLOR` environment variable is set or stdout is not a TTY, the
color constants are empty strings.
"""

import os
import sys

# Color constants
G = "\033[32m"
Y = "\033[93m"
B = "\033[94m"
R = "\033[31m"
W = "\x1b[37m"
M = "\x1b[35m"
C = "\x1b[36m"
end = "\033[0m"
Bold = "\033[1m"
underline = "\033[4m"

# Disable colors when NO_COLOR set or not a TTY
if os.environ.get("NO_COLOR") or not sys.stdout.isatty():
    G = Y = B = R = W = M = C = end = Bold = underline = ""


def _line(prefix, color, text):
    print(end + Bold + prefix + end + color + str(text) + end)


def status(text):
    _line("[+] ", G, text)


def error(text):
    _line("[!] ", R, text)


def warning(text):
    _line("[W] ", Y, text)


def goodbye():
    # Exit cleanly
    sys.exit(0)
