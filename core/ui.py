#!/usr/bin/env python3
# QR Shield console UI helpers
import atexit
import os
import shlex
import shutil
import subprocess
from typing import Any

from .color import B, Bold, C, G, R, Y, end

readline: Any
try:
    import readline  # type: ignore
except ImportError:
    readline = None


def clear_screen():
    try:
        if os.name == "nt":
            subprocess.run(
                ["cmd", "/c", "cls"],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                shell=False,
            )
        else:
            print("\033[2J\033[H", end="")
    except Exception:
        pass


def _line(prefix, color, text):
    print(end + Bold + prefix + end + color + str(text) + end)


def info(text):
    _line("[*] ", C, text)


def status(text):
    _line("[+] ", G, text)


def error(text):
    _line("[!] ", R, text)


def warning(text):
    _line("[W] ", Y, text)


def title(text):
    width = max(60, len(text) + 4)
    line = "=" * width
    print(Bold + line + end)
    print(Bold + f"= {text.center(width - 4)} =" + end)
    print(Bold + line + end)


class PromptCompleter:
    def __init__(self, options=None):
        self.options = sorted(set(options or []))

    def complete(self, text, state):
        if state == 0:
            self.matches = [opt for opt in self.options if opt.startswith(text)]
        try:
            return self.matches[state]
        except IndexError:
            return None


def init_readline(options=None, history_file=None):
    if not readline:
        return
    if history_file is None:
        history_file = os.path.join(os.getcwd(), ".qrshield_history")

    try:
        completer = PromptCompleter(options)
        readline.set_completer(completer.complete)
        if readline.__doc__ and "libedit" in readline.__doc__:
            readline.parse_and_bind("bind ^I rl_complete")
        else:
            readline.parse_and_bind("tab: complete")
        readline.parse_and_bind("set colored-completion-prefix on")
        readline.parse_and_bind("set show-all-if-unmodified on")
        readline.parse_and_bind("set horizontal-scroll-mode on")
        if os.path.exists(history_file):
            try:
                readline.read_history_file(history_file)
            except Exception:
                pass
        readline.set_history_length(200)
    except Exception:
        pass

    def save_history():
        try:
            readline.write_history_file(history_file)
        except Exception:
            pass

    atexit.register(save_history)


def split_commands(line):
    lexer = shlex.shlex(line, posix=True)
    lexer.whitespace = ";"
    lexer.whitespace_split = True
    lexer.commenters = "#"
    return [part.strip() for part in lexer if part.strip()]


def format_prompt(name, debug=False, development=False, verbose=False):
    badges = []
    if debug:
        badges.append(f"{Y}DEBUG{end}")
    if development:
        badges.append(f"{B}DEV{end}")
    if verbose:
        badges.append(f"{C}VERBOSE{end}")
    badge_text = " ".join(badges)
    return f"\n{name}{' ' + badge_text if badge_text else ''}{G} > {end}"


def create_table(headers, rows):
    import re
    import unicodedata

    def _vis_len(s):
        clean = re.sub(r"\x1b\[[0-9;]*m", "", str(s))
        width = 0
        for ch in clean:
            eaw = unicodedata.east_asian_width(ch)
            width += 2 if eaw in ("W", "F") else 1
        return width

    def _pad(s, width):
        return str(s) + " " * (width - _vis_len(s))

    term_w = shutil.get_terminal_size((120, 24)).columns
    all_rows = [headers] + list(rows)
    n_cols = max(len(r) for r in all_rows)

    col_w = [0] * n_cols
    for row in all_rows:
        for i, cell in enumerate(row):
            col_w[i] = max(col_w[i], _vis_len(str(cell)))

    total = sum(col_w) + (n_cols - 1) * 2 + 2
    if total > term_w and n_cols > 1:
        col_w[-1] = max(8, col_w[-1] - (total - term_w))

    sep = "  " + "  ".join("─" * w for w in col_w)

    print()
    print("  " + "  ".join(_pad(str(h), col_w[i]) for i, h in enumerate(headers)))
    print(sep)
    for row in rows:
        cells = list(row) + [""] * (n_cols - len(row))
        print("  " + "  ".join(_pad(str(cells[i]), col_w[i]) for i in range(n_cols)))
