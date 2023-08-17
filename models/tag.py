from common.db import db
from sqlalchemy.dialects.mysql import INTEGER
from sqlalchemy.sql import func


class TagModel(db.Model):
    __tablename__ = "tag"

    id = db.Column(INTEGER(unsigned=True), primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    created_at = db.Column(
        db.DateTime, server_default=func.now(), nullable=False)
    updated_at = db.Column(
        db.DateTime, server_default=func.now(), onupdate=func.now(), nullable=False)
