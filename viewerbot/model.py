from pydantic import BaseModel


class ProxyServer(BaseModel):
    ip: str
    port: int

    @property
    def address(self) -> str:
        return f"{self.ip}:{self.port}"
