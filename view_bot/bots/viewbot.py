import abc
import logging

from playwright.async_api import ProxySettings

from view_bot.models import ProxyConfig


class ViewBot(abc.ABC):

    def __init__(
        self,
        index: int,
        url: str,
        headless: bool = True,
        proxy_config: ProxyConfig | None = None,
    ):
        self.index = index
        self.bot_name = f"ViewBot-{index}"
        self.url = url
        self.headless = headless
        self.proxy_server = proxy_config
        self.proxy = ProxySettings(server=self.proxy_server.socks5_address) if self.proxy_server else None
        self.slow_motion = 500

        base_logger = logging.getLogger(__name__)
        self.logger = logging.LoggerAdapter(base_logger, {"botName": self.bot_name})

    @abc.abstractmethod
    async def run(self) -> None:
        raise NotImplementedError("Subclasses must implement this method")

    async def detect_ip_timezone(self, browser) -> str | None:
        page, context = None, None

        try:
            self.logger.debug("Detecting ip timezone...")

            context = await browser.new_context(proxy=self.proxy)
            page = await context.new_page()
            await page.goto("https://ipapi.co/json/", timeout=10000)

            whoami = await page.evaluate("() => JSON.parse(document.body.innerText)")
            timezone = whoami.get("timezone")
            self.logger.debug("Detected timezone: %s", timezone)
            return timezone

        except Exception as e:
            self.logger.warning(f"Failed to get ip timezone: {e}")
            return None

        finally:
            if page:
                await page.close()
            if context:
                await context.close()
