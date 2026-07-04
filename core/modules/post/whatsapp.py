# -*- coding: utf-8 -*-
# WhatsApp post-exploitation module
# Operates on a previously captured WhatsApp profile session.
from core.color import error, status
from core.module_utils import load_post_session, resolve_post_session, types


class info:
    author = "Puneet Chandra Chaudhary - D0C70R"
    short_description = "WhatsApp post-session interaction (open captured session)"
    full_description = (
        "Loads a previously captured WhatsApp session (profile type) into a "
        "visible Firefox browser window so you can interact with it. "
        "Set session_id to the ID shown by 'sessions -l'."
    )


class execution:
    module_type = types.post
    name = "whatsapp"
    url = "https://web.whatsapp.com"
    session_type = "profile"

    # post modules don't need grabber XPaths — only session_id option matters
    # (injected via types.post.options)

    @staticmethod
    def run(global_options, visible_browser):
        """Open the captured WhatsApp session in a visible browser window."""
        try:
            session_id = resolve_post_session(
                global_options, module_name="whatsapp", session_type="profile"
            )
        except Exception as exc:
            error(str(exc))
            return

        status(f"Loading WhatsApp session [{session_id}]...")
        load_post_session("profile", session_id, visible_browser)
