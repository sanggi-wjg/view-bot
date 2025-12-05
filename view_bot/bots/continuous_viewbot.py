import asyncio
import traceback

from playwright.async_api import async_playwright
from playwright_stealth import Stealth

from view_bot.bots.single_visit_viewbot import SingleVisitViewBot


class ContinuousViewBot(SingleVisitViewBot):

    async def run(self) -> None:
        # fixme 패턴이나 구조는 이후 진행 예정, kiss for now
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
                await asyncio.Future()

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
