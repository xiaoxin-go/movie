import json
import os
import base64
from sqlalchemy.exc import IntegrityError
def to_json(data):
    if isinstance(data,list):
        return list(map(fun, data))
    else:
        return [fun(data)]

def fun(item):
    data = item.__dict__
    if '_sa_instance_state' in data:
        del data['_sa_instance_state']
    for key,value in data.items():
        if isinstance(value,bytes):
            print('key,value',key,value[:100])
            with open('test.jpg','wb') as f:
                f.write(value)
            data[key] = base64.b64encode(value).decode()
    return data

class Base:
    def __init__(self, request, Object, filters):
        self.request = request
        self.Object = Object
        self.filters = filters

    def exec(self):
        if self.request.method == 'GET':
            return self.get_data()

        if self.request.method == 'POST':
            return self.add_data()

        if self.request.method == 'PUT':
            return self.put_data()

        if self.request.method == 'DELETE':
            return self.del_data()

    def get_data(self):
        data = self.request.values
        print('----------------------------')
        print('data:',data)
        print('----------------------------')

        id = data.get('id')
        if id:
            query_filter = self.Object.filter_(self.Object.id, id).first()
            print('query_filter', query_filter)
            json_data = to_json(query_filter)
            return {'data': json_data}

        page = int(data.get('page'))
        page_size = int(data.get('page_size'))
        total = int(data.get('total'))
        keyword = data.get('keyword') or ''
        query_result = self.Object.filters_(keyword,self.filters).order_by('-id')
        if not total:
            total = query_result.count()
        print('tags:', query_result)
        print('total:', total)
        data_list = query_result[(page-1) * page_size: page * page_size]
        json_data = to_json(data_list)
        return {'data': json_data, 'total': total}

    def add_data(self):
        data = self.request.json
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
        print('put_data:',data)
        id = data.pop('id')
        try:
            state = self.Object.query.filter_by(id=id).update(data)
            self.Object.commit()
        except IntegrityError as e:
            print('%s: common,76, tag修改失败' % e)
            state = 2
        return {'state': state}

    def del_data(self):
        data = self.request.values
        id = data.get('id')
        state = self.Object.query.filter_by(id=id).delete()
        self.Object.commit()
        return {'state': state}