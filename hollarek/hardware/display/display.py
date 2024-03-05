from typing import Optional
from PIL import Image
from mss import mss
from screeninfo import get_monitors, Monitor


def get_primary_monitor() -> Optional[Monitor]:
    for monitor in get_monitors():
        if monitor.is_primary:
            return monitor
    return None

def get_secondary_monitor() -> Optional[Monitor]:
    for monitor in get_monitors():
        if not monitor.is_primary:
            return monitor
    return None

def get_screenshot(monitor : Monitor = get_primary_monitor()) -> Image:
    if not monitor:
        raise ValueError(f"Given monitor {monitor} is None")

    with mss() as sct:
        monitor_dict = {"top": monitor.y, "left": monitor.x, "width": monitor.width, "height": monitor.height}
        sct_img = sct.grab(monitor_dict)
        return Image.frombytes('RGB', sct_img.size, sct_img.bgra, 'raw', 'BGRX')
