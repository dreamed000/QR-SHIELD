#!/usr/bin/env python3
# QR Shield core utilities
import atexit
import importlib
import os
import random
import shutil
from typing import Any, Callable, Iterable, cast

from .color import Bold, C, G, M, R, end

# Ensure `readline` exists as a module object on all platforms. When the
# real readline isn't available (Windows without pyreadline), create a
# lightweight dummy module that provides the attributes our code expects.
try:
    import readline as _readline  # type: ignore

    readline = cast(Any, _readline)
except Exception:
    import types

    _readline = cast(Any, types.ModuleType("readline"))
    setattr(_readline, "get_line_buffer", lambda: "")
    setattr(_readline, "set_completer", lambda func: None)
    setattr(_readline, "parse_and_bind", lambda s: None)
    setattr(_readline, "read_history_file", lambda f: None)
    setattr(_readline, "write_history_file", lambda f: None)
    setattr(_readline, "set_history_length", lambda n: None)
    setattr(_readline, "set_completer_delims", lambda s: None)
    _readline.__doc__ = ""
    readline = cast(Any, _readline)


def banner(m) -> None:
    """Print a random banner to the terminal.

    Args:
        m: iterable of module names used to display counts in the banner.
    """
    # Choose a random banner and prints it
    import subprocess

    try:
        subprocess.run(["clear" if os.name != "nt" else "cls"], shell=False, timeout=2)
    except Exception:
        pass  # Graceful fallback if clear fails

    try:
        with open(os.path.join("core", "Data", "banners.txt"), encoding="utf-8") as _bf:
            banners = _bf.read().split("$$$$$AnyShIt$$$$$$")
    except FileNotFoundError:
        print("[!] Banner file not found")
        return
    except Exception as e:
        print(f"[!] Error loading banners: {e}")
        return

    banner = random.choice(banners) if banners else ""
    try:
        with open(os.path.join("core", "Data", "version.txt"), encoding="utf-8") as _vf:
            v = _vf.read().strip()
    except FileNotFoundError:
        v = "unknown"
    except Exception:
        v = "unknown"
    grabbers = len([i for i in m if "grabber" in i])
    post = len([i for i in m if "post" in i])
    banner_text = banner.format(Name="", Description="", Loaded="").rstrip()
    panel_lines = [
        f"{Bold}{R}QR-SHIELD Framework{end}",
        f"{C}By Puneet Chandra Chaudhary - D0C70R{end}",
        "",
        f"{M}Version{end}: {v}",
        f"{M}Email{end}: dreamdrafted000@gmail.com",
        f"{M}Instagram{end}: @_dreamdrafted_",
        f"{M}Loaded Grabbers{end}: {grabbers}",
        f"{M}Loaded Post Modules{end}: {post}",
    ]
    panel = "\n".join(f"  {line}" for line in panel_lines)
    banner_to_print = f"{Bold}{G}{banner_text}{end}\n{panel}"
    print(banner_to_print)
    return


def getinput() -> Callable[..., str]:
    """Return the builtin input function (compatibility shim)."""
    return input


def reload(module):
    """Reload an already-imported module and return it.

    Args:
        module: module object to reload.
    Returns:
        The reloaded module object.
    """
    return importlib.reload(module)


def create_table(headers, rows) -> None:
    """Print a Unicode table.

    Args:
        headers: iterable of column header values.
        rows: iterable of row iterables.
    """
    import re
    import unicodedata

    def _vis_len(s):
        clean = re.sub(r"\x1b\[[0-9;]*m", "", str(s))
        w = 0
        for ch in clean:
            eaw = unicodedata.east_asian_width(ch)
            w += 2 if eaw in ("W", "F") else 1
        return w

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


def pythonize(path: str) -> str:
    """Convert a path to a python importable dotted path.

    Normalizes forward/back slashes and lowercases the path.
    """
    return path.lower().replace("/", ".").replace("\\", "")


