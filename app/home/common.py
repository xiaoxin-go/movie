import os
from flask import Blueprint, flash, redirect, render_template, request, session, url_for, jsonify, Response
from sqlalchemy.exc import IntegrityError
from app.models import *
from app.base import *
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
            query_result = Movie.query.filter(Movie.title != None)
        if not total:
            total = query_result.count()
        print('tags:', query_result)
        print('total:', total)
        data_list = query_result[(page-1) * page_size: page * page_size]
        print('return data...')
        json_data = to_json(data_list)
        return {'data': json_data, 'total': total}

class Moviecol_(Base):
    def get_data(self):
        data = self.request.values
        user_id = session.get('home_user_id')

        total = data.get('total')
        page = data.get('page')
        page_size = data.get('page_size')

        user = User.query.get(user_id)
        moviecols = user.moviecols
        if not total:
            total = len(moviecols)
        data_list = moviecols[(page-1)*page_size:page*page_size]
        json_data = to_json(map(lambda item: item.movie, data_list))
        return {'data': json_data, 'total': total}

    def add_data(self):
        user_id = session.get('home_user_id')
        if not user_id:
            return {'state': 0}

        data = request.json
        print('data:', data)

        movie_id = data.get('id')
        moviecol = Moviecol(movie_id=movie_id, user_id=user_id)
        moviecol.save()

        return {'state':1}

    def del_data(self):
        user_id = session.get('home_user_id')
        data = request.values
        movie_id = int(data.get('id'))

        state = Moviecol.query.filter_by(user_id=user_id, movie_id=movie_id).delete()
        db.session.commit()
        return {'state':state}

class Follow_(Base):
    def get_data(self):
        data = self.request.values
        user_id = session.get('home_user_id')

        total = data.get('total')
        page = data.get('page')
        page_size = data.get('page_size')

        follows = Follow.query.filter_by(user_id=user_id)
        performer_ids = list(map(lambda item:item.performer_id, follows))
        if not total:
            total = len(performer_ids)
        performers = Performer.query.filter(Performer.id.in_(performer_ids))
        data_list = performers[(page-1)*page_size:page*page_size]
        json_data = to_json(data_list)
        return {'data': json_data, 'total': total}

    def add_data(self):
        user_id = session.get('home_user_id')
        if not user_id:
            return {'state': 0}

        data = request.json
        print('data:', data)

        movie_id = data.get('id')
        moviecol = Moviecol(movie_id=movie_id, user_id=user_id)
        moviecol.save()

        return {'state':1}

    def del_data(self):
        user_id = session.get('home_user_id')
        data = request.values
        movie_id = int(data.get('id'))

        state = Moviecol.query.filter_by(user_id=user_id, movie_id=movie_id).delete()
        db.session.commit()
        return {'state':state}