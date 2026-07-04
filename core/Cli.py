#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""QR Shield CLI and command dispatcher.

Provides the `QRShieldCLI` class which implements the interactive command
loop and command handlers used by the framework.
"""

import argparse
import importlib
import json
import os
import shlex
import shutil
import sys
import time
import traceback

# QR Shield CLI and command dispatcher
from typing import Any, Optional, cast

from core import Settings, db, ui, utils
from core.color import Bold, G, Y, end

all_keywords = [
    "help",
    "?",
    "os",
    "banner",
    "exit",
    "quit",
    "list",
    "show",
    "use",
    "info",
    "previous",
    "search",
    "sessions",
    "jobs",
    "database",
    "debug",
    "dev",
    "verbose",
    "reload",
    "refresh",
    "history",
    "makerc",
    "resource",
    "report",
    "back",
]
modules = db.index_modules()

help_msg = end + G + """
General commands
=================
  help/?              Show this help menu.
  os <command>        Execute a system command without closing the framework.
  banner              Display the QR Shield banner.
  history             Print the command history.
  makerc              Save entered commands to a file.
  resource <file>     Run commands from a file.
  exit/quit           Exit the framework.

Core commands
=============
  database            Show core database version and update the framework.
  debug               Toggle debug mode.
  dev                 Toggle development mode.
  verbose             Toggle verbose mode.
  reload/refresh      Reload the module database.

Sessions commands
=================
  sessions (-h)       Manage saved sessions.
  jobs (-h)           List and terminate running jobs.
""" + end

module_help = end + G + """
Module commands
===============
  list/show           List available modules.
  use <module>        Select a module to run.
  info <module>       Show information about a module.
  search <text>       Search modules by text.
  previous            Switch to the previously used module.
  back                Exit module context.
  options             Show current module options.
  set <opt> <value>   Set a module option.
  run                 Execute the selected module.
