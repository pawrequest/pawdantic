# from __future__ import annotations
from __future__ import annotations

import re
import typing as _t
import typing as _ty

import pydantic as _p
from pydantic import StringConstraints


def identifiers_only(v):
    # return v
    if isinstance(v, str):
        return ''.join([char if char.isidentifier() else '_' for char in v])
    return ''


def printable_only(v):
    # return v
    if isinstance(v, str):
        return ''.join([char if char.isprintable() else '_' for char in v])
    return ''


IdentStr = _t.Annotated[str, _p.BeforeValidator(identifiers_only)]
PrintableStr = _t.Annotated[str, _p.BeforeValidator(printable_only)]


def truncate_before(maxlength) -> _p.BeforeValidator:
    def _truncate(v):
        if v:
            if len(v) > maxlength:
                return v[:maxlength]
        return v

    return _p.BeforeValidator(_truncate)


def truncate_after(maxlength) -> _p.AfterValidator:
    def _truncate(v):
        if v:
            if len(v) > maxlength:
                return v[:maxlength]
        return v

    return _p.AfterValidator(_truncate)


def truncated_ident_str_type(max_length: int):
    return _ty.Annotated[IdentStr, _p.StringConstraints(max_length=max_length), truncate_before(max_length)]


def optional_truncated_ident_str_type(max_length: int):
    return _ty.Annotated[
        IdentStr, _p.StringConstraints(max_length=max_length), truncate_before(max_length), _p.Field('')
    ]


def truncated_printable_str_type(max_length: int):
    return _ty.Annotated[PrintableStr, _p.StringConstraints(max_length=max_length), truncate_before(max_length)]


def optional_truncated_printable_str_type(max_length: int):
    return _ty.Annotated[
        PrintableStr,
        _p.StringConstraints(max_length=max_length),
        truncate_before(max_length),
        _p.Field(
            default=None,
        ),
    ]


pc_excluded = {'C', 'I', 'K', 'M', 'O', 'V'}


def validate_uk_postcode(v: str):
    pattern = re.compile(r'([A-Z]{1,2}\d[A-Z\d]? ?\d[A-Z]{2})')
    if not re.match(pattern, v) and not set(v[-2:]).intersection(pc_excluded):
        raise _p.ValidationError('Invalid UK postcode')
    return v


def default_gen(typ, **kwargs):
    return _t.Annotated[typ, _p.Field(**kwargs)]


POSTCODE_PATTERN = r'([A-Z]{1,2}\d[A-Z\d]? ?\d[A-Z]{2})'
VALID_POSTCODE = _t.Annotated[
    str,
    _p.AfterValidator(validate_uk_postcode),
    _p.BeforeValidator(lambda s: s.strip().upper()),
    _p.Field(..., description='A valid UK postcode'),
]


def multi_model_dump(*models: _p.BaseModel) -> dict[str, str]:
    return {k: v for mod in list(models) for k, v in mod.model_dump(exclude_none=True).items()}


def get_initial_f_dict(*dicts: dict):
    dicts = list(dicts)
    return {k: v for d in dicts for k, v in d.items()}


def str_length_const(length: int):
    return _t.Annotated[str,
    StringConstraints(strip_whitespace=True, max_length=length),
    ]


ConvertMode = Literal['pydantic', 'python', 'python-alias', 'json', 'json-alias']


def pydantic_export(obj: BaseModel, mode: ConvertMode) -> dict | BaseModel | str:
    match mode:
        case 'pydantic':
            return obj
        case 'python':
            return obj.model_dump(mode='json', by_alias=False)
        case 'python-alias':
            return obj.model_dump(mode='json', by_alias=True)
        case 'json':
            return obj.model_dump_json(by_alias=False)
        case 'json-alias':
            return obj.model_dump_json(by_alias=True)
        case _:
            raise ValueError(f'Invalid ConvertMode: {mode}')

