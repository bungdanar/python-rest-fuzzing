from ..common.db import db
from sqlalchemy.dialects.mysql import INTEGER, DECIMAL, DOUBLE
from sqlalchemy import DateTime
from sqlalchemy.sql import func


class Product(db.Model):
    __tablename__ = "product"

    id = db.Column(INTEGER(unsigned=True), primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    sku = db.Column(db.String(255), nullable=False)
    regular_price = db.Column(
        DECIMAL(precision=19, scale=4, unsigned=True), nullable=False)
    discount_price = db.Column(
        DECIMAL(precision=19, scale=4, unsigned=True), nullable=False)
    quantity = db.Column(INTEGER(unsigned=True), nullable=False)
    description = db.Column(db.String(1000), nullable=False)
    weight = db.Column(DOUBLE(unsigned=True), nullable=False)
    note = db.Column(db.String(255), nullable=False)
    published = db.Column(db.Boolean, nullable=False, default=False)
    created_at = db.Column(DateTime(timezone=True),
                           nullable=False, server_default=func.now())
    updated_at = db.Column(DateTime(timezone=True),
                           nullable=False, onupdate=func.now())
