import asyncio

import typer

from view_bot.bots.viewbot_factory import create_viewbot
from view_bot.enums import BotType
from view_bot.models import ProxyConfig


async def async_main(
    bot_type: BotType,
    url: str,
    concurrency: int,
    start_port_number: int,
    headless: bool,
    use_proxy: bool,
):
    bots = [
        create_viewbot(
            bot_type,
            i,
            url,
            headless,
            ProxyConfig(ip="127.0.0.1", port=start_port_number + i) if use_proxy else None,
        )
        for i in range(concurrency)
    ]
    tasks = [bot.run() for bot in bots]
    await asyncio.gather(*tasks)


def main(
    bot_type: BotType = BotType.SINGLE_VISIT,
    url: str = "https://httpbin.org/ip",
    concurrency: int = 5,
    start_port_number: int = 9050,
    headless: bool = True,
    use_proxy: bool = True,
) -> None:
    asyncio.run(
        async_main(
            bot_type=bot_type,
            url=url,
            concurrency=concurrency,
            start_port_number=start_port_number,
            headless=headless,
            use_proxy=use_proxy,
        ),
    )


if __name__ == "__main__":
    typer.run(main)
