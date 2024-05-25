from __future__ import annotations

import logging
from dataclasses import dataclass
from typing import Optional


@dataclass
class LogSettings:
    threshold: int = logging.INFO
    log_fpath: Optional[str] = None
    timestamp: bool = True
    include_ms : bool = False
    include_call_location : bool = False


class LogTarget:
    FILE = "FILE"
    CONSOLE = "CONSOLE"

