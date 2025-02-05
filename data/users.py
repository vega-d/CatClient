import datetime

import sqlalchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash

from .db_session import SqlAlchemyBase


class User(SqlAlchemyBase, UserMixin):
    __table_args__ = {'extend_existing': True}

    def set_password(self, password, is_hash=False):
        self.hashed_password = password if is_hash else generate_password_hash(password)

    def check_password(self, password, is_hash=False):
        if is_hash:
            import secrets
            return secrets.compare_digest(password, self.hashed_password)
        return self.check_password(self.hashed_password, is_hash=True)

    def __repr__(self):
        return '<User>' + ' ' + str(self.id) + ' ' + self.name

    __tablename__ = 'users'
    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    hashed_password = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    created_date = sqlalchemy.Column(sqlalchemy.DateTime,
                                     default=datetime.datetime.now)
    dirs = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    type_user = sqlalchemy.Column(sqlalchemy.String, nullable=False, default='user')


