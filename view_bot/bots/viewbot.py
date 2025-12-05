import abc
import logging

from playwright.async_api import ProxySettings, Browser

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
        self.proxy_config = proxy_config
        self.proxy = ProxySettings(server=self.proxy_config.socks5_address) if self.proxy_config else None
        self.slow_motion = 500

        base_logger = logging.getLogger(__name__)
        self.logger = logging.LoggerAdapter(base_logger, {"botName": self.bot_name})

    def get_stealth_firefox_preferences(self) -> dict[str, bool | int]:
        return {
            "privacy.resistFingerprinting": True,
            "media.peerconnection.enabled": False,
            "privacy.resistFingerprinting.randomization.daily_reset.enabled": True,
            "webgl.disabled": False,
            "privacy.resistFingerprinting.randomDataOnCanvasExtract": True,
            "layout.css.font-visibility.private": 1,
            "dom.maxHardwareConcurrency": 2,  # CPU 코어 수 제한
        }

    async def detect_ip_timezone(self, browser: Browser) -> str | None:
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

    @abc.abstractmethod
    async def run(self) -> None:
        raise NotImplementedError("Subclasses must implement this method")
