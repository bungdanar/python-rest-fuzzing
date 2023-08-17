from common.db import db
from sqlalchemy.dialects.mysql import INTEGER, DECIMAL
from sqlalchemy.sql import func


class ProductModel(db.Model):
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
    weight = db.Column(DECIMAL(precision=8, scale=4,
                       unsigned=True), nullable=False)
    note = db.Column(db.String(255), nullable=False)
    published = db.Column(db.Boolean, nullable=False, default=False)
    created_at = db.Column(
        db.DateTime, server_default=func.now(), nullable=False)
    updated_at = db.Column(
        db.DateTime, server_default=func.now(), onupdate=func.now(), nullable=False)

    tags = db.relationship(
        "TagModel", back_populates="products", secondary="product_tag")

    categories = db.relationship(
        "CategoryModel", back_populates="products", secondary="product_category")
