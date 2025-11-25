import json
import os
import random
from pathlib import Path

from colorful_print import cp
from pydantic import BaseModel
from seleniumbase import SB


class ProxyServer(BaseModel):
    ip: str
    port: int

    @property
    def address(self) -> str:
        return f"{self.ip}:{self.port}"


def read_proxy_available(
    filename: str = "proxy_available.json",
) -> list[dict]:
    script_dir = os.path.dirname(os.path.abspath(__file__))
    datapath = os.path.join(script_dir, ".data", filename)
    filepath = Path(datapath)
    if not filepath.exists():
        raise FileNotFoundError(f"파일이 존재하지 않습니다: {filepath}")

    with open(filepath, "r") as f:
        return json.load(f)


def main():
    proxies: list[ProxyServer] = [ProxyServer(**item) for item in read_proxy_available()]
    proxy: ProxyServer = random.choice(proxies)

    url = "https://httpbin.org/ip"
    # url = "https://sanggi-jayg.tistory.com/entry/Mac-%EB%A7%A5-%ED%99%98%EA%B2%BD-Jetbrains-IDE-%EA%B3%BC%EA%B1%B0-%EB%B2%84%EC%A0%84-%EC%82%AD%EC%A0%9C"

    with SB(proxy=proxy.address, multi_proxy=True) as sb:
        cp.green(f"Try access {url}")
        sb.open(url)
        # sb.uc_open_with_reconnect(url)
        sb.wait(2)

        sb.sleep(5)


if __name__ == "__main__":
    main()
