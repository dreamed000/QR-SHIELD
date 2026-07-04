#!/usr/bin/env python3
# QR Shield application orchestration and CLI entrypoint
import argparse
import os
import sys

from core import Cli, Settings, db, ui, utils


class QRShieldApp:
    def __init__(self):
        self.settings = Settings

    def parse_args(self, argv=None):
        parser = argparse.ArgumentParser(prog="qrshield")
        parser.add_argument(
            "-r", metavar="", help="Execute a resource file (history file)."
        )
        parser.add_argument(
            "-x", metavar="", help="Execute a specific command (use ; for multiples)."
        )
        parser.add_argument("--debug", action="store_true", help="Enable debug mode.")
        parser.add_argument(
            "--dev", action="store_true", help="Enable development mode."
        )
        parser.add_argument(
            "--verbose", action="store_true", help="Enable verbose mode."
        )
        parser.add_argument("-q", action="store_true", help="Quit mode (no banner).")
        return parser.parse_args(argv)

    def run(self, argv=None):
        args = self.parse_args(argv)
        self.settings.path = os.path.abspath(os.getcwd())
        self.settings.debug = args.debug
        self.settings.development = args.dev
        self.settings.verbose = args.verbose

        if not args.q:
            ui.clear_screen()
            utils.banner(db.index_modules())

        if args.x:
            for command in args.x.split(";"):
                if command.strip():
                    Cli.start(command.strip())
            Cli.start()
        elif args.r:
            try:
                with open(args.r, "r", encoding="utf-8") as resource_file:
                    for line in resource_file:
                        line = line.strip()
                        if line and not line.startswith("#"):
                            Cli.start(line)
                Cli.start()
            except FileNotFoundError:
                ui.error(f"Resource file not found: {args.r}")
                sys.exit(1)
            except IOError as io_err:
                ui.error(f"Error reading resource file: {io_err}")
                if self.settings.debug:
                    import traceback

                    traceback.print_exc()
                sys.exit(1)
            except Exception as exc:
                ui.error(f"Unexpected error processing resource file: {exc}")
                if self.settings.debug:
                    import traceback

                    traceback.print_exc()
                sys.exit(1)
        else:
            Cli.start()

        sys.exit(0)


def main():
    QRShieldApp().run()
