import os
from sqlalchemy.exc import IntegrityError
from app.base import *
from app.models import *

class Movie_(Base):
    def add_data(self):
        data = self.request.json
        print(data)
        logo = data.get('logo')
        file = ''
        if logo:
            filename = logo.split('\\')[-1]
            f = open(filename, 'rb')
            file = f.read()
            f.close()
            os.remove(filename)

        data['logo'] = file

        tag = self.Object(**data)
        state = 1
        try:
            tag.save()
        except IntegrityError as e:
            print('%s:common.py,56' % e)
            state = 2
        #json_data = to_json(tag.search())
        return {'state': state}

    def put_data(self):
        data = self.request.json
        print('data:',data)
        logo = data.get('logo')
        file = None
        if logo:
            filename = logo.split('\\')[-1]
            f = open(filename, 'rb')
            file = f.read()
            f.close()
        data['logo'] = file

        id = data.pop('id')
        try:
            state = self.Object.query.filter_by(id=id).update(data)
        except IntegrityError as e:
            print('%s: common,76, tag修改失败' % e)
            state = 2
        return {'state': state}

    def del_data(self):
        data = self.request.values
        print(data)
        ids = data.get('id_list[]')

        for id in json.loads(ids):
        # 删除电影
            movie = Movie.query.get(id)

            # 删除电影相关图片，链接
            Link.query.filter_by(movie_id=id).delete()
            Image.query.filter_by(movie_id=id).delete()

            db.session.delete(movie)
        db.session.commit()
        return {'state': 1}

class Performer_(Movie_):
    def del_data(self):
        data = self.request.values
        ids = data.get('id_list[]')

        for id in json.loads(ids):
            performer = Performer.query.get(id)

            # 删除演员的电影
            movies = Movie.query.filter_by(performer=performer.name)
            for movie in movies:
                # 删除电影连接图片
                Link.query.filter_by(movie_id=movie.id).delete()
                Image.query.filter_by(movie_id=movie.id).delete()
            movies.delete()
            db.session.delete(performer)
        db.session.commit()

        return {'state': 1}