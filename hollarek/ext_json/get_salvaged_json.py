from __future__ import annotations
from json_repair import repair_json

# ----------------------------------------------

def get_salvaged_json_str(json_str: str) -> str:
    good_json = repair_json(json_str=json_str)
    return good_json