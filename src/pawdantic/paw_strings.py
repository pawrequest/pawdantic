from __future__ import annotations

from datetime import date


def get_ordinal_suffix(day: int) -> str:
    return {1: 'st', 2: 'nd', 3: 'rd'}.get(day % 10, 'th') if day not in (11, 12, 13) else 'th'


def date_string(date_: date) -> str:
    fstr = f'%A %#d{get_ordinal_suffix(date_.day)} %B'
    return f'{date_:{fstr}}'
