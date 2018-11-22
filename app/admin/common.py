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
        print('del movie...')
        ids = data.get('id_list[]')
        id = data.get('id')
        if ids:
            Movie.query.filter(Movie.id.in_(json.loads(ids))).update({'is_delete':0},synchronize_session=False)

        if id:
            Movie.query.filter_by(id=id).update({'is_delete':0})

        db.session.commit()
        return {'state': 1}

class Performer_(Movie_):
    def del_data(self):
        data = self.request.values
        ids = data.get('id_list[]')
        print(ids)
        ids = json.loads(ids)
        if isinstance(ids,list):
            performers = Performer.query.filter(Performer.id.in_(ids))
            performer_names = list(map(lambda item: item.name, performers))
            Movie.query.filter(Movie.performer.in_(performer_names)).update({'is_delete': 0}, synchronize_session=False)
            performers.update({'is_delete': 0}, synchronize_session=False)
        else:
            performer = Performer.query.get(ids)
            Movie.query.filter_by(performer=performer.name).update({'is_delete':0})
            performer.is_delete = 0

        db.session.commit()
        print('delete end...')
        return {'state': 1}