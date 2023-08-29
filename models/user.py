from common.db import db
from sqlalchemy.dialects.mysql import INTEGER
from sqlalchemy.sql import func


class UserModel(db.Model):
    __tablename__ = "user"

    id = db.Column(INTEGER(unsigned=True), primary_key=True)
    first_name = db.Column(db.String(255), nullable=False)
    last_name = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), nullable=False)
    phone_code = db.Column(db.String(3), nullable=False)
    phone_number = db.Column(db.String(12), nullable=False)
    created_at = db.Column(
        db.DateTime, server_default=func.now(), nullable=False)
    updated_at = db.Column(
        db.DateTime, server_default=func.now(), onupdate=func.now(), nullable=False)

    roles = db.relationship(
        "RoleModel", back_populates="users", secondary="user_role")
    user_roles = db.relationship("UserRoleModel", back_populates="user")
