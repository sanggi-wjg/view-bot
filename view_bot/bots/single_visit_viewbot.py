from playwright.async_api import ViewportSize, ProxySettings, async_playwright
from playwright_stealth import Stealth

from view_bot.bots.viewbot import ViewBot
from view_bot.utils import get_random_referer, get_random_locale_and_timezone, get_random_useragent


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
        self._log_info(f"visit {page}: {title}. {body_text[:50]}")
        await page.wait_for_timeout(1000)

    async def run(self):
        page, context = None, None

        async with Stealth().use_async(async_playwright()) as p:
            browser = await p.firefox.launch(headless=self.headless, slow_mo=self.slow_motion)
            self._log_start()

            try:
                useragent = get_random_useragent()
                locale, timezone = get_random_locale_and_timezone()

                context = await browser.new_context(
                    user_agent=useragent,
                    locale=locale,
                    timezone_id=timezone,
                    viewport=ViewportSize(width=1920, height=1080),
                    proxy=ProxySettings(server=self.proxy_server.socks5_address) if self.proxy_server else None,
                )
                page = await context.new_page()
                await self.visit_page(page)
                # await asyncio.Future()

            except Exception as e:
                self._log_error(e)

            finally:
                self._log_finish()
                if page:
                    await page.close()
                if context:
                    await context.close()
                await browser.close()
