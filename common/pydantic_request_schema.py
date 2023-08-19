from decimal import Decimal
from typing import Optional

from pydantic import BaseModel


class ProductCreatePartialPydanticValidation(BaseModel):
    name: str
    sku: str
    regular_price: Decimal
    discount_price: Decimal
    quantity: int
    description: str
    weight: Decimal
    note: str
    published: bool = False
