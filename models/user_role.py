from common.db import db
from sqlalchemy.sql import func


class UserRoleModel(db.Model):
    __tablename__ = "user_role"

    user_id = db.Column(db.Integer, db.ForeignKey(
        "user.id"), primary_key=True, autoincrement=False, nullable=False)
    role_id = db.Column(db.Integer, db.ForeignKey(
        "role.id"), primary_key=True, autoincrement=False, nullable=False)
    created_at = db.Column(
        db.DateTime, server_default=func.now(), nullable=False)
    updated_at = db.Column(
        db.DateTime, server_default=func.now(), onupdate=func.now(), nullable=False)

    user = db.relationship("UserModel", back_populates="user_roles")
