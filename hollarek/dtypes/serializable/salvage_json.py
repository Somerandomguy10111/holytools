from json_repair import repair_json, loads


def salvage_json(json_str : str) -> str:
    return repair_json(json_str=json_str)


def load_broken_json(json_str : str) -> dict:
    return loads(json_str)