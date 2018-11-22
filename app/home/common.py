import os
from flask import Blueprint, flash, redirect, render_template, request, session, url_for, jsonify, Response
from sqlalchemy.exc import IntegrityError
from app.models import *
from app.base import *

# 获取电影数据
class Movie_(Base):
    def get_data(self):
        data = self.request.values

        page = int(data.get('page'))
        page_size = int(data.get('page_size'))
        keyword = data.get('keyword')
        total = int(data.get('total'))
        if keyword:
            query_result = self.Object.filters_(keyword,self.filters)
        else:
            query_result = Movie.query.filter(Movie.title != None, Movie.is_delete == 1)
        if not total:
            total = query_result.count()
        print('tags:', query_result)
        print('total:', total)
        data_list = query_result[(page-1) * page_size: page * page_size]
        print('return data...')
        json_data = to_json(data_list)
        return {'data': json_data, 'total': total}

# 收藏
class Moviecol_(Base):
    def get_data(self):
        data = request.values
        #user_id = session.get('home_user_id')
        print(data)
        username = data.get('username')

        total = int(data.get('total'))
        page = int(data.get('page'))
        page_size = int(data.get('page_size'))

        user = User.query.filter_by(name=username).first()
        if not user:
            return {}

        moviecols = Moviecol.query.filter_by(user_id=user.id)
        movie_ids = list(map(lambda item: item.movie_id, moviecols))
        movies = Movie.query.filter(Movie.id.in_(movie_ids))
        if not total:
            total = len(movie_ids)
        data_list = movies[(page-1)*page_size:page*page_size]
        json_data = to_json(data_list)
        return {'data': json_data, 'total': total}

    def add_data(self):
        #user_id = session.get('home_user_id')
        data = request.json
        username = data.get('username')
        user = User.query.filter_by(name=username).first()
        if not user:
            return {'state': 0}

        movie_id = data.get('id')
        moviecol = Moviecol(movie_id=movie_id, user_id=user.id)
        moviecol.save()

        return {'state':1}

    def del_data(self):
        user_id = session.get('home_user_id')
        data = request.values
        movie_id = int(data.get('id'))

        state = Moviecol.query.filter_by(user_id=user_id, movie_id=movie_id).delete()
        db.session.commit()
        return {'state':state}

# 关注
class Follow_(Base):
    def get_data(self):
        data = self.request.values
        print(data)
        #user_id = session.get('home_user_id')

        total = int(data.get('total'))
        page = int(data.get('page'))
        page_size = int(data.get('page_size'))
        username = data.get('username')

        user = User.query.filter_by(name=username).first()

        follows = Follow.query.filter_by(user_id=user.id)
        performer_ids = list(map(lambda item:item.performer_id, follows))
        if not total:
            total = len(performer_ids)
        performers = Performer.query.filter(Performer.id.in_(performer_ids))
        data_list = performers[(page-1)*page_size:page*page_size]
        json_data = to_json(data_list)
        return {'data': json_data, 'total': total}

    def add_data(self):
        data = request.json

        username = data.get('username')
        user = User.query.filter_by(name=username).first()
        #user_id = session.get('home_user_id')
        if not user:
            return {'state': 0}

        data = request.json
        print('data:', data)

        performer_id = data.get('id')
        follow = Follow(performer_id=performer_id, user_id=user.id)
        follow.save()

        return {'state':1}

    def del_data(self):
        #user_id = session.get('home_user_id')
        data = request.values
        username = data.get('username')
        user = User.query.filter_by(name=username).first()
        movie_id = int(data.get('id'))

        state = Moviecol.query.filter_by(user_id=user.id, movie_id=movie_id).delete()
        db.session.commit()
        return {'state':state}