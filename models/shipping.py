from common.db import db
from sqlalchemy.dialects.mysql import INTEGER, DECIMAL
from sqlalchemy.sql import func


class ShippingModel(db.Model):
    __tablename__ = "shipping"

    id = db.Column(INTEGER(unsigned=True), primary_key=True)
    description = db.Column(db.String(1000), nullable=False)
    charge = db.Column(
        DECIMAL(precision=19, scale=4, unsigned=True, asdecimal=False), nullable=False)
    free = db.Column(db.Boolean, nullable=False, default=False)
    estimated_days = db.Column(INTEGER(unsigned=True), nullable=False)
    product_id = db.Column(INTEGER(unsigned=True), db.ForeignKey(
        "product.id"), nullable=False)
    created_at = db.Column(
        db.DateTime, server_default=func.now(), nullable=False)
    updated_at = db.Column(
        db.DateTime, server_default=func.now(), onupdate=func.now(), nullable=False)

    product = db.relationship("ProductModel", back_populates="shippings")
