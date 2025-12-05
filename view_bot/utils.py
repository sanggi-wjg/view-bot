import json
import os
import random
from pathlib import Path
from warnings import deprecated

from playwright.async_api import ViewportSize

_RANDOM_REFERER = [
    "https://www.google.com/",
    "https://www.google.co.kr/",
    "https://www.naver.com/",
    "https://www.daum.net/",
    "https://www.bing.com/",
    "https://www.yahoo.com/",
    "https://www.facebook.com/",
    "https://twitter.com/",
    "https://www.youtube.com/",
    "https://www.instagram.com/",
    "https://www.reddit.com/",
    "https://www.twitch.tv/",
    None,
]

_RANDOM_VIEWPORT_SIZES = [
    {"width": 1920, "height": 1080},
    {"width": 1366, "height": 768},
    {"width": 1440, "height": 900},
    {"width": 1536, "height": 864},
    {"width": 1280, "height": 720},
    {"width": 1600, "height": 900},
    {"width": 2560, "height": 1440},
    {"width": 3840, "height": 2160},
]


@deprecated("read_proxy_available is deprecated.")
def read_proxy_available(
    filename: str = "proxy_available.json",
) -> list[dict]:
    script_dir = os.path.dirname(os.path.abspath(__file__))
    datapath = os.path.join(script_dir, ".data", filename)
    filepath = Path(datapath)
    if not filepath.exists():
        raise FileNotFoundError(f"File not exists: {filepath}. Please run 'proxy_checker.py' to create the file.")

    with open(filepath, "r") as f:
        return json.load(f)


def get_random_referer() -> str | None:
    # TODO: Expand referer list, or use external library to get popular referer.
    return random.choice(_RANDOM_REFERER)


def get_random_viewport_size() -> ViewportSize:
    return ViewportSize(**random.choice(_RANDOM_VIEWPORT_SIZES))
