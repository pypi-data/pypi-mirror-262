"""Peplink info model."""

from ..interfaces.connectivity import Connectivity


class Location:
    """Class that represents a GPS Location Obj in the Peplink API."""

    def __init__(self, raw_data: dict, connectivity: Connectivity):
        """Initialize a GPS Location Obj."""
        self.raw_data = raw_data
        self.connectivity = connectivity

    @property
    def latitude(self) -> str:
        """Return the latitude of the GPS Location Obj."""
        return self.raw_data["response"]["location"]["latitude"]

    @property
    def longitude(self) -> str:
        """Return the longitude of the GPS Location Obj."""
        return self.raw_data["response"]["location"]["longitude"]

    @property
    def altitude(self) -> str:
        """Return the altitude of the GPS Location Obj."""
        return self.raw_data["response"]["location"]["altitude"]

    @property
    def speed(self) -> str:
        """Return the speed of the GPS Location Obj."""
        return self.raw_data["response"]["location"]["speed"]

    @property
    def heading(self) -> str:
        """Return the heading of the GPS Location Obj."""
        return self.raw_data["response"]["location"]["heading"]

    async def async_update(self):
        """Update the GPS Location data."""
        resp = await self.connectivity.request("get", "info.location")
        resp.raise_for_status()
        self.raw_data = await resp.json()
