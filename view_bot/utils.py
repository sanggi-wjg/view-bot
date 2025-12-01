import json
import os
import random
from pathlib import Path

from fake_useragent import UserAgent


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


def get_random_useragent() -> str:
    ua = UserAgent()
    return ua.random


def get_random_locale_and_timezone() -> tuple[str, str]:
    return random.choice(
        [
            ("ko-KR", "Asia/Seoul"),
            ("en-US", "America/New_York"),
            ("en-US", "America/Los_Angeles"),
            ("en-US", "America/Chicago"),
            ("en-GB", "Europe/London"),
            ("fr-FR", "Europe/Paris"),
            ("de-DE", "Europe/Berlin"),
            ("ja-JP", "Asia/Tokyo"),
            ("zh-CN", "Asia/Shanghai"),
            ("zh-TW", "Asia/Taipei"),
            ("zh-HK", "Asia/Hong_Kong"),
            ("en-SG", "Asia/Singapore"),
            ("es-ES", "Europe/Madrid"),
            ("pt-BR", "America/Sao_Paulo"),
            ("ru-RU", "Europe/Moscow"),
            ("it-IT", "Europe/Rome"),
            ("en-AU", "Australia/Sydney"),
            ("en-NZ", "Pacific/Auckland"),
        ]
    )


def get_random_referer() -> str | None:
    return random.choice(
        [
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
    )
