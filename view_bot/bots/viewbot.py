import abc

from colorful_print import cp

from view_bot.model import ProxyServer


class ViewBot(abc.ABC):

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
        self.slow_motion = 500

    def _log_start(self) -> None:
        proxy_info = f"proxy: {self.proxy_server.address}" if self.proxy_server else "no proxy"
        cp.bright_blue(f"[INFO] {self.bot_name} started. | {proxy_info}")

    def _log_info(self, *args) -> None:
        cp.green(f"[INFO] {self.bot_name} ", *args)

    def _log_warn(self, *args) -> None:
        cp.yellow(f"[WARN] {self.bot_name} ", *args)

    def _log_error(self, e: Exception) -> None:
        cp.red(f"[ERROR] {self.bot_name} encountered an error: {e}", bold=True)

    def _log_finish(self) -> None:
        cp.bright_blue(f"[INFO] {self.bot_name} finished its task.")

    @abc.abstractmethod
    async def run(self):
        raise NotImplementedError("Subclasses must implement this method")
