from flask_restful import reqparse, abort, Api, Resource
from flask import Flask, render_template, redirect, request, make_response, session, abort, Blueprint, jsonify
import parser
from data import db_session
from data.users import User


class Files(Resource):
    def get(self):
        """
        :return:
            {
              "users": [
                {"Veseha": "dir,dir,dir"},
                {"Lunar": "dir,dir,dir"}
              ]
            }
        """
        session = db_session.create_session()
        user = session.query(User).all()
        users = {}
        for i in user:
            users[int(i.id)] = [i.name, i.dirs]
        return jsonify({'users': users})


class File(Resource):
    def get(self, id_user):
        """
        :param id_user:
        :return:
        {
            "dirs": "dir,dir,dir"
        }
        """
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
        # news = News(
        #     title=args['title'],
        #     content=args['content'],
        #     user_id=args['user_id'],
        #     is_published=args['is_published'],
        #     is_private=args['is_private']
        # )
        # session.add(news)
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
        # news = session.query(News).get(news_id)
        # session.delete(news)
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



