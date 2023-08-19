from decimal import Decimal
from typing import List

from pydantic import BaseModel, Field, model_validator, ConfigDict, constr


class ProductCreatePartialPydanticValidation(BaseModel):
    model_config = ConfigDict(extra='forbid')

    name: str
    sku: str
    regular_price: Decimal
    discount_price: Decimal
    quantity: int
    description: str
    weight: Decimal
    note: str
    published: bool = False


class CategoryCreatePartialPydanticValidation(BaseModel):
    model_config = ConfigDict(extra='forbid')

    name: str
    description: str


class ProductTagCategoryCreatePartialPydanticValidation(ProductCreatePartialPydanticValidation):
    tags: List[str] = Field(min_length=1)
    category: CategoryCreatePartialPydanticValidation


class ProductCreateFullPydanticValidation(BaseModel):
    model_config = ConfigDict(extra='forbid')

    name: str = Field(max_length=255)
    sku: str = Field(max_length=255)
    regular_price: Decimal = Field(ge=0, max_digits=19, decimal_places=4)
    discount_price: Decimal = Field(ge=0, max_digits=19, decimal_places=4)
    quantity: int = Field(ge=0, le=9999)
    description: str = Field(max_length=1000)
    weight: Decimal = Field(ge=0, le=1000, max_digits=8, decimal_places=4)
    note: str = Field(max_length=255)
    published: bool = False

    @model_validator(mode='after')
    def validate_max_discount_price(self) -> 'ProductCreateFullPydanticValidation':
        if self.discount_price > self.regular_price:
            raise ValueError(
                'discount_price must be less than or equal to regular_price')

        return self


class CategoryCreateFullPydanticValidation(BaseModel):
    model_config = ConfigDict(extra='forbid')

    name: str = Field(max_length=255)
    description: str = Field(max_length=1000)


class ProductTagCategoryCreateFullPydanticValidation(ProductCreateFullPydanticValidation):
    tags: List[constr(max_length=255)] = Field(min_length=1)
    category: CategoryCreateFullPydanticValidation
