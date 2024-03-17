# from __future__ import annotations
from __future__ import annotations

import re
import typing as _t
import typing as _ty

import pydantic as _p


def validate_str(v):
    # return v
    if v:
        v = v.replace(r'/', '')
    return v or ''


SafeStr = _ty.Annotated[str, _p.BeforeValidator(validate_str)]


def truncate_before(maxlength) -> _p.BeforeValidator:
    def _truncate(v):
        if v:
            if len(v) > maxlength:
                return v[:maxlength]
        return v

    return _p.BeforeValidator(_truncate)


def TruncatedSafeStr(max_length: int):
    return _ty.Annotated[SafeStr, _p.StringConstraints(max_length=max_length), truncate_before(max_length)]


def TruncatedSafeMaybeStr(max_length: int):
    return _ty.Annotated[
        SafeStr, _p.StringConstraints(max_length=max_length), truncate_before(max_length), _p.Field('')
    ]


excluded_chars = {'C', 'I', 'K', 'M', 'O', 'V'}


def validate_uk_postcode(v: str):
    pattern = re.compile(r'([A-Z]{1,2}\d[A-Z\d]? ?\d[A-Z]{2})')
    if not re.match(pattern, v) and not set(v[-2:]).intersection(excluded_chars):
        raise _p.ValidationError('Invalid UK postcode')
    return v


def is_valid_postcode(s):
    pattern = re.compile(r'([A-Z]{1,2}\d[A-Z\d]? ?\d[A-Z]{2})')
    return bool(re.match(pattern, s))


ValidPostcode = _ty.Annotated[str, _p.BeforeValidator(validate_uk_postcode), _p.BeforeValidator(lambda v: v.upper())]


def default_gen(typ, **kwargs):
    return _t.Annotated[typ, _p.Field(**kwargs)]
