from view_bot.bots.single_visit_viewbot import SingleVisitViewBot
from view_bot.bots.viewbot import ViewBot


from view_bot.enums import BotType

from view_bot.model import ProxyServer

_BOT_KLASS_REGISTRY = {
    BotType.SINGLE_VISIT: SingleVisitViewBot,
    # BotType.CONTINUOUS: ContinuousViewbot,
    # BotType.BROWSING: BrowsingViewBot,
}


def create_viewbot(
    bot_type: BotType,
    index: int,
    url: str,
    headless: bool,
    proxy_server: ProxyServer | None,
) -> ViewBot:
    bot_klass = _BOT_KLASS_REGISTRY.get(bot_type)
    if bot_klass is None:
        raise ValueError(f"Unsupported bot type: {bot_type}.")

    return bot_klass(
        index=index,
        url=url,
        headless=headless,
        proxy_server=proxy_server,
    )
