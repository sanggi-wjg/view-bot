import asyncio

from playwright.async_api import ViewportSize, ProxySettings, async_playwright
from playwright_stealth import Stealth

from view_bot.bots.viewbot import ViewBot
from view_bot.utils import get_random_referer


class SingleVisitViewBot(ViewBot):

    async def visit_page(self, page):
        await page.goto(
            self.url,
            referer=get_random_referer(),
            wait_until="load",
            timeout=60000,
        )

        title = await page.title()
        body_text = await page.locator("body").inner_text()
        self.log_info(f"visit {page}: {title} / {body_text[:50]}")
        await page.wait_for_timeout(1000)

    async def create_context(self, browser):
        # useragent = get_random_useragent()
        # locale, timezone = get_random_locale_and_timezone()

        return await browser.new_context(
            # locale=locale,
            # timezone_id=timezone,
            viewport=ViewportSize(width=1920, height=1080),
            proxy=ProxySettings(server=self.proxy_server.socks5_address) if self.proxy_server else None,
        )

    async def run(self):
        page, context = None, None

        async with Stealth().use_async(async_playwright()) as p:
            browser = await p.firefox.launch(headless=self.headless, slow_mo=self.slow_motion)
            self.log_start()

            try:
                context = await self.create_context(browser)
                page = await context.new_page()
                await self.visit_page(page)
                await asyncio.Future()

            except Exception as e:
                self.log_error(e)

            finally:
                self.log_finish()
                if page:
                    await page.close()
                if context:
                    await context.close()
                await browser.close()
