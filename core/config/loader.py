from .models import AppConfig


def load_settings() -> AppConfig:
    """Return an AppConfig instance.

    This loader function is intentionally simple and returns the default
    configuration. It centralizes future loading behavior (env, files).
    """
    return AppConfig()
