import sqlalchemy
from flask_login import UserMixin

from .db_session import SqlAlchemyBase


class Settings(SqlAlchemyBase, UserMixin):
    def __repr__(self):
        return '<Settings>' + ' ' + str(self.id)

    __tablename__ = 'settings'
    id_settings = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    id = sqlalchemy.Column(sqlalchemy.Integer,
                           sqlalchemy.ForeignKey("users.id"))
    theme = sqlalchemy.Column(sqlalchemy.String, nullable=True, default='dark')
    token = sqlalchemy.Column(sqlalchemy.String, nullable=True)