def humanize(path: str) -> str:
    """Convert a python importable dotted path back to a normal path."""
    return path.lower().replace(".", "/")


def grab_wanted(cmd: str, keywords: Iterable[str]) -> str:
    """Return up to 3 suggestions for a mistyped command.

    Args:
        cmd: the user-typed command fragment.
        keywords: iterable of valid keywords.
    Returns:
        Comma-separated suggestion string.
    """
    wanted = []
    for i in reversed(range(1, 5)):
        for s in keywords:
            if s[:i] == cmd[:i] and s not in wanted:
                wanted.append(s)
        if wanted:
            break
    return ", ".join(wanted[:3])


def check_version():
    # Use the shipped version file for compatibility verification
    try:
        with open(
            os.path.join("core", "Data", "version.txt"), "r", encoding="utf-8"
        ) as fh:
            return fh.read().strip()
    except Exception:
        return None


def my_map(func, values):
    # Map wrapper for consistent behavior across Python versions
    result = []
    for value in values:
        result.append(func(value))
    return result


# TODO: make autocomplete fix typos                                               (Done)
# TODO: make autocomplete with parts like whatsapp replaced with grabber/whatsapp (DONE)
# Say hi to my own autocomplete implementation :)
class MyCompleter(object):
    def __init__(self, options):
        self.options = sorted(options)
        self.module_options = sorted(["host", "port", "useragent"])

    def complete(self, text, state):
        if state == 0:
            if text:
                text = text.lower()
                line = readline.get_line_buffer()  # This one gets the whole line typed
                # If user is typing 'use' or 'info', prefer module suggestions
                if line.startswith("use") or line.startswith("info"):
                    self.matches = [
                        m for m in self.options if "/" in m and m.startswith(text)
                    ]
                    # This returns modules that have any word of the current
                    # written ones
                    if len(self.matches) == 0:
                        self.matches = [
                            m for m in self.options if "/" in m and text in m
                        ]

                elif line.startswith("set") and "set" in self.options:
                    # This returns options for set command but only when
                    # it's available :D
                    self.matches = [
                        m for m in self.module_options if m.startswith(text)
                    ]
                    if len(self.matches) == 0:
                        # This returns all options if no thing is written after
                        # the set command
                        self.matches = self.module_options
                else:
                    self.matches = [
                        s for s in self.options if s.startswith(text) and "/" not in s
                    ]
                    if len(self.matches) == 0:
                        possible_matches = [s for s in self.options if "/" not in s]
                        wanted = []
                        for i in reversed(
                            range(1, 5)
                        ):  # Fixing typos to return matches if there's no matches :D
                            wanted.extend(
                                [
                                    s
                                    for s in possible_matches
                                    if (s[:i] == text[:i] and s not in wanted)
                                ]
                            )
                            if len(wanted) > 0:
                                self.matches = sorted(wanted)
                                break
                        self.matches = sorted(wanted)
            else:
                line = readline.get_line_buffer()
                if line.startswith("use "):
                    # This works if there's no word typed but use command was
                    # typed before
                    self.matches = [m for m in self.options if "/" in m]
                elif line.startswith("set") and "set" in self.options:
                    self.matches = self.module_options
                else:
                    self.matches = [m for m in self.options if "/" not in m]
        try:
            return self.matches[state]
        except IndexError:
            return None


history_file = os.path.join(".autocomplete_history")


def save_history(
    history_file=history_file,
):  # So you can use the up key to access the previous session commands
    try:
        readline.write_history_file(history_file)
    except (IOError, AttributeError):
        pass  # Non-fatal if history can't be saved or readline unavailable


def Input_completer(keywords):
    completer = MyCompleter(keywords)
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
            readline.set_history_length(20)
        except (IOError, FileNotFoundError):
            pass  # Non-fatal if history can't be read
    readline.set_completer_delims(" ")
    atexit.register(save_history)
