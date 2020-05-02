from flask_restful import reqparse, abort, Api, Resource
from flask import Flask, render_template, redirect, request, make_response, session, abort, Blueprint, jsonify
import parser
from data import db_session
from data.users import User


class Files(Resource):
    def get(self):
        session = db_session.create_session()
        user = session.query(User).all()
        return jsonify({'Users': [item.to_dict(only=('title', 'content', 'user.name')) for item in user]})

    def post(self):
        args = parser.parse_args()
        session = db_session.create_session()
        news = News(
            title=args['title'],
            content=args['content'],
            user_id=args['user_id'],
            is_published=args['is_published'],
            is_private=args['is_private']
        )
        session.add(news)
        session.commit()
        return jsonify({'success': 'OK'})


class File(Resource):
    def delete(self, news_id):
        abort_if_news_not_found(news_id)
        session = db_session.create_session()
        news = session.query(News).get(news_id)
        session.delete(news)
        session.commit()
        return jsonify({'success': 'OK'})


class Users(Resource):
    None


def abort_if_news_not_found(news_id):
    session = db_session.create_session()
    news = session.query(News).get(news_id)
    if not news:
        abort(404, message=f"News {news_id} not found")


