# -*- coding: utf-8 -*-
# WhatsApp QR-session grabber
# Updated selectors: June 2025 – WhatsApp Web v2.3000+ DOM
from core.module_utils import types


class info:
    author = "Puneet Chandra Chaudhary - D0C70R"
    short_description = "Whatsapp QR-sessions grabber and controller"
    full_description = None


class execution:
    module_type = types.grabber
    name = "whatsapp"
    url = "https://web.whatsapp.com"
    session_type = "profile"

    # =========================================================================
    # QR CODE CANVAS XPATHS
    # =========================================================================
    # WhatsApp Web renders the QR as a <canvas> inside a <div> that has
    # data-ref / data-testid attributes.  The structure has changed several
    # times; we keep a cascade from most-specific to most-generic so at least
    # one survives a WhatsApp DOM update.
    #
    # Strategy:
    #   1. data-testid attribute selectors  (most stable across updates)
    #   2. aria-label / role selectors       (accessibility tree – very stable)
    #   3. Structural canvas fallback        (last resort)
    # =========================================================================

    # --- Primary: data-testid on the canvas itself (WA ≥ 2.2346) ----------
    image_xpath = '//canvas[@data-testid="qrcode"]'

    # --- Alt 1: data-testid on the wrapper div, then first canvas child ----
    image_xpath_alt1 = '//div[@data-testid="qrcode"]//canvas'

    # --- Alt 2: aria-label contains "QR" on a canvas or its parent --------
    image_xpath_alt2 = (
        '//canvas[contains(@aria-label,"QR") or contains(@aria-label,"qr")]'
    )

    # --- Alt 3: any canvas inside the dedicated QR landing section ---------
    #     WhatsApp wraps the QR login area in a <div> with id="app" >
    #     multiple nested divs.  The landing div often has data-animate-modal
    #     or a class that changes, but the QR canvas is always its only canvas.
    image_xpath_alt3 = (
        '//div[@id="app"]'
        "/div/div/div/div/div/div/div"
        "/canvas[not(ancestor::header)]"
    )

    # --- Alt 4: broadest possible canvas catch (slow but reliable fallback) -
    image_xpath_alt4 = "//canvas[not(ancestor::header) and not(ancestor::footer)]"

    # =========================================================================
    # QR RELOAD / REFRESH BUTTON XPATHS
    # =========================================================================
    # WhatsApp shows a "Click to reload QR code" overlay when the QR expires.
    # The button/div that triggers the refresh has changed testid names; keep
    # several variants.
    # =========================================================================

    img_reload_button = '//button[@data-testid="qrcode-refresh"]'
    img_reload_btn_alt = '//div[@data-testid="qrcode-refresh"]'
    img_reload_btn_alt2 = (
        '//button[contains(@aria-label,"Reload") or contains(@aria-label,"reload")]'
    )
    img_reload_btn_alt3 = '//span[contains(@data-icon,"refresh") or contains(@data-icon,"reload")]/ancestor::button[1]'

    # =========================================================================
    # SESSION / LOGIN SUCCESS DETECTION XPATHS
    # =========================================================================
    # After the user scans the QR code WhatsApp transitions to the main chat
    # UI.  We detect this by looking for elements that only appear post-login.
    #
    # Most reliable signal: the header toolbar that contains the user avatar.
    # Second signal: the main chat panel or the new-chat icon.
    # =========================================================================

    # Primary: side-panel header – always present after login
    change_identifier = '//header[@data-testid="chatlist-header"]'

    # Alt 1: user avatar button in the top-left corner
    change_id_android = '//button[@data-testid="menu-bar-menu-icon"]'

    # Alt 2: "New chat" compose button (only visible when logged in)
    change_id_ios = '//button[@data-testid="compose-btn"]'

    # Alt 3: the search box in the sidebar (always present post-login)
    change_id_alt = '//div[@data-testid="chat-list-search"]'

    # =========================================================================
    # SELECTOR MAINTENANCE NOTES
    # =========================================================================
    # If ALL selectors fail after a WhatsApp Web update:
    #
    # 1. Open https://web.whatsapp.com in your browser (not headless).
    # 2. Open DevTools → Elements and locate the QR <canvas>.
    # 3. Look for the nearest ancestor that has a data-testid, aria-label,
    #    or id attribute – these are far more stable than positional XPaths.
    # 4. Update image_xpath with the new testid, e.g.:
    #       '//canvas[@data-testid="<new-testid>"]'
    # 5. For the reload button, right-click the "Reload QR" overlay and
    #    inspect – find its data-testid or aria-label.
    # 6. For session detection, inspect the header bar after login.
    #
    # data-testid values used by WhatsApp Web (as of 2025-26):
    #   QR canvas:           qrcode
    #   QR wrapper div:      qrcode
    #   Reload button:       qrcode-refresh
    #   Chat-list header:    chatlist-header
    #   Compose/new-chat:    compose-btn
    #   Chat search:         chat-list-search
    # =========================================================================
