import abc

from colorful_print import cp
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
        self.bot_name = f"Bot-{index}"
        self.url = url
        self.headless = headless
        self.proxy_server = proxy_config
        self.proxy = ProxySettings(server=self.proxy_server.socks5_address) if self.proxy_server else None
        self.slow_motion = 500

    def log_start(self) -> None:
        proxy_info = f"proxy: {self.proxy_server.address}" if self.proxy_server else "no proxy"
        cp.bright_blue(f"[INFO] {self.bot_name} started. | {proxy_info}")

    def log_info(self, *args) -> None:
        cp.green(f"[INFO] {self.bot_name} ", *args)

    def log_warn(self, *args) -> None:
        cp.yellow(f"[WARN] {self.bot_name} ", *args)

    def log_error(self, e: Exception) -> None:
        cp.red(f"[ERROR] {self.bot_name} encountered an error: {e}", bold=True)

    def log_finish(self) -> None:
        cp.bright_blue(f"[INFO] {self.bot_name} finished its task.")

    @abc.abstractmethod
    async def run(self) -> None:
        raise NotImplementedError("Subclasses must implement this method")

    async def detect_ip_timezone(self, browser) -> str | None:
        page, context = None, None

        try:
            context = await browser.new_context(proxy=self.proxy)
            page = await context.new_page()
            await page.goto("https://ipapi.co/json/", timeout=10000)
            whoami = await page.evaluate("() => JSON.parse(document.body.innerText)")
            return whoami.get("timezone")
        except Exception as e:
            self.log_warn(e)
            # todo print stack trace
            return None
        finally:
            if page:
                await page.close()
            if context:
                await context.close()
