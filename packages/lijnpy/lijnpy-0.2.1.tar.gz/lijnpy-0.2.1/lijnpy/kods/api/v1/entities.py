from pydantic import ValidationError

from lijnpy import _logger
from lijnpy.kods.api.v1 import _rest_adapter
from lijnpy.kods.api.v1.models import (
    Entity,
    Line,
    Municipality,
    Stop,
)
from lijnpy.rest_adapter import DeLijnAPIException


def get_entities() -> list[Entity]:
    """Get a list of all entities

    Returns:
        list[Entity]: A list of all entities
    """
    result = _rest_adapter.get("/entiteiten")
    try:
        assert result.data is not None
        entities = [Entity(**entity) for entity in result.data["entiteiten"]]
    except (AssertionError, ValidationError, KeyError) as e:
        _logger.error(f"Failed to parse the response from the API: {e}")
        raise DeLijnAPIException from e

    return entities


def get_entity(entity_number: int) -> Entity:
    """Get an entity by its number

    Args:
        entity_number (int): The number of the entity

    Returns:
        Entity: The entity with the given number
    """
    result = _rest_adapter.get(f"/entiteiten/{entity_number}")
    try:
        assert result.data is not None
        entity = Entity(**result.data)
    except (AssertionError, ValidationError) as e:
        _logger.error(f"Failed to parse the response from the API: {e}")
        raise DeLijnAPIException from e

    return entity


def get_municipalities(entity_number: int) -> list[Municipality]:
    """Get a list of municipalities in Belgium for a given entity

    Args:
        entity_number (str): The number of the entity

    Returns:
        list[Municipality]: A list of municipalities in Belgium for a given entity
    """
    result = _rest_adapter.get(f"/entiteiten/{entity_number}/gemeenten")
    try:
        assert result.data is not None
        municipalities = [
            Municipality(**municipality) for municipality in result.data["gemeenten"]
        ]
    except (AssertionError, ValidationError, KeyError) as e:
        _logger.error(f"Failed to parse the response from the API: {e}")
        raise DeLijnAPIException from e

    return municipalities


def get_stops(entity_number: int) -> list[Stop]:
    """Get a list of stops in Belgium for a given entity

    Args:
        entity_number (str): The number of the entity

    Returns:
        list[Stop]: A list of stops in Belgium for a given entity
    """
    result = _rest_adapter.get(f"/entiteiten/{entity_number}/haltes")
    try:
        assert result.data is not None
        stops = [Stop(**stop) for stop in result.data["haltes"]]
    except (AssertionError, ValidationError, KeyError) as e:
        _logger.error(f"Failed to parse the response from the API: {e}")
        raise DeLijnAPIException from e

    return stops


def get_lines(entity_number: int) -> list[Line]:
    """Get a list of lines in Belgium for a given entity

    Args:
        entity_number (str): The number of the entity

    Returns:
        list[Line]: A list of lines in Belgium for a given entity
    """
    result = _rest_adapter.get(f"/entiteiten/{entity_number}/lijnen")
    try:
        assert result.data is not None
        lines = [Line(**line) for line in result.data["lijnen"]]
    except (AssertionError, ValidationError, KeyError) as e:
        _logger.error(f"Failed to parse the response from the API: {e}")
        raise DeLijnAPIException from e

    return lines
