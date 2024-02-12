from __future__ import annotations
from json_repair import repair_json

# ----------------------------------------------

def get_salvaged_json(broken_json: str) -> str:
    good_json = repair_json(json_str=broken_json)
    return good_json