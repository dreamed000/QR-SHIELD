# -*- coding: utf-8 -*-
# Signal QR-session grabber
# Selectors based on Signal Desktop Web (signal.me/#p/ linked-devices QR flow, 2025)
from core.module_utils import types


class info:
    author = "Puneet Chandra Chaudhary - D0C70R"
    short_description = "Signal QR-sessions grabber and controller"
    full_description = None


class execution:
    module_type = types.grabber
    name = "signal"
    url = "https://signal.me/#p/linked-devices"
    session_type = "localstorage"

    # =========================================================================
    # QR CODE IMAGE XPATHS
    # =========================================================================
    # Signal's linked-devices QR page renders the QR code as a <canvas> element
    # inside a React component.  The canvas is the only one on the page and
    # lives inside a wrapper with a data-testid or class containing "qr".
    #
    # Strategy (most-specific → most-generic):
    #   1. data-testid on canvas or wrapper
    #   2. class name match on wrapper
    #   3. Broad canvas fallback (only canvas on page)
    # =========================================================================

    # --- Primary: canvas with data-testid="qr-canvas" (Signal ≥ 7.x) -------
    image_xpath = '//canvas[@data-testid="qr-canvas"]'

    # --- Alt 1: first canvas inside a div whose class contains "qr" ---------
    image_xpath_alt1 = (
        '//div[contains(@class,"qr") or contains(@class,"Qr") or contains(@class,"QR")]'
        + "//canvas"
    )

    # --- Alt 2: canvas inside the link-a-device / install panel -------------
    image_xpath_alt2 = (
        '//div[contains(@class,"install") or contains(@class,"Install")]' + "//canvas"
    )

    # --- Alt 3: any canvas not inside header/footer (broadest fallback) -----
    image_xpath_alt3 = (
        "//canvas[not(ancestor::header) and not(ancestor::footer) "
        "and not(ancestor::nav)]"
    )

    # --- Alt 4: canvas with aria-label mentioning QR ------------------------
    image_xpath_alt4 = (
        '//canvas[contains(@aria-label,"QR") or contains(@aria-label,"qr")]'
    )

    # =========================================================================
    # QR RELOAD / REFRESH BUTTON XPATHS
    # =========================================================================
    # Signal shows a "QR code expired — click to refresh" overlay after ~60 s.
    # =========================================================================

    img_reload_button = (
        '//button[contains(@data-testid,"refresh") or contains(@data-testid,"reload")]'
    )
    img_reload_btn_alt = (
        '//button[contains(normalize-space(.),"Refresh") '
        'or contains(normalize-space(.),"Reload")]'
    )
    img_reload_btn_alt2 = (
        '//button[contains(@aria-label,"Refresh") or contains(@aria-label,"refresh")]'
    )
    img_reload_btn_alt3 = None

    # =========================================================================
    # SESSION / LOGIN SUCCESS DETECTION XPATHS
    # =========================================================================
    # After QR scan, Signal transitions to a "Device linked" confirmation page
    # or, in some flows, directly into a chat list view.
    #
    # Primary: "Device linked" / "Linked" success banner
    # Alt 1: "Open Signal" or redirect CTA button shown post-scan
    # Alt 2: a conversation list / inbox container (full web client)
    # =========================================================================

    # Primary: success confirmation heading / banner
    change_identifier = (
        '//*[contains(normalize-space(.),"linked") '
        'or contains(normalize-space(.),"Linked") '
        'or contains(normalize-space(.),"Device added")]'
    )

    # Alt 1: CTA button that appears only after successful linking
    change_id_android = (
        '//a[contains(@href,"signal://") or contains(normalize-space(.),"Open Signal")]'
    )

    # Alt 2: conversation list (if Signal launches a web chat view post-scan)
    change_id_ios = '//div[@role="list" and contains(@aria-label,"Chats")]'

    # Alt 3: any element confirming device registration complete
    change_id_alt = (
        '//*[contains(@class,"success") or contains(@class,"linked") '
        'or contains(@data-testid,"success")]'
    )

    # =========================================================================
    # SELECTOR MAINTENANCE NOTES
    # =========================================================================
    # If ALL selectors fail after a Signal update:
    #
    # 1. Open https://signal.me/#p/linked-devices in your browser.
    # 2. Open DevTools → Elements and locate the QR <canvas>.
    # 3. Inspect the nearest ancestor for data-testid, class, or aria-* attrs.
    # 4. Update image_xpath with the new selector, e.g.:
    #       '//canvas[@data-testid="<new-testid>"]'
    # 5. For session detection, after a test-scan look for elements that only
    #    appear on the success/linked confirmation screen.
    #
    # Known Signal DOM attributes (2025):
    #   QR canvas:         canvas[data-testid="qr-canvas"]
    #   QR wrapper:        div.qr* / div.QrCode*
    #   Success heading:   *[text contains "linked" / "Device added"]
    #   Open Signal CTA:   a[href^="signal://"]
    # =========================================================================
