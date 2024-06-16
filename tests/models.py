from enum import StrEnum
from pydantic import BaseModel
from sqlalchemy import Column
from sqlmodel import Field, SQLModel

from pawdantic.pawsql import optional_json_field, required_json_field, PydanticJSONColumn


class AlertType(StrEnum):
    ERROR = 'ERROR'
    WARNING = 'WARNING'
    NOTIFICATION = 'NOTIFICATION'


class Alert(BaseModel):
    code: int | None = None
    message: str
    type: AlertType = AlertType.NOTIFICATION

    @classmethod
    def from_exception(cls, e: Exception):
        return cls(message=str(e), type=AlertType.ERROR)

    def __hash__(self):
        return hash(self.model_dump_json())


class TestModel(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    alert: Alert = Field(..., sa_column=Column(PydanticJSONColumn(Alert)))
    alerts_list: list[Alert] = Field(default_factory=list, sa_column=Column(PydanticJSONColumn(Alert)))
    alerts_dict: dict[str, Alert] = Field(default_factory=dict, sa_column=Column(PydanticJSONColumn(Alert)))
    alerts_tuple: tuple[Alert, ...] = Field(default=(), sa_column=Column(PydanticJSONColumn(Alert)))


class TestModelRequiredJson(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    alert: Alert = required_json_field(Alert)
    alerts_list: list[Alert] = required_json_field(Alert)
    alerts_dict: dict[str, Alert] = required_json_field(Alert)
    alerts_tuple: tuple[Alert, ...] = required_json_field(Alert)


class TestModelOptionalJson(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    alert: Alert = optional_json_field(Alert)
    alerts_list: list[Alert] = optional_json_field(Alert)
    alerts_dict: dict[str, Alert] = optional_json_field(Alert)
    alerts_tuple: tuple[Alert, ...] = optional_json_field(Alert)
