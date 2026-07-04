from dataclasses import dataclass, field
from typing import Any

from ..color import R, W, end, underline


@dataclass
class AppConfig:
    """Application configuration dataclass for QR Shield.

    Replaces legacy `AppSettings` while preserving the same attributes
    and method names for backward compatibility.
    """

    path: str = ""
    debug: bool = False
    development: bool = False
    verbose: bool = False
    running_module: Any = None
    headless_browser: Any = None
    visible_browser: Any = None
    previous: list[str] = field(default_factory=list)
    history: list[str] = field(default_factory=list)
    name: str = W + underline + "QR-SHIELD" + end

    def update_history(self, command: str) -> None:
        self.history.append(command)

    def update_previous(self) -> None:
        self.previous.append(self.running_module)

    def add_module(self, module_name: str) -> None:
        self.name = (
            W
            + underline
            + "QR-SHIELD"
            + end
            + W
            + " Module("
            + R
            + str(module_name)
            + W
            + ")"
            + end
        )

    def reset_name(self) -> None:
        self.name = W + underline + "QR-SHIELD" + end