""" + end

sessions_parser = argparse.ArgumentParser(prog="sessions", add_help=False)
sessions_parser.add_argument("-h", action="store_true", help="Show this help message.")
sessions_parser.add_argument(
    "-l", action="store_true", help="List all captured sessions."
)
sessions_parser.add_argument(
    "-K", action="store_true", help="Remove all captured sessions."
)
sessions_parser.add_argument(
    "-s", metavar="", help="Search for sessions with a specific type."
)
sessions_parser.add_argument(
    "-k", metavar="", help="Remove a specific captured session by ID"
)
sessions_parser.add_argument(
    "-i", metavar="", help="Interact with a captured session by ID."
)


class QRShieldCLI:
    """Interactive command-line interface for QR Shield.

    The CLI exposes command handlers prefixed with `command_` which are
    dispatched from the interactive loop or when used programmatically.
    """

    def __init__(self) -> None:
        self.modules = modules
        self.current_prompt = ""
        self.module_context: Optional[Any] = None
        self.all_keywords: list[str] = []
        self.refresh_completion()
        self.update_prompt()

    def refresh_completion(self):
        self.modules = db.index_modules()
        self.all_keywords = list(all_keywords)
        ui.init_readline(self.all_keywords + self.modules)

    def update_prompt(self):
        self.current_prompt = ui.format_prompt(
            Settings.name, Settings.debug, Settings.development, Settings.verbose
        )

    def _load_module_context(self) -> Optional[Any]:
        if self.module_context is None:
            try:
                self.module_context = cast(Any, importlib.import_module("core.module"))
                if hasattr(self.module_context, "context") and hasattr(
                    self.module_context.context, "register_cli_dispatcher"
                ):
                    self.module_context.context.register_cli_dispatcher(
                        general_commands
                    )
            except Exception as exc:
                ui.error(f"Unable to load module context: {exc}")
                if Settings.debug:
                    traceback.print_exc()
                return None
        return self.module_context

    def start(self, rc: Optional[str] = None) -> None:
        if rc:
            for command in ui.split_commands(rc):
                if command:
                    ui.status(f"\n{Settings.name}{G} > {end}{command}")
                    self.execute(command)
                    time.sleep(0.2)
            return

        while True:
            try:
                self.update_prompt()
                raw_line = input(self.current_prompt)
            except KeyboardInterrupt:
                ui.info("")
                ui.warning("KeyboardInterrupt - use exit command.")
                continue
            except EOFError:
                ui.info("EOF received. Exiting.")
                self.shutdown()

            if not raw_line or not raw_line.strip():
                continue

            for command in ui.split_commands(raw_line):
                if command:
                    self.execute(command)

    def execute(self, command_line: str) -> None:
        command_line = command_line.strip()
        if not command_line or command_line.startswith("#"):
            return

        if Settings.running_module:
            module_context = self._load_module_context()
            if module_context is None:
                ui.error("Module context unavailable.")
                return
            module_context.handle(command_line)
            Settings.update_history(command_line)
            return

        try:
            parts = shlex.split(command_line)
        except ValueError as exc:
            ui.error(f"Invalid command syntax: {exc}")
            return

        if not parts:
            return

        command = parts[0].lower()
        args = " ".join(parts[1:])
        handler = getattr(self, f"command_{command}", None)

        if callable(handler):
            handler(args)
            Settings.update_history(command_line)
        else:
            ui.error(f"{command} is not recognized as an internal command!")
            wanted = utils.grab_wanted(command, self.all_keywords + self.modules)
            if wanted:
                ui.status("Maybe you meant: " + wanted)
            ui.status("Type help or ? to learn more.")

    def command_help(self, text=False):
        ui.info(help_msg + module_help)

    def command_banner(self, text=False):
        utils.banner(self.modules)

    def command_history(self, text=False):
        if not Settings.history:
            ui.info("No history available.")
            return
        for entry in Settings.history:
            ui.info(entry)

    def command_makerc(self, text=False):
        file_name = text.strip() if text else "history.txt"
        try:
            with open(file_name, "w", encoding="utf-8") as f:
                for line in Settings.history:
                    f.write(line + "\n")
            ui.status(f"Command history saved to {file_name}")
        except Exception as exc:
            ui.error(f"Unable to save history: {exc}")

    def command_exit(self, text=False):
        self.shutdown()

    def command_quit(self, text=False):
        self.shutdown()

    def command_resource(self, text=False):
        if not text:
            ui.error("Enter a resource file to read!")
            return
        try:
            with open(text, "r", encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith("#"):
                        self.execute(line)
        except Exception:
            ui.error(f"Can't open the specified resource file: {text}")
            if Settings.debug:
                traceback.print_exc()

    def command_info(self, text=False):
        if not text:
            ui.error("You must enter a module to get its information !")
            return
        module_name = text.lower()
        if module_name in self.modules:
            info = db.grab(module_name)
            ui.status(f"      Module : {utils.humanize(module_name)}")
            ui.info(f" Provided by : {info.author}")
            ui.info(f" Description : {info.full_description or info.short_description}")
        else:
            ui.error(module_name + " module not found!")

    def command_reload(self, text=False):
        self.refresh_completion()
        ui.status(f"Database updated! ({len(self.modules)} module(s) loaded now)")

    def command_refresh(self, text=False):
        self.command_reload(text)

    def command_database(self, text=False):
        ui.status("Checking...")
        try:
            with open(
                os.path.join(Settings.path, "core", "Data", "version.txt"),
                encoding="utf-8",
            ) as _vf:
                current_version = _vf.read().strip()
        except Exception as exc:
            ui.error(f"Failed to read local version: {exc}")
            return

        ui.status("Core database " + Y + current_version)
        latest = utils.check_version()
        if latest and latest == current_version:
            ui.status("You are up-to-date!")
        elif not latest:
            ui.error("Error in connection! Check your internet!")
        else:
            ui.error("The latest core database is " + latest)
            ui.status("Updating...")
            try:
                result = __import__("subprocess").run(
                    ["git", "pull"],
                    cwd=Settings.path,
                    capture_output=True,
                    text=True,
                    timeout=30,
                )
                if result.returncode == 0:
                    ui.status("Framework updated successfully!")
                else:
                    ui.error("git pull failed: " + result.stderr.strip())
            except Exception as exc:
                ui.error("git pull failed: " + str(exc))

    def command_exec(self, text=False):
        ui.error("The exec command is disabled for security reasons.")

    def command_eval(self, text=False):
        ui.error("The eval command is disabled for security reasons.")

    def command_report(self, text=False):
        if Settings.debug and Settings.headless_browser:
            for key, browser_data in Settings.headless_browser.browsers.items():
                ui.info("Key: " + str(key))
                ui.info("Data: ")
                ui.info(str(browser_data.get("Controller").capabilities))
                break

    def command_debug(self, text=False):
        Settings.debug = not Settings.debug
        ui.status("Debug mode " + ("enabled!" if Settings.debug else "disabled!"))

    def command_dev(self, text=False):
        Settings.development = not Settings.development
        ui.status(
            "Development mode " + ("enabled!" if Settings.development else "disabled!")
        )

    def command_verbose(self, text=False):
        Settings.verbose = not Settings.verbose
        ui.status("Verbose mode " + ("enabled!" if Settings.verbose else "disabled!"))

    def command_list(self, text=False):
        headers = [G + Bold + "Name" + end, G + Bold + "Description" + end]
        table = []
        for module_name in self.modules:
            info = db.grab(module_name)
            table.append([module_name, info.short_description])
        ui.create_table(headers, table)

    def command_show(self, text=False):
        self.command_list(text)

    def command_search(self, text=False):
        if not text:
            ui.error("You must enter a text to search for !")
            return
        search_text = text.lower()
        headers = [G + Bold + "Name" + end, G + Bold + "Description" + end]
        table = []
        for module_name in self.modules:
            info = db.grab(module_name)
            full_text = " ".join(
                [
                    info.author or "",
                    info.short_description or "",
                    info.full_description or "",
                ]
            ).lower()
            if search_text in full_text:
                table.append([module_name, info.short_description])
        if not table:
            ui.error("No modules found matching the entered text.")
        else:
            ui.create_table(headers, table)

    def command_os(self, text=False):
        if not text:
            ui.error("You must enter a command to execute !")
            return

        try:
            import subprocess

            cmd = shlex.split(text, posix=(os.name != "nt"))
            if not cmd:
                ui.error("Empty command provided.")
                return

            result = subprocess.run(cmd, capture_output=True, text=True, shell=False)
            if result.stdout:
                ui.info(result.stdout.strip())
            if result.stderr:
                ui.error(result.stderr.strip())
        except FileNotFoundError:
            ui.error(f"Command not found: {text.split()[0]}")
        except Exception as exc:
            ui.error(f"Failed to execute command: {exc}")

    def command_use(self, text=False):
        if not text:
            ui.error("You must enter a module to use !")
            return
        module_name = text.lower()
        if module_name not in self.modules:
            if Settings.debug:
                ui.error("Module not found: " + module_name)
                ui.status("Loaded modules: " + ", ".join(self.modules))
            ui.error(module_name + " module not found!")
            return
        if Settings.running_module:
            Settings.update_previous()
        Settings.running_module = module_name
        module_context = self._load_module_context()
        if module_context is None:
            return
        if hasattr(module_context, "Exec"):
            module_context.Exec(self.all_keywords)
        else:
            ui.error(
                "Failed to enter module context: module execution handler "
                "not available."
            )

    def command_sessions(self, text=""):
        sessions_file = os.path.join("sessions", "sessions.json")
        sessions = self._load_sessions(sessions_file)
        if sessions is None:
            return

        try:
            cmd = sessions_parser.parse_args(shlex.split(text) if text else [])
        except SystemExit:
            cmd = sessions_parser.parse_args([])

        if cmd.h:
            ui.info(sessions_parser.format_help())
            return

        if not text or cmd.l:
            self._list_sessions(sessions)
            return

        if cmd.i:
            self._interact_session(cmd.i, sessions)
            return

        if cmd.k:
            self._remove_session(cmd.k, sessions_file, sessions)
            return

        if cmd.s:
            self._search_sessions(cmd.s, sessions)
            return

        if cmd.K:
            self._remove_all_sessions(sessions_file, sessions)
            return

    def _load_sessions(self, sessions_file):
        if not os.path.exists(sessions_file):
            ui.error(f"Sessions file not found: {sessions_file}")
            return None
        try:
            with open(sessions_file, "r", encoding="utf-8") as f:
                return json.load(f)
        except json.JSONDecodeError:
            ui.error("Sessions file is corrupted. Cannot parse JSON.")
            if Settings.debug:
                traceback.print_exc()
            return None
        except Exception as exc:
            ui.error(f"Failed to load sessions file: {exc}")
            if Settings.debug:
                traceback.print_exc()
            return None

    def _list_sessions(self, sessions):
        if not sessions:
            ui.error("No captured sessions.")
            return
        headers = [
            G + Bold + "ID" + end,
            G + Bold + "Module name" + end,
            G + Bold + "Captured on" + end,
        ]
        rows = []
        for session_id, data in sessions.items():
            session_path = data.get("session_path", "unknown")
            timestamp = os.path.basename(session_path.rstrip('/\\"')).replace(
                ".session", ""
            )
            rows.append([session_id, data.get("name", "unknown"), timestamp])
        ui.create_table(headers, rows)

    def _interact_session(self, session_id, sessions):
        if session_id not in sessions:
            ui.error("Invalid session ID!")
            return
        session_data = sessions[session_id]
        session_type = session_data.get("session_type", "profile")
        session_path = session_data.get("session_path")
        web_url = session_data.get("web_url", "unknown")

        if not session_path:
            ui.error(
                f"Session {session_id}: Missing session_path field in sessions.json"
            )
            return
        if not web_url:
            ui.error(f"Session {session_id}: Missing web_url field in sessions.json")
            return

        if not Settings.visible_browser:
            import core.browser as browser

            Settings.visible_browser = browser.visible_browsers()

        ui.status(f"Starting interaction with session ({session_id})...")
        ui.status(f"Session Type: {session_type}")
        ui.status(f"Target URL: {web_url}")

        try:
            if session_type == "localStorage":
                ui.status("Loading localStorage session...")
                Settings.visible_browser.load_localstorage(session_id)
            elif session_type == "cookies":
                ui.status("Loading cookie-based session...")
                Settings.visible_browser.load_cookie(session_id)
            else:
                ui.status("Loading Firefox profile session...")
                Settings.visible_browser.load_profile(session_id)
        except Exception as exc:
            ui.error(f"Failed to load session {session_id}: {exc}")
            if Settings.debug:
                traceback.print_exc()
            return

        if not getattr(Settings.visible_browser, "browsers", None):
            ui.error(f"Failed to load session {session_id}")
            return

        ui.status(f"✓ Browser window should now be open with session {session_id}")

    def _remove_session(self, session_id, sessions_file, sessions):
        if session_id not in sessions:
            ui.error("Invalid session ID!")
            return
        session_file = sessions[session_id].get("session_path")
        try:
            if session_file and os.path.exists(session_file):
                if os.path.isdir(session_file):
                    shutil.rmtree(session_file)
                else:
                    os.remove(session_file)
            sessions.pop(session_id)
            with open(sessions_file, "w", encoding="utf-8") as f:
                json.dump(sessions, f, indent=2)
            ui.status(f"Session ({session_id}) removed!")
        except Exception as exc:
            ui.error(f"Failed to remove session {session_id}: {exc}")
            if Settings.debug:
                traceback.print_exc()

    def _search_sessions(self, session_type, sessions):
        matching = {
            sid: info
            for sid, info in sessions.items()
            if info.get("name") == session_type
        }
        if not matching:
            ui.error(f"No sessions found with type '{session_type}'")
            return
        headers = [G + Bold + "ID" + end, G + Bold + "Captured on" + end]
        rows = []
        for session_id, info in matching.items():
            session_path = info.get("session_path", "unknown")
            timestamp = os.path.basename(session_path.rstrip('/\\"')).replace(
                ".session", ""
            )
            rows.append([session_id, timestamp])
        ui.create_table(headers, rows)

    def _remove_all_sessions(self, sessions_file, sessions):
        if not sessions:
            ui.error("No captured sessions.")
            return
        removed = 0
        for sid, info in list(sessions.items()):
            session_file = info.get("session_path")
            if session_file and os.path.exists(session_file):
                try:
                    if os.path.isdir(session_file):
                        shutil.rmtree(session_file)
                    else:
                        os.remove(session_file)
                    removed += 1
                except Exception as exc:
                    if Settings.debug:
                        ui.warning(f"Could not remove {session_file}: {exc}")
        with open(sessions_file, "w", encoding="utf-8") as f:
            json.dump({}, f, indent=2)
        ui.status(f"All captured sessions removed! ({removed} items deleted)")

    def command_jobs(self, text=False):
        if text == "-h":
            print("""
