import sqlalchemy
from pydantic import BaseModel
from sqlmodel import Column, Field


class PydanticJSONColumn(sqlalchemy.TypeDecorator):
    impl = sqlalchemy.JSON

    def __init__(self, model_class: type[BaseModel], *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.model_class = model_class

    def process_bind_param(self, value, dialect):
        if value is None:
            return None
        elif isinstance(value, list):
            return [item.model_dump_json(round_trip=True) if isinstance(item, BaseModel) else item for item in value]
        elif isinstance(value, dict):
            return {
                key: item.model_dump_json(round_trip=True) if isinstance(item, BaseModel) else item
                for key, item in value.items()
            }
        elif isinstance(value, BaseModel):
            return value.model_dump_json(round_trip=True)
        return value

    def process_result_value(self, value, dialect):
        if value is None:
            return None
        elif isinstance(value, list):
            return [self.model_class.model_validate_json(item) for item in value]
        elif isinstance(value, dict):
            return {key: self.model_class.model_validate_json(item) for key, item in value.items()}
        return self.model_class.model_validate_json(value)


def pydantic_json_column(model_class: type[BaseModel]):
    return Column(PydanticJSONColumn(model_class))


def required_json_field(model_class: type[BaseModel]):
    return Field(..., sa_column=pydantic_json_column(model_class))


def optional_json_field(model_class: type[BaseModel]):
    return Field(None, sa_column=pydantic_json_column(model_class))
