import simplejson as json

from ..common.db import db
from sqlalchemy.dialects.mysql import INTEGER, DECIMAL, DOUBLE
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
    created_at = db.Column(
        db.DateTime, server_default=func.now(), nullable=False)
    updated_at = db.Column(
        db.DateTime, server_default=func.now(), onupdate=func.now(), nullable=False)

    def __init__(self, data):
        self.name = data.name
        self.sku = data.sku
        self.regular_price = data.regular_price
        self.discount_price = data.discount_price
        self.quantity = data.quantity
        self.description = data.description
        self.weight = data.weight
        self.note = data.note
        self.published = data.published

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def json(self):
        return {
            "id": self.id,
            "name": self.name,
            "sku": self.sku,
            "regular_price": json.dumps(self.regular_price),
            "discount_price": json.dumps(self.discount_price),
            "quantity": self.quantity,
            "description": self.description,
            "weight": json.dumps(self.weight),
            "note": self.note,
            "published": self.published,
            "created_at": json.dumps(self.created_at, default=str),
            "updated_at": json.dumps(self.updated_at, default=str)
        }
