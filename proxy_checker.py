import asyncio
import json
import os
from pathlib import Path

import httpx
from colorful_print import cp
from pydantic import BaseModel


class ProxyCheckResult(BaseModel):
    ip: str
    port: int
    socket_ok: bool = False
    https_ok: bool = False

    @property
    def is_ok(self) -> bool:
        return self.socket_ok and self.https_ok

    def __repr__(self) -> str:
        status = "alive" if self.is_ok else "dead"
        return f"ProxyCheckResult({self.ip}:{self.port}, {status})"


async def check_socket_proxy_server(ip: str, port: int, timeout: float = 3.0) -> bool:
    try:
        reader, writer = await asyncio.wait_for(
            asyncio.open_connection(ip, port),
            timeout=timeout,
        )
        writer.close()
        await writer.wait_closed()
        return True
    except (asyncio.TimeoutError, OSError, ConnectionRefusedError):
        return False


async def check_https_proxy_server(ip: str, port: int, timeout: float = 5.0) -> bool:
    proxy_url = f"http://{ip}:{port}"
    ip_echo_url = "https://httpbin.org/ip"

    try:
        async with httpx.AsyncClient(proxy=proxy_url, timeout=timeout) as client:
            response = await client.get(ip_echo_url)
            response.raise_for_status()
            return True
    except (httpx.ProxyError, httpx.TimeoutException, httpx.ConnectError, httpx.HTTPStatusError, Exception):
        return False


async def check_proxy(ip: str, port: int, socket_timeout: float = 3.0, https_timeout: float = 5.0) -> ProxyCheckResult:
    cp.bright_blue(f"🔍 프록시 체크 중: {ip}:{port}", italic=True)
    result = ProxyCheckResult(ip=ip, port=port)

    result.socket_ok = await check_socket_proxy_server(ip, port, socket_timeout)
    if not result.socket_ok:
        return result

    result.https_ok = await check_https_proxy_server(ip, port, https_timeout)
    return result


async def check_proxies(
    proxies: list[tuple[str, int]],
    socket_timeout: float = 3.0,
    https_timeout: float = 5.0,
    concurrency: int = 10,
) -> list[ProxyCheckResult]:
    semaphore = asyncio.Semaphore(concurrency)

    async def check_with_semaphore(ip: str, port: int) -> ProxyCheckResult:
        async with semaphore:
            return await check_proxy(ip, port, socket_timeout, https_timeout)

    tasks = [check_with_semaphore(ip, port) for ip, port in proxies]
    return await asyncio.gather(*tasks)


async def filter_available_proxies(
    proxies: list[tuple[str, int]],
    concurrency: int = 10,
) -> list[ProxyCheckResult]:
    results = await check_proxies(proxies=proxies, concurrency=concurrency)
    return [r for r in results if r.is_ok]


async def check_proxies_from_file(
    input_file: str = "proxy_candidate.json",
    output_file: str = "proxy_available.json",
):
    script_dir = os.path.dirname(os.path.abspath(__file__))
    data_dir = os.path.join(script_dir, ".data")
    input_path = Path(os.path.join(data_dir, input_file))
    output_path = Path(os.path.join(data_dir, output_file))

    if not input_path.exists():
        cp.red(f"입력 파일 {input_path}이 존재하지 않습니다.")
        return

    with open(input_path, "r") as f:
        proxy_data = json.load(f)

    cp.cyan(f"총 {len(proxy_data)}개의 프록시 서버를 체크합니다.")
    proxies = [(item["ip"], item["port"]) for item in proxy_data]
    available_proxies = await filter_available_proxies(proxies)
    available_proxies_dict = [proxy.model_dump() for proxy in available_proxies]

    cp.green(f"\n체크 완료: 총 {len(proxies)}개")
    cp.green(f"살아있는 프록시: {len(available_proxies)}개", bold=True)
    cp.bright_red(f"죽은 프록시: {len(proxies) - len(available_proxies)}개")
    cp.green(f"생존률: {len(available_proxies) / len(proxies) * 100:.1f}%")

    with open(output_path, "w") as f:
        json.dump(available_proxies_dict, f, indent=2)

    cp.green(f"\n사용 가능한 프록시를 {output_path}에 저장했습니다.", bold=True)


if __name__ == "__main__":
    asyncio.run(
        check_proxies_from_file(),
    )
