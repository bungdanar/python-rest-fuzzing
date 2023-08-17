from common.db import db
from sqlalchemy.sql import func


class ProductCouponModel(db.Model):
    __tablename__ = "product_coupon"

    product_id = db.Column(db.Integer, db.ForeignKey(
        "product.id"), primary_key=True, autoincrement=False, nullable=False)
    coupon_id = db.Column(db.Integer, db.ForeignKey(
        "coupon.id"), primary_key=True, autoincrement=False, nullable=False)
    created_at = db.Column(
        db.DateTime, server_default=func.now(), nullable=False)
    updated_at = db.Column(
        db.DateTime, server_default=func.now(), onupdate=func.now(), nullable=False)
