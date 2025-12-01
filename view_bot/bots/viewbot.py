from colorful_print import cp
from playwright.async_api import async_playwright, ViewportSize, ProxySettings
from playwright_stealth import Stealth

from view_bot.model import ProxyServer
from view_bot.utils import get_random_referer, get_random_locale_and_timezone, get_random_useragent


class ViewBot:

    def __init__(
        self,
        index: int,
        url: str,
        headless: bool = True,
        proxy_server: ProxyServer | None = None,
    ):
        self.index = index
        self.bot_name = f"Bot-{index}"
        self.url = url
        self.headless = headless
        self.proxy_server = proxy_server

    def _log_start(self, browser_name: str, browser_version: str):
        cp.cyan(f"[INFO] {self.bot_name} started. | proxy: proxy : {self.proxy_server.address}", italic=True)

    def _log_error(self, e: Exception):
        cp.bright_red(f"[ERROR] {self.bot_name} encountered an error: {e}", bold=True)

    def _log_finish(self):
        cp.bright_cyan(f"[INFO] {self.bot_name} finished its task.", italic=True)

    async def visit_page(self, page):
        await page.goto(
            self.url,
            referer=get_random_referer(),
            # wait_until="domcontentloaded",
            timeout=60000,
        )

        title = await page.title()
        body_text = await page.locator("body").inner_text()
        # cp.green(f"[INFO] {self.bot_name} visit {self.url}: {title}")
        cp.green(f"[INFO] {self.bot_name} visit {page}: {title}\n{body_text[:50]}")
        # await page.wait_for_event(3000)

    async def run(self):
        async with Stealth().use_async(async_playwright()) as p:
            browser = await p.firefox.launch(headless=self.headless, slow_mo=500)
            self._log_start(browser.browser_type.name, browser.version)

            try:
                useragent = get_random_useragent()
                locale, timezone = get_random_locale_and_timezone()

                context = await browser.new_context(
                    user_agent=useragent,
                    locale=locale,
                    timezone_id=timezone,
                    viewport=ViewportSize(width=1920, height=1080),
                    proxy=(ProxySettings(server=self.proxy_server.socks5_address) if self.proxy_server else None),
                )
                page = await context.new_page()
                await self.visit_page(page)
                # await asyncio.Future()

            except Exception as e:
                self._log_error(e)
            finally:
                self._log_finish()
                await browser.close()
