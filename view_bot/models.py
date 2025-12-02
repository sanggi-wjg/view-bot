from pydantic import BaseModel


class ProxyServer(BaseModel):
    ip: str
    port: int
    username: str | None = None
    password: str | None = None

    @property
    def address(self) -> str:
        return f"{self.ip}:{self.port}"

    @property
    def http_address(self) -> str:
        return f"http://{self.ip}:{self.port}"

    @property
    def https_address(self) -> str:
        return f"https://{self.ip}:{self.port}"

    @property
    def socks_address(self) -> str:
        return f"socks://{self.ip}:{self.port}"

    @property
    def socks5_address(self) -> str:
        return f"socks5://{self.ip}:{self.port}"

    @property
    def socks5_address_with_auth(self) -> str:
        if self.username and self.password:
            return f"socks5://{self.username}:{self.password}@{self.ip}:{self.port}"
        raise ValueError("Username and password must be provided for authenticated SOCKS5 address.")


class BrowserFingerprint(BaseModel):
    user_agent: str
    vendor: str
    app_version: str
    platform: str
    locale: str
    timezone: str
