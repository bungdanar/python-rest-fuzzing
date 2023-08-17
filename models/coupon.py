from common.db import db
from sqlalchemy.dialects.mysql import INTEGER, DECIMAL
from sqlalchemy.sql import func


class CouponModel(db.Model):
    __tablename__ = "coupon"

    id = db.Column(INTEGER(unsigned=True), primary_key=True)
    code = db.Column(db.String(255), nullable=False)
    description = db.Column(db.String(1000), nullable=False)
    discount_value = db.Column(DECIMAL(precision=5, scale=2,
                                       unsigned=True), nullable=False)
    discount_type = db.Column(db.String(255), nullable=False)
    times_used = db.Column(INTEGER(unsigned=True), nullable=False)
    max_usage = db.Column(INTEGER(unsigned=True), nullable=False)
    start_date = db.Column(db.DateTime, nullable=False)
    end_date = db.Column(db.DateTime, nullable=False)
    created_at = db.Column(
        db.DateTime, server_default=func.now(), nullable=False)
    updated_at = db.Column(
        db.DateTime, server_default=func.now(), onupdate=func.now(), nullable=False)

    products = db.relationship(
        "ProductModel", back_populates="coupons", secondary="product_coupon")
