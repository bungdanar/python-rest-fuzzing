from ..common.db import db
from sqlalchemy.dialects.mysql import INTEGER


class Product(db.Model):
    __tablename__ = "product"

    id = db.Column(INTEGER(unsigned=True), primary_key=True)
