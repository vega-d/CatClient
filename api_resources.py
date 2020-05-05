import parser

from flask import jsonify
from flask_restful import Resource

import service_func as sf
from data import db_session
from data.users import User
from data.settings import Settings


class Userlist(Resource):
    def get(self, token):
        """
        :return:
            {
              "users": [
                {"Veseha": "dir,dir,dir"},
                {"Lunar": "dir,dir,dir"}
              ]
            }
        """
        print('token', token)
        session = db_session.create_session()
        userlist = session.query(User).all()

        users = [(i.name, i.dirs) for i in userlist]
        ret = jsonify({'users': users})
        return ret


class Userget(Resource):
    def get(self, id_user, token):
        """
        :param id_user:
        :return:
        {
            "dirs": "dir,dir,dir"
        }
        """
        print('token', token)
        if user_found(id_user):
            return jsonify({"error": True})
        session = db_session.create_session()
        user = session.query(User).get(id_user)
        dirs_user = user.dirs
        return jsonify({'dirs': dirs_user})

    def post(self):
        """
        not work
        :return:
        """
        args = parser.parse_args()
        session = db_session.create_session()
        session.commit()
        return jsonify({'success': 'OK'})

    def delete(self, news_id):
        """
        not work
        :param news_id:
        :return:
        """
        user_found(news_id)
        session = db_session.create_session()
        session.commit()
        return jsonify({'success': 'OK'})


class Users(Resource):
    None


def user_found(id_user):
    session = db_session.create_session()
    user = session.query(User).get(id_user)
    if not user:
        return True
    return False


class Auth(Resource):
    def get(self, login, hash):
        session = db_session.create_session()
        user = session.query(User).filter(User.name == login).first()
        ret = {}
        if user and user.check_password(hash, is_hash=True):
            ret['error'] = 'OK'
        else:
            ret['error'] = 'WrongCredentials'
            return ret
        token = sf.get_token(login)
        if token:
            ret['token'] = token
        else:
            ret['error'] = 'NoToken'
        return ret

    def post(self):
        pass


class Tokens(Resource):
    def get(self):
        pass

    def post(self, login, hash):
        from service_func import generate_token
        session = db_session.create_session()
        print('one')
        user = session.query(User).filter(User.name == login, User.hashed_password == hash).first()
        print('two')
        if not user:
            return jsonify({"error": "CredentialError"})
        user_settings = session.query(Settings).filter(Settings.id == user.id)
        if user_settings.token:
            return jsonify({"error": "TokenAlreadyExists"})
        user_settings.token = generate_token()
        session.commit()
        return jsonify({"error": "OK"})
    # delete me
