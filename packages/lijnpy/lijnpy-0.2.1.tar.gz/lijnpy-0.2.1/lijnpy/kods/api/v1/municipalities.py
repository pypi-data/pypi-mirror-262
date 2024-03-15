from pydantic import ValidationError

from lijnpy import _logger
from lijnpy.kods.api.v1 import _rest_adapter
from lijnpy.kods.api.v1.models import (
    Line,
    Municipality,
    Stop,
)
from lijnpy.rest_adapter import DeLijnAPIException


def get_municipalities() -> list[Municipality]:
    """Get a list of all municipalities in Belgium

    Returns:
        MunicipalitiesResponse: A list of all municipalities in Belgium
    """
    result = _rest_adapter.get("/gemeenten")
    try:
        assert result.data is not None
        municipalities = [
            Municipality(**municipality) for municipality in result.data["gemeenten"]
        ]
    except (AssertionError, ValidationError, KeyError) as e:
        _logger.error(f"Failed to parse the response from the API: {e}")
        raise DeLijnAPIException from e

    return municipalities


def get_stops(municipality_number: int) -> list[Stop]:
    """Get a list of stops in a municipality

    Args:
        municipality_number (int): The municipality number

    Returns:
        StopsResponse: A list of stops in the municipality
    """
    result = _rest_adapter.get(f"/gemeenten/{municipality_number}/haltes")
    try:
        assert result.data is not None
        stops = [Stop(**stop) for stop in result.data["haltes"]]
    except (AssertionError, ValidationError, KeyError) as e:
        _logger.error(f"Failed to parse the response from the API: {e}")
        raise DeLijnAPIException from e

    return stops


def get_lines(municipality_number: int) -> list[Line]:
    """Get a list of lines in a municipality

    Args:
        municipality_number (int): The municipality number

    Returns:
        LinesResponse: A list of lines in the municipality
    """
    result = _rest_adapter.get(f"/gemeenten/{municipality_number}/lijnen")
    try:
        assert result.data is not None
        lines = [Line(**line) for line in result.data["lijnen"]]
    except (AssertionError, ValidationError, KeyError) as e:
        _logger.error(f"Failed to parse the response from the API: {e}")
        raise DeLijnAPIException from e

    return lines


def get_municipality(municipality_number: int) -> Municipality:
    """Get a municipality by its number

    Args:
        municipality_number (int): The number of the municipality

    Returns:
        Municipality: The municipality with the given number
    """
    result = _rest_adapter.get(f"/gemeenten/{municipality_number}")
    try:
        assert result.data is not None
        municipality = Municipality(**result.data)
    except (AssertionError, ValidationError) as e:
        _logger.error(f"Failed to parse the response from the API: {e}")
        raise DeLijnAPIException from e

    return municipality
