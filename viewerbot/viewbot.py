from colorful_print import cp
from playwright.async_api import async_playwright, ViewportSize, ProxySettings
from playwright_stealth import Stealth

from viewerbot.model import ProxyServer
from viewerbot.utils import get_random_locale_and_timezone, get_random_useragent


class ViewBot:

    def __init__(
        self,
        index: int,
        url: str,
        headless: bool = True,
        proxy_server: ProxyServer | None = None,
    ):
        self.index = index
        self.url = url
        self.headless = headless
        self.proxy_server = proxy_server
        self.bot_name = f"Bot-{index}"

    async def run(self):
        self._log_start()

        locale, timezone = get_random_locale_and_timezone()
        useragent = get_random_useragent()

        async with Stealth().use_async(async_playwright()) as p:
            browser = await p.chromium.launch(headless=self.headless, slow_mo=500)

            try:
                context = await self._create_browser_context(browser, useragent, locale, timezone)
                page = await context.new_page()
                await self.visit_page(page)

            except Exception as e:
                self._log_error(e)
            finally:
                self._log_finish()
                await browser.close()

    async def _create_browser_context(self, browser, useragent: str, locale: str, timezone: str):
        return await browser.new_context(
            user_agent=useragent,
            locale=locale,
            timezone_id=timezone,
            viewport=ViewportSize({"width": 1920, "height": 1080}),
            proxy=ProxySettings(server=self.proxy_server.address) if self.proxy_server else None,
        )

    async def visit_page(self, page, wait_time: int = 10000):
        await page.goto(self.url)
        cp.green(f"[INFO] {self.bot_name} opened: ", await page.title())
        await page.wait_for_timeout(wait_time)

    def _log_start(self):
        proxy_info = f" with proxy({self.proxy_server.address})" if self.proxy_server else ""
        cp.cyan(f"[INFO] {self.bot_name} started.{proxy_info}", italic=True)

    def _log_error(self, error: Exception):
        cp.bright_red(f"[ERROR] {self.bot_name} encountered an error: {error}", bold=True)

    def _log_finish(self):
        cp.bright_cyan(f"[INFO] {self.bot_name} finished its task.", italic=True)
