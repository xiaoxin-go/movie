from datetime import datetime
from sqlalchemy import or_
from app import db

db.metadata.clear()

class DB:
    def save(self):
        db.session.add(self)
        db.session.commit()

    @staticmethod
    def commit():
        db.session.commit()

    # 单个精确查询方法
    def search(self):
        data = self.__dict__
        data.pop('_sa_instance_state')
        return self.query.filter_by(**data).first()

    # 单个模糊查询方法
    @classmethod
    def filter_(cls, key, keyword):
        return cls.query.filter(key.like("%{}%".format(keyword)))

    # 多个模糊查询方法
    @classmethod
    def filters_(cls, keyword, filters):
        print(filters)
        data_list = []
        for filter in filters:
            data_list.append(filter.like("%{}%".format(keyword)))
        return cls.query.filter(or_(*data_list))


# 会员
class User(db.Model,DB):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True)  # 编号
    name = db.Column(db.String(100), unique=True)  # 昵称
    pwd = db.Column(db.String(100))  # 密码
    email = db.Column(db.String(100), unique=True)  # 邮箱
    phone = db.Column(db.String(11), unique=True)  # 手机号码
    info = db.Column(db.Text)  # 个性简介
    face = db.Column(db.String(255), unique=True)  # 头像
    #state = db.Column(db.Integer, default=1)                   # 状态
    addtime = db.Column(db.DateTime, index=True, default=datetime.now)  # 注册时间
    uuid = db.Column(db.String(255), unique=True)  # 唯一标志符
    userlogs = db.relationship('Userlog', backref='user')  # 会员日志外键关系关联
    comments = db.relationship('Comment', backref='user')  # 评论外键关系关联
    moviecols = db.relationship('Moviecol', backref='user')  # 收藏外键关系关联

    def __repr__(self):
        return "<User %r>" % self.name

    def check_pwd(self, pwd):
        from werkzeug.security import check_password_hash
        return check_password_hash(self.pwd, pwd)


# 会员登录日志
class Userlog(db.Model,DB):
    __tablename__ = "userlog"
    id = db.Column(db.Integer, primary_key=True)  # 编号
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))  # 所属会员
    ip = db.Column(db.String(100))  # 登录IP
    addtime = db.Column(db.DateTime, index=True, default=datetime.now)  # 登录时间

    def __repr__(self):
        return "<Userlog %r>" % self.id

# 标签
class Tag(db.Model,DB):
    __tablename__ = 'tag'
    id = db.Column(db.Integer, primary_key=True)    # 编号
    name = db.Column(db.String(100), unique=True)   # 标签名
    addtime = db.Column(db.DateTime, index=True, default=datetime.now)   # 添加时间
    movies = db.relationship("Movie", backref='tag')    # 电影信息

    def __repr__(self):
        return "<Tag %r>" % self.name

movie_performer = db.Table('movie_performer',
    db.Column('movie_id', db.Integer, db.ForeignKey('movie.id')),
    db.Column('performer_id', db.Integer, db.ForeignKey('performer.id'))
)

# 电影
class Movie(db.Model,DB):
    __tablename__ = 'movie'
    id = db.Column(db.Integer, primary_key=True)    # 编号
    title = db.Column(db.String(255), unique=True)  # 标题
    url = db.Column(db.String(255), unique=True)    # 地址
    info = db.Column(db.Text)                       # 简介
    #logo = db.Column(db.LargeBinary)   # 封面
    genre = db.Column(db.String(255))
    star = db.Column(db.SmallInteger)               # 星级
    playnum = db.Column(db.BigInteger)              # 播放量
    commentnum = db.Column(db.BigInteger)           # 评论量
    tag_id = db.Column(db.Integer, db.ForeignKey('tag.id')) # 标签
    area = db.Column(db.String(255))                # 上映地区
    release_time = db.Column(db.Date)               # 上映时间
    length = db.Column(db.String(100))              # 播放长度
    addtime = db.Column(db.DateTime, index=True, default=datetime.now)   # 添加时间
    performer = db.Column(db.String(500))           # 演员，以,分割
    state = db.Column(db.Integer)
    comments = db.relationship('Comment', backref='movie')
    moviecols = db.relationship('Moviecol', backref='movie')
    links = db.relationship('Link', backref='movie')
    images = db.relationship('Image', backref='movie')
    performers = db.relationship('Performer', secondary=movie_performer, backref='movie')

    def __repr__(self):
        return '<Movie %r>' % self.title

    __mapper_args__ = {
        "order_by": release_time.desc()
    }

# 演员表
class Performer(db.Model,DB):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))    # 演员名
    age = db.Column(db.SmallInteger)    # 年龄
    birthday = db.Column(db.Date)       # 生日
    height = db.Column(db.SmallInteger) # 身高
    cup = db.Column(db.String(10))      # 大小
    bust = db.Column(db.SmallInteger)   # 上
    waist = db.Column(db.SmallInteger)  # 中
    hips = db.Column(db.SmallInteger)   # 下
    hometown = db.Column(db.String(255))    # 出生地
    hobby = db.Column(db.String(100))   # 兴趣
    #image = db.Column(db.LargeBinary)          # 头像
    #movies = db.relationship('Movie', backref='performer')

    def __repr__(self):
        return '<Performer %r>' % self.name




