from aiohttp import ClientSession, ClientResponse
from ssl import SSLContext
from typing import Literal


class Connectivity:
    """Class to make authenticated requests."""

    def __init__(
        self, websession: ClientSession, host: str, username: str, password: str
    ):
        """Initialize the auth."""
        self.websession = websession
        self.host = host
        self.username = username
        self.password = password
        self.cookie = None
        self.ssl_context: SSLContext | Literal[False] = False

    async def login(self) -> None:
        """Login to the router with username and password. Receive a bauth cookie back to use as authentication for the session."""
        login_url = f"{self.host}/api/login"
        async with self.websession.post(
            login_url,
            data={"username": self.username, "password": self.password},
            ssl=self.ssl_context,
        ) as response:
            if response.status == 200:
                self.cookie = response.cookies.get("bauth")
            else:
                raise Exception(
                    f"Failed to get authentication cookie. Status code: {response.status}"
                )

    async def request(self, method: str, path: str, **kwargs) -> ClientResponse:
        """Make a request."""
        if not self.cookie:
            await self.login()

        headers = kwargs.get("headers")

        if headers is None:
            headers = {}
        else:
            headers = dict(headers)

        cookies = {"bauth": self.cookie}

        return await self.websession.request(
            method,
            f"{self.host}/api/{path}",
            **kwargs,
            headers=headers,
            cookies=cookies,
            ssl=self.ssl_context,
        )
