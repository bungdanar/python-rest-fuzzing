from common.db import db
from sqlalchemy.dialects.mysql import INTEGER
from sqlalchemy.sql import func


class CategoryModel(db.Model):
    __tablename__ = "category"

    id = db.Column(INTEGER(unsigned=True), primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.String(1000), nullable=False)
    active = db.Column(db.Boolean, nullable=False, default=True)
    created_at = db.Column(
        db.DateTime, server_default=func.now(), nullable=False)
    updated_at = db.Column(
        db.DateTime, server_default=func.now(), onupdate=func.now(), nullable=False)

    products = db.relationship(
        "ProductModel", back_populates="categories", secondary="product_category")
