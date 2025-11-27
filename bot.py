import asyncio

import typer

from viewerbot.model import ProxyServer
from viewerbot.utils import read_proxy_available
from viewerbot.viewbot import ViewBot


async def async_main(
    url: str,
    headless: bool,
    use_proxy: bool,
):
    if use_proxy:
        proxies = [ProxyServer(**item) for item in read_proxy_available()]
        bots = [
            ViewBot(
                i + 1,
                url,
                headless,
                p,
            )
            for i, p in enumerate(proxies)
        ]
    else:
        bots = [
            ViewBot(
                i + 1,
                url,
                headless,
                None,
            )
            for i in range(5)
        ]

    tasks = [bot.run() for bot in bots]
    await asyncio.gather(*tasks)


def main(
    url: str = "https://www.fitpetmall.com/mall",
    headless: bool = True,
    use_proxy: bool = False,
):
    asyncio.run(
        async_main(url, headless, use_proxy),
    )


if __name__ == "__main__":
    typer.run(main)
