from pydantic_core import ValidationError

from lijnpy import _logger
from lijnpy.kods.api.v1 import _rest_adapter
from lijnpy.kods.api.v1.models import (
    Detour,
    Direction,
    Disruption,
    GeoCoordinate,
    Passage,
    PassageNote,
    RealTimePassage,
    RealTimeTimetable,
    RideNote,
    Stop,
    StopInVicinity,
    Timetable,
)
from lijnpy.rest_adapter import DeLijnAPIException


def get_stops_in_vicinity(
    geo_coordinate: GeoCoordinate,
) -> list[StopInVicinity]:
    """Get a list of all available stops in the neighbourhood of the given geo-coordinates

    Args:
        geo_coordinate (GeoCoordinate): The geo-coordinates to search around

    Returns:
        StopsInVicinityResponse: A list of all available stops in the neighbourhood of the given geo-coordinates

    Raises:
        DeLijnAPIException: If the API request fails
    """
    result = _rest_adapter.get(
        f"/haltes/indebuurt/{geo_coordinate.latitude},{geo_coordinate.longitude}",
    )
    try:
        assert result.data is not None
        stops_in_vicinity = [StopInVicinity(**stop) for stop in result.data["haltes"]]
    except (AssertionError, ValidationError, KeyError) as e:
        _logger.error(f"Failed to parse the response from the API: {e}")
        raise DeLijnAPIException from e

    return stops_in_vicinity


def get_stop(entity_number: int, stop_number: int) -> Stop:
    """Get the stop with the given entity and stop number

    Args:
        entity_number (int): The number of the entity
        stop_number (int): The number of the stop

    Returns:
        StopResponse: The stop with the given entity and stop number

    Raises:
        DeLijnAPIException: If the API request fails
    """
    result = _rest_adapter.get(f"/haltes/{entity_number}/{stop_number}")
    try:
        assert result.data is not None
        stop = Stop(**result.data)
    except (AssertionError, ValidationError) as e:
        _logger.error(f"Failed to parse the response from the API: {e}")
        raise DeLijnAPIException from e

    return stop


def get_timetable(entity_number: int, stop_number: int) -> Timetable:
    """Get the schedule of the stop with the given entity and stop number

    Returns:
        Timetable: The schedule of the stop with the given entity and stop number

    Raises:
        DeLijnAPIException: If the API request fails
    """
    result = _rest_adapter.get(
        f"/haltes/{entity_number}/{stop_number}/dienstregelingen"
    )
    try:
        assert result.data is not None
        timetable = Timetable(
            passages=[
                Passage(**passage)
                for passage in result.data["halteDoorkomsten"][0]["doorkomsten"]
            ],
            passage_notes=[
                PassageNote(**note) for note in result.data["doorkomstNotas"]
            ],
            ride_notes=[RideNote(**note) for note in result.data["ritNotas"]],
            detours=[Detour(**detour) for detour in result.data["omleidingen"]],
        )
    except (AssertionError, ValidationError, KeyError) as e:
        _logger.error(f"Failed to parse the response from the API: {e}")
        raise DeLijnAPIException from e

    return timetable


def get_directions(entity_number: int, stop_number: int) -> list[Direction]:
    """Get the directions of the stop with the given entity and stop number

    Args:
        entity_number (int): The number of the entity
        stop_number (int): The number of the stop

    Returns:
        DirectionsResponse: The directions of the stop with the given entity and stop number

    Raises:
        DeLijnAPIException: If the API request fails
    """
    result = _rest_adapter.get(f"/haltes/{entity_number}/{stop_number}/lijnrichtingen")
    try:
        assert result.data is not None
        directions = [
            Direction(**direction) for direction in result.data["lijnrichtingen"]
        ]
    except (AssertionError, ValidationError, KeyError) as e:
        _logger.error(f"Failed to parse the response from the API: {e}")
        raise DeLijnAPIException from e

    return directions


def get_detours(entity_number: int, stop_number: int) -> list[Detour]:
    """Get the detours of the stop with the given entity and stop number

    Args:
        entity_number (int): The number of the entity
        stop_number (int): The number of the stop

    Returns:
        DetoursResponse: The detours of the stop with the given entity and stop number

    Raises:
        DeLijnAPIException: If the API request fails
    """
    result = _rest_adapter.get(f"/haltes/{entity_number}/{stop_number}/omleidingen")
    try:
        assert result.data is not None
        detours = [Detour(**detour) for detour in result.data["omleidingen"]]
    except (AssertionError, ValidationError, KeyError) as e:
        _logger.error(f"Failed to parse the response from the API: {e}")
        raise DeLijnAPIException from e

    return detours


def get_real_time_timetable(entity_number: int, stop_number: int) -> RealTimeTimetable:
    """Get the real-time arrivals of the stop with the given entity and stop number

    Args:
        entity_number (int): The number of the entity
        stop_number (int): The number of the stop

    Returns:
        RealTimePassagesResponse: The real-time arrivals of the stop with the given entity and stop number

    Raises:
        DeLijnAPIException: If the API request fails
    """
    result = _rest_adapter.get(
        f"/haltes/{entity_number}/{stop_number}/real-time-doorkomsten"
    )
    try:
        assert result.data is not None
        real_time_timetable = RealTimeTimetable(
            passages=[
                RealTimePassage(**passage)
                for passage in result.data["halteDoorkomsten"][0]["doorkomsten"]
            ],
            passage_notes=[
                PassageNote(**note) for note in result.data["doorkomstNotas"]
            ],
            ride_notes=[RideNote(**note) for note in result.data["ritNotas"]],
            detours=[Detour(**detour) for detour in result.data["omleidingen"]],
        )
    except (AssertionError, ValidationError, KeyError) as e:
        _logger.error(f"Failed to parse the response from the API: {e}")
        raise DeLijnAPIException from e

    return real_time_timetable


def get_disruptions(entity_number: int, stop_number: int) -> list[Disruption]:
    """Get the directions of the stop with the given entity and stop number

    Args:
        entity_number (int): The number of the entity
        stop_number (int): The number of the stop

    Returns:
        DisruptionsResponse: The disruptions of the stop with the given entity and stop number
    Raises:
        DeLijnAPIException: If the API request fails
    """
    result = _rest_adapter.get(f"/haltes/{entity_number}/{stop_number}/storingen")
    try:
        assert result.data is not None
        disruptions = [
            Disruption(**disruption) for disruption in result.data["storingen"]
        ]
    except (AssertionError, ValidationError, KeyError) as e:
        _logger.error(f"Failed to parse the response from the API: {e}")
        raise DeLijnAPIException from e

    return disruptions
