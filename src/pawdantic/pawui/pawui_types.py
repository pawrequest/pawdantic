from __future__ import annotations

import typing as _t

import pydantic as _p
from fastui import components as c

ModalType = tuple[c.Button, c.Modal]
AlertType = _t.Literal['ERROR', 'WARNING', 'NOTIFICATION', 'INFO']

AlertDict = _t.Annotated[dict[str, AlertType], _p.Field(default_factory=dict)]
