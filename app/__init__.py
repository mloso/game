from __future__ import annotations

import sys

MIN_VERSION = (3, 10)
CURRENT_VERSION = (sys.version_info.major, sys.version_info.minor)

if CURRENT_VERSION < MIN_VERSION:
    raise SystemError(
        f"Your python {CURRENT_VERSION} version not supported, minimal version is {MIN_VERSION}"
    )