# 链接表
class Link(db.Model,DB):
    __tablename__ = 'link'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    url = db.Column(db.Text)
    size = db.Column(db.String(20))
    share_date = db.Column(db.Date)
    movie_id = db.Column(db.Integer, db.ForeignKey('movie.id'))
    def __repr__(self):
        return '<Link %r>' % self.name

# 图片表
class Image(db.Model,DB):
    __tablename__ = 'image'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    url = db.Column(db.String(255))
    movie_id = db.Column(db.Integer, db.ForeignKey('movie.id'))

# 预告
class Preview(db.Model,DB):
    __tablename__ = 'preview'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), unique=True)
    logo = db.Column(db.LargeBinary)
    addtime = db.Column(db.DateTime, index=True, default=datetime.now)

    def __repr__(self):
        return '<Preview %r>' % self.title

# 评论
class Comment(db.Model,DB):
    __tablename__ = 'comment'
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text)
    movie_id = db.Column(db.Integer, db.ForeignKey('movie.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    addtime = db.Column(db.DateTime, index=True, default=datetime.now)

    def __repr__(self):
        return '<Comment %r>' % self.id

# 收藏
class Moviecol(db.Model,DB):
    __tablename__ = 'moviecol'
    id = db.Column(db.Integer, primary_key=True)
    movie_id = db.Column(db.Integer, db.ForeignKey('movie.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    addtime = db.Column(db.DateTime, index=True, default=datetime.now)

    def __repr__(self):
        return '<Moviecol %r>' % self.id

# 收藏
class Follow(db.Model,DB):
    __tablename__ = 'follow'
    id = db.Column(db.Integer, primary_key=True)
    performer_id = db.Column(db.Integer)
    user_id = db.Column(db.Integer)
    addtime = db.Column(db.DateTime, index=True, default=datetime.now)

    def __repr__(self):
        return '<Follow %r>' % self.id

# 权限
class Auth(db.Model,DB):
    __tablename__ = 'auth'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True)
    url = db.Column(db.String(255), unique=True)
    type = db.Column(db.SmallInteger)
    image = db.Column(db.String(100))
    addtime = db.Column(db.DateTime, index=True, default=datetime.now)

    def __repr__(self):
        return '<Auth %r>' % self.name

# 角色
class Role(db.Model,DB):
    __tablename__ = 'role'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True)
    auths = db.Column(db.String(600))               # 权限ID列表
    addtime = db.Column(db.DateTime, index=True, default=datetime.now)
    
    def __repr__(self):
        return '<Role %r>' % self.name

# 管理员
class Admin(db.Model,DB):
    __tablename__ = 'admin'
    id = db.Column(db.Integer, primary_key=True)  # 编号
    name = db.Column(db.String(100), unique=True)  # 昵称
    pwd = db.Column(db.String(100))
    is_super = db.Column(db.SmallInteger)           # 是否为超级管理员
    role_id = db.Column(db.Integer, db.ForeignKey('role.id'))
    addtime = db.Column(db.DateTime, index=True, default=datetime.now)
    adminlogs = db.relationship('Adminlog', backref='admin')
    oplogs = db.relationship('Oplog', backref='admin')

    def __repr__(self):
        return '<Admin %r>' % self.name

# 登录日志
class Adminlog(db.Model,DB):
    __tablename__ = 'adminlog'
    id = db.Column(db.Integer, primary_key=True)
    admin_id = db.Column(db.Integer, db.ForeignKey('admin.id'))
    ip = db.Column(db.String(100))          # 登录IP
    addtime = db.Column(db.DateTime, index=True, default=datetime.now)

    def __repr__(self):
        return '<Adminlog %r>' % self.id

# 操作日志
class Oplog(db.Model,DB):
    __tablename__ = 'oplog'
    id = db.Column(db.Integer, primary_key=True)
    admin_id = db.Column(db.Integer, db.ForeignKey('admin.id'))
    ip = db.Column(db.String(100))
    reason = db.Column(db.String(600))      # 操作原因
    addtime = db.Column(db.DateTime, index=True, default=datetime.now)

    def __repr__(self):
        return '<Oplog %r>' % self.id

#if __name__ == '__main__':
    #db.metadata.clear()
    db.create_all()
    # role = Role(
    #     id = 1,
    #     name = '超级管理员',
    #     auths=''
    # )
    # from werkzeug.security import generate_password_hash
    # admin = Admin(
    #     name='xiaoxin',
    #     pwd=generate_password_hash('xiaoxin'),
    #     is_super=0,
    #     role_id=1
    # )
    # db.session.add(role)
    # db.session.commit()
    # tag = Tag(
    #     name = '武侠'
    # )
    # db.session.add(tag)
    # #
    # db.session.commit()
    