import datetime
import sqlalchemy
from werkzeug.security import generate_password_hash, check_password_hash
from .db_session import SqlAlchemyBase
from sqlalchemy import orm
from flask_login import UserMixin


class Settings(SqlAlchemyBase, UserMixin):
    def __repr__(self):
        return '<User>' + ' ' + str(self.id) + ' ' + self.name

    __tablename__ = 'users'
    id = sqlalchemy.Column(sqlalchemy.Integer,
                           sqlalchemy.ForeignKey("users.id"))
    theme = sqlalchemy.Column(sqlalchemy.String, nullable=True, default='dark')
    token = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    theme1 = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    theme2 = sqlalchemy.Column(sqlalchemy.String, nullable=True)


