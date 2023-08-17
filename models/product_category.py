from common.db import db
from sqlalchemy.sql import func


class ProductCategoryModel(db.Model):
    __tablename__ = "product_category"

    product_id = db.Column(db.Integer, db.ForeignKey(
        "product.id"), primary_key=True, autoincrement=False, nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey(
        "category.id"), primary_key=True, autoincrement=False, nullable=False)
    created_at = db.Column(
        db.DateTime, server_default=func.now(), nullable=False)
    updated_at = db.Column(
        db.DateTime, server_default=func.now(), onupdate=func.now(), nullable=False)
