from common.db import db
from sqlalchemy.dialects.mysql import INTEGER
from sqlalchemy.sql import func


class AddressModel(db.Model):
    __tablename__ = "address"

    id = db.Column(INTEGER(unsigned=True), primary_key=True)
    street = db.Column(db.String(255), nullable=False)
    city = db.Column(db.String(255), nullable=False)
    country = db.Column(db.String(255), nullable=False)
    postal_code = db.Column(db.String(5), nullable=False)
    user_id = db.Column(INTEGER(unsigned=True), db.ForeignKey(
        "user.id"), nullable=False)
    created_at = db.Column(
        db.DateTime, server_default=func.now(), nullable=False)
    updated_at = db.Column(
        db.DateTime, server_default=func.now(), onupdate=func.now(), nullable=False)

    user = db.relationship("UserModel", back_populates="addresses")
