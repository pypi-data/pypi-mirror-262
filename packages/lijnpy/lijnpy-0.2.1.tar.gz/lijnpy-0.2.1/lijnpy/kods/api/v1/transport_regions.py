from pydantic import ValidationError

from lijnpy import _logger
from lijnpy.kods.api.v1 import _rest_adapter
from lijnpy.kods.api.v1.models import Line, TransportRegion
from lijnpy.rest_adapter import DeLijnAPIException


def get_transport_regions() -> list[TransportRegion]:
    """Get a list of all transport regions

    Returns:
        TransportRegionsResponse: A list of all transport regions
    """
    result = _rest_adapter.get("/vervoerregios")
    try:
        assert result.data is not None
        transport_regions = [
            TransportRegion(**transport_region)
            for transport_region in result.data["vervoerRegios"]
        ]
    except (AssertionError, ValidationError, KeyError) as e:
        _logger.error(f"Failed to parse the response from the API: {e}")
        raise DeLijnAPIException from e

    return transport_regions


def get_transport_region(transport_region_code: str) -> TransportRegion:
    """Get a transport region by code

    Args:
        transport_region_code (str): The code of the transport region

    Returns:
        TransportRegion: The transport region
    """
    result = _rest_adapter.get(f"/vervoerregios/{transport_region_code}")
    try:
        assert result.data is not None
        transport_region = TransportRegion(**result.data)
    except (AssertionError, ValidationError) as e:
        _logger.error(f"Failed to parse the response from the API: {e}")
        raise DeLijnAPIException from e

    return transport_region


def get_lines(transport_region_code: str) -> list[Line]:
    """Get a list of lines by transport region code

    Args:
        transport_region_code (str): The code of the transport region

    Returns:
        LinesResponse: A list of lines
    """
    result = _rest_adapter.get(f"/vervoerregios/{transport_region_code}/lijnen")
    try:
        assert result.data is not None
        lines_response = [Line(**line) for line in result.data["lijnen"]]
    except (AssertionError, ValidationError, KeyError) as e:
        _logger.error(f"Failed to parse the response from the API: {e}")
        raise DeLijnAPIException from e

    return lines_response
