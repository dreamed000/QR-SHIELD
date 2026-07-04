#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# QR Shield module execution and context handling
import copy
import traceback
from typing import Any, Optional

from core import Settings, db, utils
from core.color import B, Bold, G, end, error, status
from core.module_utils import types
from core.plugin_manager import load_module

# core.browser depends on optional external packages (selenium). Import
# it lazily/optionally so tests and environments without selenium can still
# import this module and register the CLI dispatcher.
browser: Optional[Any] = None
try:
    import core.browser as browser
except Exception:
    browser = None

module_help = end + G + """

Module commands
===============
    Command               Description
    ----------            --------------
    list/show             List modules you can use.
    options               Displays options for the current module.
    set                   Sets a context-specific variable to a value.
    run                   Launch the current module.
    use     <module>      Use an available module.
    info    <module>      Get information about an available module.
    search  <text>        Search for a module by a text in its name or description.
    previous              Sets the previously loaded module as the current module.
    back                  Move back from the current context.
""" + end

_BASE_MODULE_KEYWORDS = ["options", "set", "run", "back", "close"]


class ModuleContext:
    def __init__(self):
        self.global_options = {}
        self.module_keywords = list(_BASE_MODULE_KEYWORDS)
        self.cli_keywords = []
        self.modules = db.index_modules()
        self.cli_command_dispatcher = None

    def register_cli_dispatcher(self, dispatcher):
        self.cli_command_dispatcher = dispatcher

    def exec(self, all_keywords):
        self.module_keywords = list(_BASE_MODULE_KEYWORDS) + list(all_keywords)
        self.cli_keywords = all_keywords
        module = load_module(Settings.running_module, development=Settings.development)
        self.global_options = copy.deepcopy(
            getattr(module, "execution").module_type.options
        )
        if getattr(utils, "readline", None):
            utils.Input_completer(self.module_keywords + self.modules)
        Settings.add_module(Settings.running_module)

    def handle(self, command_text):
        if not command_text or not command_text.strip():
            return

        command_text = command_text.strip()
        if command_text.startswith("#"):
            return

        parts = command_text.split()
        if not parts:
            return

        head = parts[0].lower()
        args = " ".join(parts[1:])

        try:
            local_handler = getattr(self, f"command_{head}", None)
            if callable(local_handler):
                local_handler(args)
                Settings.update_history(command_text)
                return

            if callable(self.cli_command_dispatcher) and self.cli_command_dispatcher(
                head, args, module_help
            ):
                return

            error(head + " is not recognized as an internal command !")
            wanted = utils.grab_wanted(head, self.module_keywords)
            if wanted:
                status("Maybe you meant : " + wanted)
            status("Type help or ? to learn more..")
        except Exception as exc:
            if Settings.debug:
                error("Exception -> " + str(exc))
                status("    Input -> " + str(command_text))
                status("Trackback -> ")
                traceback.print_exc()
            else:
                error(head + " is not recognized as an internal command !")
            status("Type help or ? to learn more..")

    def command_options(self, text=False):
        try:
            options = self.global_options
            headers = [
                B + Bold + "Name",
                "Current value",
                "Required",
                "Description" + end,
            ]
            names = list(options.keys())
            values = utils.my_map(lambda x: str(options[x][2]), names)
            required = utils.my_map(lambda x: ["No", "Yes"][options[x][0]], names)
            description = utils.my_map(lambda x: options[x][1], names)
            rows = [
                [names[row], values[row], required[row], description[row]]
                for row in range(len(names))
            ]
            utils.create_table(headers, rows)
        except Exception as exc:
            if Settings.debug:
                error("Error in finding options! ")
                error("Exception -> " + str(exc))
                status("   Module -> " + str(Settings.running_module))
                status("Trackback -> ")
                traceback.print_exc()
            else:
                error("Unknown error! enable debug mode to more details")

    def is_option(self, option):
        try:
            return [self.global_options[option.lower()][2]]
        except Exception:
            return False

    def validate_option_value(self, option_name, new_value):
        option_name_lower = option_name.lower()
        if option_name_lower == "port":
            try:
                port_num = int(new_value)
                if port_num < 1 or port_num > 65535:
                    error(f"Port must be between 1 and 65535, got {port_num}")
                    return False
            except ValueError:
                error(f"Port must be a valid integer, got '{new_value}'")
                return False
        elif option_name_lower == "host":
            if not new_value or not new_value.strip():
                error("Host cannot be empty")
                return False
        elif option_name_lower == "session_id":
            if not new_value or not new_value.strip():
                error("Session ID cannot be empty")
                return False
        return True

    def change_value(self, option, new_value):
        self.global_options[option.lower()][2] = new_value

    def command_set(self, opt=False):
        if not opt or not opt.strip():
            error("You must type an option first !")
            return

        if len(opt.split(" ")) < 2 and "=" not in opt:
            error("You must type a new value to the option !")
            return

        split_char = " "
        if "=" in opt:
            split_char = "="

        splitted = opt.split(split_char, 1)
        if len(splitted) < 2:
            error("Invalid option format!")
            return

        option_name = splitted[0].strip()
        new_value = splitted[1].strip()

        value_check = self.is_option(option_name)
        if isinstance(value_check, list):
            if isinstance(value_check[0], bool):
                self.change_value(option_name, not value_check[0])
                status(option_name + " => " + str(not value_check[0]))
            else:
                if not self.validate_option_value(option_name, new_value):
                    return
                self.change_value(option_name, new_value)
                status(option_name + " => " + new_value)
        else:
            error("Invalid option!")

    def command_run(self, text=False):
        missing_options = [
            key
            for key, value in self.global_options.items()
            if value[0] == 1 and not str(value[2]).strip()
        ]
        if missing_options:
            error("Missing required option(s): " + ", ".join(missing_options))
            return

        for key, value in self.global_options.items():
            current_value = str(value[2]).strip()
            if current_value and not self.validate_option_value(key, current_value):
                return

        try:
            module = load_module(
                Settings.running_module, development=Settings.development
            )
            exec_info = getattr(module, "execution")
        except Exception as exc:
            if Settings.debug:
                error(f"Failed to load module: {str(exc)}")
                traceback.print_exc()
            else:
                error("Failed to load module. Enable debug mode for details.")
            return

        current_browser = {"Status": "Ok"}
        try:
            if not Settings.headless_browser:
                if browser is None:
                    error(
                        "Browser support is unavailable "
                        "(missing optional dependencies)."
                    )
                    return
                Settings.headless_browser = browser.headless_browsers()
            current_browser = Settings.headless_browser.new_session(
                exec_info.name,
                exec_info.url,
                self.global_options["useragent"][2],
            )
        except Exception as exc:
            if Settings.debug:
                error(f"Browser session error: {str(exc)}")
                traceback.print_exc()
            else:
                error("Failed to initialize browser. Check your Firefox installation.")
            return

        status_map = {
            "Duplicate": "Module already running!",
            "NoBrowser": (
                "Firefox not found. Please install Firefox to use this module."
            ),
            "Failed": "Failed to open Firefox. Check your installation.",
            "Invalid useragent": (
                "Invalid useragent option. Use (default), (random), "
                "or a custom string."
            ),
        }
        current_status = current_browser.get("Status")
        if current_status in status_map:
            error(status_map[current_status])
            return

        try:
            if exec_info.module_type == types.grabber:
                if Settings.development:
                    status("Grabber module detected!")
                image_args = [
                    getattr(exec_info, key, None)
                    for key in (
                        "image_xpath",
                        "image_xpath_alt1",
                        "image_xpath_alt2",
                        "image_xpath_alt3",
                        "image_xpath_alt4",
                    )
                ]
                change_ids = [
                    getattr(exec_info, key, None)
                    for key in (
                        "change_identifier",
                        "change_id_android",
                        "change_id_ios",
                        "change_id_alt",
                    )
                ]
                reload_buttons = [
                    getattr(exec_info, key, None)
                    for key in (
                        "img_reload_button",
                        "img_reload_btn_alt",
                        "img_reload_btn_alt2",
                        "img_reload_btn_alt3",
                    )
                ]

                Settings.headless_browser.website_qr(
                    exec_info.name, image_args[0], *image_args[1:]
                )
                Settings.headless_browser.create_listener(
                    exec_info.name,
                    change_ids[0],
                    exec_info.session_type,
                    *change_ids[1:],
                )
                if reload_buttons[0]:
                    Settings.headless_browser.check_img(
                        exec_info.name,
                        reload_buttons[0],
                        reload_buttons[1],
                        reload_buttons[2],
                        reload_buttons[3],
                    )
                Settings.headless_browser.serve_module(
                    exec_info.name,
                    self.global_options["host"][2],
                    int(self.global_options["port"][2]),
                )
            elif exec_info.module_type == types.post:
                if Settings.development:
                    status("Post module detected!")
                if not Settings.visible_browser:
                    Settings.visible_browser = browser.visible_browsers()
                try:
                    exec_info.run(self.global_options, Settings.visible_browser)
                except AttributeError:
                    error("Post module does not implement a run() method.")
                    return
                except Exception as exc:
                    if Settings.debug:
                        error(f"Post module execution failed: {str(exc)}")
                        traceback.print_exc()
                    else:
                        error(
                            "Failed to run post module. Enable debug mode for details."
                        )
                    return
                return
            else:
                error("Error running module. Enable debug mode for details.")
        except Exception as exc:
            if Settings.debug:
                error(f"Error running module: {str(exc)}")
                traceback.print_exc()
            else:
                error("Error running module. Enable debug mode for details.")

    def command_close(self, text=False):
        if Settings.headless_browser:
            Settings.headless_browser.close_all()
            Settings.headless_browser = None

    def command_back(self, text=False):
        Settings.update_previous()
        Settings.running_module = False
        Settings.reset_name()
        if getattr(utils, "readline", None):
            utils.Input_completer(self.cli_keywords + self.modules)


context = ModuleContext()

# Compatibility wrappers
Exec = context.exec
handle = context.handle
command_options = context.command_options
command_set = context.command_set
command_run = context.command_run
command_close = context.command_close
command_back = context.command_back
