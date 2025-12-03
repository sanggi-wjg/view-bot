import traceback

from playwright.async_api import async_playwright, BrowserContext
from playwright_stealth import Stealth

from view_bot.bots.viewbot import ViewBot
from view_bot.utils import get_random_referer, get_random_viewport_size


class SingleVisitViewBot(ViewBot):

    async def visit_page(self, page) -> None:
        await page.goto(
            self.url,
            referer=get_random_referer(),
            wait_until="load",
            timeout=60000,
        )

        title = await page.title()
        body_text = await page.locator("body").inner_text()
        self.logger.info(f"Visited {self.url}: {title} / {body_text[:50]}")
        await page.wait_for_timeout(1000)

    async def create_context(self, browser) -> BrowserContext:
        timezone = await self.detect_ip_timezone(browser)
        viewport = get_random_viewport_size()

        return await browser.new_context(
            timezone_id=timezone,
            viewport=viewport,
            proxy=self.proxy,
        )

    async def run(self) -> None:
        page, context = None, None

        async with Stealth().use_async(async_playwright()) as p:
            browser = await p.firefox.launch(
                headless=self.headless,
                slow_mo=self.slow_motion,
                firefox_user_prefs=self.get_stealth_firefox_preferences(),
            )
            self.logger.info("🚀 launched")

            try:
                context = await self.create_context(browser)
                page = await context.new_page()
                await self.visit_page(page)
                # await asyncio.Future()

            except Exception as e:
                self.logger.error(f"🔥 An error occurred: {e}")
                traceback.print_exc()

            finally:
                self.logger.info("👍 closed")
                if page:
                    await page.close()
                if context:
                    await context.close()
                await browser.close()
