import sqlalchemy
from pydantic import BaseModel
from sqlmodel import Column, Field


# class JSONColumn(sqlalchemy.TypeDecorator):
#     impl = sqlalchemy.JSON
#
#     def __init__(self, model_class: type[BaseModel], *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         self.model_class = model_class
#
#     def process_bind_param(self, value, dialect):
#         return value.model_dump_json(round_trip=True) if value is not None else None
#
#     def process_result_value(self, value, dialect):
#         return self.model_class.model_validate_json(value) if value else None
#
#
# class PydanticJSONColumn(sqlalchemy.TypeDecorator):
#     impl = sqlalchemy.JSON
#
#     def __init__(self, model_class: type[BaseModel], *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         self.model_class = model_class
#
#     def process_bind_param(self, value, dialect):
#         if isinstance(value, list):
#             logger.warning(f'Binding list ({self.model_class})')
#             return [v.model_dump_json(round_trip=True) for v in value]
#         if isinstance(value, BaseModel):
#             logger.warning(f'Binding model ({self.model_class})')
#             return value.model_dump_json(round_trip=True) if value else None
#         logger.warning(f'wrong type to bind ({type(value)})')
#
#     def process_result_value(self, value, dialect):
#         if isinstance(value, list):
#             if all(isinstance(v, BaseModel) for v in value):
#                 logger.warning(f'Processing list ({self.model_class})')
#                 return [self.model_class.model_validate_json(v) for v in value]
#             logger.warning(f'wrong type in list to process ({self.model_class})')
#         if isinstance(value, BaseModel):
#             logger.warning(f'Processing model ({self.model_class})')
#             return self.model_class.model_validate_json(value) if value else None
#         logger.warning(f'wrong type to bind ({type(value)})')
#
#     # def process_bind_param(self, value, dialect):
#     #     # if isinstance(value, dict):
#     #     #     logger.warning(f'Binding dict ({self.model_class})')
#     #     #     return value
#     #     # if isinstance(value, list):
#     #     #     logger.warning(f'Binding list ({self.model_class})')
#     #     #     return [v.model_dump_json(round_trip=True) for v in value]
#     #     # if isinstance(value, BaseModel):
#     #     logger.warning(f'Binding model ({self.model_class})')
#     #     return value.model_dump_json(round_trip=True) if value else None
#     #
#     # def process_result_value(self, value, dialect):
#     #     # if isinstance(value, dict):
#     #     #     logger.warning(f'Processing dict ({self.model_class})')
#     #     #     return self.model_class.model_validate(value) if value else None
#     #     # if isinstance(value, list):
#     #     #     logger.warning(f'Processing list ({self.model_class})')
#     #     #     return [self.model_class.model_validate(v) for v in value]
#     #     logger.warning(f'Processing model ({self.model_class})')
#     #     return self.model_class.model_validate_json(value) if value else None
#
#
# def pydantic_json_column(model_class: type[BaseModel]):
#     return Column(PydanticJSONColumn(model_class))
#
#
# def required_json_field(model_class: type[BaseModel]):
#     return Field(..., sa_column=pydantic_json_column(model_class))
#
#
# def optional_json_field(model_class: type[BaseModel]):
#     return Field(None, sa_column=pydantic_json_column(model_class))
#
# def optional_json_list_field(model_class: type[BaseModel]):
#     return Field(None, sa_column=pydantic_json_column(model_class))
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
