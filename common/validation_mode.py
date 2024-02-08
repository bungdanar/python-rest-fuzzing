from enum import Enum


class ValidationMode(Enum):
    NO = 'no'
    MA_PARTIAL = 'ma-partial'
    MA_FULL = 'ma-full'
    PYDANTIC_PARTIAL = 'pydantic-partial'
    PYDANTIC_FULL = 'pydantic-full'
