from typing import List

from .interfaces.connectivity import Connectivity
from .models.info import Location


class PeplinkAPI:
    """Class to communicate with the Peplink API."""

    def __init__(self, connectivity: Connectivity):
        """Initialize the API and store the auth so we can make requests."""
        self.connectivity = connectivity

    async def async_get_location(self) -> Location:
        """Return the location."""
        resp = await self.connectivity.request("get", "info.location")
        resp.raise_for_status()
        return Location(await resp.json(), self.connectivity)
