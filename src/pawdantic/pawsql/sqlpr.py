from __future__ import annotations

from collections.abc import Sequence, Sized
from functools import lru_cache

import sqlalchemy as sqa
from loguru import logger
from pydantic import BaseModel
from pydantic.alias_generators import to_snake
from sqlmodel import SQLModel


def assign_rel(instance: SQLModel, model: type[SQLModel], matches: list[SQLModel]) -> None:
    """
    Assign a list of models to an instance

    :param instance: instance to assign to
    :param model: model to assign
    :param matches: list of models to assign
    :return: None
    """

    if isinstance(instance, model):
        logger.warning(f'Instance is same type as model: {instance.__class__.__name__}')
        return
    try:
        to_extend = related_from_snakenames(instance, model)
        to_extend.extend(matches)
    except Exception as e:
        logger.error(f'Error assigning {model.__name__} to {instance.__class__.__name__} - {e}')


def related_from_snakenames(instance, model):
    return getattr(instance, f'{to_snake(model.__name__)}s')


async def assign_all(instance: SQLModel, matches_d: dict[str, list[SQLModel]]) -> None:
    """
    Assign all matches to an instance

    :param instance: instance to assign to
    :param matches_d: dict of matches
    :return: None
    """
    for group_name, matches in matches_d.items():
        if not matches:
            continue
        model = matches[0].__class__
        assign_rel(instance, model, matches)


def matches_str(matches: Sized, model: type):
    """
    :param matches: A list of model instances.
    :param model: The model class to describe.
    :return: A string describing the number and type of model matches.
    """
    matches = len(matches)
    return f"{matches} '{model.__name__}' {'match' if matches == 1 else 'matches'}"


def model_map_(models: Sequence[SQLModel]) -> dict[str, SQLModel]:
    """
    Get a map of model names to models

    :param models: models to map
    :return: dict of model names to models
    """
    return {f'{to_snake(_.__name__)}s': _ for _ in models}


@lru_cache
def get_other_table_names(obj, data_models) -> list[str]:
    """
    Get the names of all tables that are not the table of an object

    :param obj: object to check
    :param data_models: models to check
    :return: list of table names
    """
    return [related_from_snakenames(obj, _) for _ in data_models if not isinstance(obj, _)]


class GenericJSONType(sqa.TypeDecorator):
    impl = sqa.JSON

    def __init__(self, model_class: type[BaseModel], *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.model_class = model_class

    def process_bind_param(self, value, dialect):
        return value.model_dump_json(round_trip=True) if value is not None else None

    def process_result_value(self, value, dialect):
        return self.model_class.model_validate_json(value) if value else None