usage: jobs [-h] [-l] [-K] [-k]

optional arguments:
  -h   Show this help message.
  -l   List all running jobs.
  -K   Terminate all running jobs.
  -k   Terminate jobs by job ID or module name
""")
            return

        if not Settings.headless_browser or not getattr(
            Settings.headless_browser, "browsers", {}
        ):
            ui.error("No active jobs.")
            return

        parts = shlex.split(text) if text else []
        if not parts or parts[0] == "-l":
            headers = [
                G + Bold + "ID" + end,
                G + Bold + "Module name" + end,
                G + Bold + "Serving on" + end,
            ]
            rows = []
            for module_name, data in Settings.headless_browser.browsers.items():
                uri = f"{data.get('host')}:{data.get('port')}"
                session_id = "(closed)"
                try:
                    session_id = data["Controller"].session_id
                except Exception:
                    pass
                rows.append([session_id, module_name, uri])
            ui.create_table(headers, rows)
            return

        if parts[0] == "-K":
            Settings.headless_browser.close_all()
            Settings.headless_browser = None
            ui.status("All jobs terminated successfully!")
            return

        if parts[0] == "-k":
            if len(parts) < 2:
                ui.error("Enter a job ID/module name to terminate!")
                return
            target = parts[1]
            for module_name, data in list(Settings.headless_browser.browsers.items()):
                ctrl = data.get("Controller")
                if (
                    ctrl and getattr(ctrl, "session_id", None) == target
                ) or module_name == target:
                    Settings.headless_browser.close_job(module_name)
                    ui.status("Job terminated successfully!")
                    return
            ui.error("Job not found!")
            return

        ui.error("Invalid option!")

    def command_previous(self, text=False):
        if Settings.previous:
            prev = Settings.previous.pop(-1)
            self.command_use(prev)
        else:
            ui.error("You haven't used any modules yet!")

    def command_back(self, text=False):
        Settings.update_previous()
        Settings.running_module = False
        Settings.reset_name()
        self.refresh_completion()

    def shutdown(self):
        if Settings.headless_browser:
            Settings.headless_browser.close_all()
            Settings.headless_browser = None
        if Settings.visible_browser:
            Settings.visible_browser.close_all()
            Settings.visible_browser = None
        sys.exit(0)


cli = QRShieldCLI()

# Compatibility wrapper for module handlers


def general_commands(
    command: str, args: Optional[str] = None, full_help: Optional[str] = module_help
) -> bool:
    """Compatibility wrapper to call CLI command handlers from modules.

    Returns True if the command was handled, False otherwise.
    """
    handler = getattr(cli, f"command_{command}", None)
    if callable(handler):
        handler(args)
        return True
    return False


def start(rc: Optional[str] = None) -> None:
    return cli.start(rc)
