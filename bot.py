import asyncio

import typer

from view_bot.bots.viewbot import ViewBot
from view_bot.model import ProxyServer


async def async_main(
    url: str,
    concurrency: int,
    headless: bool,
    use_proxy: bool,
):
    if use_proxy:
        bots = [
            ViewBot(
                i,
                url,
                headless,
                ProxyServer(ip="127.0.0.1", port=9050 + i),
            )
            for i in range(concurrency)
        ]
    else:
        bots = [ViewBot(i, url, headless, None) for i in range(concurrency)]

    tasks = [bot.run() for bot in bots]
    await asyncio.gather(*tasks)


def main(
    url: str = "https://httpbin.org/ip",
    concurrency: int = 5,
    headless: bool = True,
    use_proxy: bool = True,
):
    asyncio.run(
        async_main(url, concurrency, headless, use_proxy),
    )


if __name__ == "__main__":
    typer.run(main)
