import pymysql

"""
mysql模块封装思路
mysql = Mysql(table_name)
1. 数据查询
    输入查询键值对，默认为查询所有，like为模糊查询
    返回 {data:datalist, count:1}
    mysql.query({id:1,name:test}, like=True)
    
2. 数据添加
    可输入单个数据，或者数据列表
    mysql.insert({id:1,name:test}) or mysql.insert([{id:1},{id:2}])
    
3. 数据更新
    输入筛选条件和要更新数据字典
    返回更新条数
    mysql.update({id:1}, {name:new_test}, like=False)
    
4. 数据删除
    输入筛选条件，默认为精确删除
    返回删除条件
    mysql.delete({id:1})
    
"""


class Mysql:
    def __new__(cls, table):
        if not hasattr(cls, 'instance'):
            host = 'localhost'      # 数据库地址
            user = 'root'           # 数据库用户名
            pwd = 'root!@#$'        # 数据库密码
            database = 'movie'      # 数据库名
            cls.mysql = pymysql.connect(host, user, pwd, database)
            cls.mysql.set_charset('utf8')
            cls.cursor = cls.mysql.cursor()
            cls.cursor.execute('SET CHARACTER SET utf8;')
            cls.cursor.execute('SET character_set_connection=utf8;')

            cls.instance = super(Mysql, cls).__new__(cls)
        return cls.instance

    def __init__(self, table):
        self.table = table

    # 获取当前表字段名
    def get_keys(self):
        self.cursor.execute('desc ' + self.table)
        result = self.cursor.fetchall()
        self.keys = list(map(lambda item: item[0], result))

    # 查询数据， 默认查询所有数据, 默认为精确查询
    def query(self, data ,like=False):
        self.get_keys()
        if not data:
            sql = 'select * from %s' % self.table
        else:
            key_value = ''
            for key, value in data.items():
                if like:
                    key_value += '%s like "%%%s%%" and ' % (key, value)
                else:
                    key_value += '%s="%s" and ' % (key,value)
            sql = 'select * from %s where %s' % (self.table, key_value[:-5])

        count = self.cursor.execute(sql)
        if count:
            result = self.cursor.fetchall()
            data_list = list(map(lambda item: dict(zip(self.keys, item)), result))
            return {'data': data_list, 'count': count}
        else:
            return {}

    # 更新数据，输入old_data: 筛选条件， data: 更新的数据， 返回更新条数
    def update(self, old_data, data, like=False):
        old_key_value = ''
        for key, value in old_data.items():
            if like:
                old_key_value += '%s like "%%%s%%" and ' % (key,value)
            else:
                old_key_value += '%s="%s",' % (key, value)

        key_value = ''
        for key, value in data.items():
            key_value += '%s="%s" and ' % (key, value)

        sql = 'update %s set %s where %s' % (self.table, key_value[:-5], old_key_value[:-1])
        count = self.cursor.execute(sql)
        self.commit()
        return count

    # 插入数据， 接收单个或多个插入
    def insert(self, data, commit=True):
        keys = ''
        values = ''

        # 多条数据插入
        if isinstance(data, list):
            for key in data[0].keys():
                keys += key + ','
                values += '%s,'
            value_list = list(map(lambda item:list(item.values()), data))
            sql = 'insert into ' + self.table + '(' + keys[:-1] + ')' + ' VALUES(' + values[:-1] + ')'
            count = self.executemany(sql, value_list)
            if commit:
                self.commit()
            return {'count': count}

        # 单个数据插入，返回单个数据
        elif isinstance(data, dict):
            key_value = ''
            value_data = []
            for key, value in data.items():
                keys += key + ','
                values += '%s,'
                value_data.append(value)
                key_value += '%s="%s" ' % (key, value)
            sql = 'insert into ' + self.table + '(' + keys[:-1] + ')' + ' VALUES(' + values[:-1] + ')'

            self.execute(sql, value_data)
            if commit:
                self.commit()

                self.get_keys()

                # 获取表当前插入数据
                sql = 'select * from %s where %s' % (self.table, key_value)
                self.execute(sql)
                result_data = self.fetchone()

                # 返回当前插入的数据信息
                return dict(zip(self.keys, result_data))
            return self.cursor.lastrowid
        else:
            return '请输入正确数据格式'

    # 删除
    def delete(self, data, like=False):
        key_value = ''
        for key,value in data.items():
            if like:
                key_value = '%s like "%%%s%%" and ' % (key,value)
            else:
                key_value = '%s="%s" and ' % (key,value)
        sql = 'delete from %s where %s' % (self.table, key_value)
        count = self.execute(sql)
        self.commit()
        return count

    def execute(self, sql ,data=None):
        if data:
            return self.cursor.execute(sql, data)
        else:
            return self.cursor.execute(sql)

    def executemany(self, sql ,data):
        return self.cursor.executemany(sql ,data)

    def fetchone(self):
        return self.cursor.fetchone()

    def fetchall(self):
        return self.cursor.fetchall()

    def commit(self):
        self.mysql.commit()

    def close(self):
        self.mysql.close()

    def __del__(self):
        self.mysql.close()
