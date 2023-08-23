from decimal import Decimal
from datetime import datetime, date
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


class CouponCreatePartialPydanticValidation(BaseModel):
    model_config = ConfigDict(extra='forbid')

    code: str
    description: str
    discount_value: Decimal
    discount_type: str
    times_used: int = 0
    max_usage: int
    start_date: datetime | date
    end_date: datetime | date


class ProductTagCategoryCreatePartialPydanticValidation(ProductCreatePartialPydanticValidation):
    tags: List[str] = Field(min_length=1)
    category: CategoryCreatePartialPydanticValidation


class ProductTagCategoryCouponCreatePartialPydanticValidation(ProductCreatePartialPydanticValidation):
    tags: List[str] = Field(min_length=1)
    categories: List[CategoryCreatePartialPydanticValidation] = Field(
        min_length=1)
    coupons: List[CouponCreatePartialPydanticValidation] = Field(min_length=1)


class ProductCreateFullPydanticValidation(BaseModel):
    model_config = ConfigDict(extra='forbid')

    name: str = Field(min_length=3, max_length=255)
    sku: str = Field(min_length=3, max_length=255)
    regular_price: Decimal = Field(ge=0, max_digits=19, decimal_places=4)
    discount_price: Decimal = Field(ge=0, max_digits=19, decimal_places=4)
    quantity: int = Field(ge=0, le=9999)
    description: str = Field(min_length=3, max_length=1000)
    weight: Decimal = Field(ge=0, le=1000, max_digits=8, decimal_places=4)
    note: str = Field(min_length=3, max_length=255)
    published: bool = False

    @model_validator(mode='after')
    def validate_max_discount_price(self) -> 'ProductCreateFullPydanticValidation':
        if self.discount_price > self.regular_price:
            raise ValueError(
                'discount_price must be less than or equal to regular_price')

        return self


class CategoryCreateFullPydanticValidation(BaseModel):
    model_config = ConfigDict(extra='forbid')

    name: str = Field(min_length=3, max_length=255)
    description: str = Field(min_length=3, max_length=1000)


class CouponCreateFullPydanticValidation(BaseModel):
    model_config = ConfigDict(extra='forbid')

    code: str = Field(min_length=3, max_length=255)
    description: str = Field(min_length=3, max_length=1000)
    discount_value: Decimal = Field(
        ge=0, le=100, max_digits=5, decimal_places=2)
    discount_type: str = Field(min_length=3, max_length=255)
    times_used: int = Field(ge=0, default=0)
    max_usage: int = Field(ge=0)
    start_date: datetime | date
    end_date: datetime | date

    @model_validator(mode='after')
    def validate_max_times_used(self) -> 'CouponCreateFullPydanticValidation':
        if self.times_used > self.max_usage:
            raise ValueError(
                'times_used must be less than or equal to max_usage')

        return self

    @model_validator(mode='after')
    def validate_min_end_date(self) -> 'CouponCreateFullPydanticValidation':
        if self.end_date < self.start_date:
            raise ValueError(
                'end_date must be greater than or equal to start_date')

        return self


class ProductTagCategoryCreateFullPydanticValidation(ProductCreateFullPydanticValidation):
    tags: List[constr(min_length=3, max_length=255)] = Field(min_length=1)
    category: CategoryCreateFullPydanticValidation


class ProductTagCategoryCouponCreateFullPydanticValidation(ProductCreateFullPydanticValidation):
    tags: List[constr(min_length=3, max_length=255)] = Field(min_length=1)
    categories: List[CategoryCreateFullPydanticValidation] = Field(
        min_length=1)
    coupons: List[CouponCreateFullPydanticValidation] = Field(min_length=1)
