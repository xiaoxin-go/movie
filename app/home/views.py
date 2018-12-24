import socket
from flask import Blueprint, flash, redirect, render_template, request, stream_with_context,session, url_for, jsonify, Response
from werkzeug.security import check_password_hash,generate_password_hash
from app.models import *
from sqlalchemy import or_, and_
import random
from app.home.common import *
bp = Blueprint('home', __name__, url_prefix='/home')    # 创建蓝图


@bp.route('/server', methods=['GET'])
def server():
    return jsonify({'server':'http://%s:8000' % socket.gethostbyname(socket.gethostname())})

@bp.route('/', methods=['GET'])
def index():
    print('....................................')
    return render_template('home/index.html')

# 用户登录
@bp.route('/login', methods=('GET', 'POST'))
def login():                        # 登录函数
    if request.method == 'POST':
        data = request.json
        username = data.get('username')         # 获取用户名
        password = data.get('password')         # 获取密码

        user = User.query.filter_by(name=username).first()

        if user is None:
            state = 0
        elif not check_password_hash(user.pwd, password):   # 检查用户密码是否一致
            state = 2
        else:
            #session.clear()                         # 清除session信息
            #session['home_user_id'] = user.id        # 设置session user_id 为用户ID
            return jsonify({'state':1,'data':to_json(user)})       # 返回项目主页

        return jsonify({'state':state})

# 退出登录
@bp.route('/logout', methods=['POST',])
def logout():
    if request.method == 'POST':
        session.clear()  # 清空session信息
        return jsonify({'state': 1})

# 获取用户信息
"""
1. 判断session中是否存在用户ID
2. 若不存在则直接返回状态值为0
3. 否则从session中取出用户ID
4. 根据用户ID取出用户信息返回到页面
"""
@bp.route('/user', methods=['GET'])
def user():
    if request.method == 'GET':
        user_id = session.get('home_user_id')
        if not user_id:
            return jsonify({'state':0})

        user = User.query.get(user_id)
        return jsonify({'state':1, 'data':to_json(user)})

# 用户名检查
@bp.route('/check_user', methods=['GET'])
def check_user():
    if request.method == 'GET':
        req_data = request.values
        name = req_data.get('name')
        if User.query.filter_by(name=name).count():
            state = 0
        else:
            state = 1
        return jsonify({'state':state})

# 注册用户
"""
1. 获取注册用户账号信息
2. 将用户注册信息存入数据库
3. 返回注册状态
"""
@bp.route('/register/', methods=['POST'])
def register():
    req_data = request.json
    req_data['pwd'] = generate_password_hash(req_data.get('pwd'))
    if User.query.filter_by(name=req_data.get('name')).count():
        return jsonify({'state': 2})

    print(req_data)

    user = User(**req_data)
    user.save()

    return jsonify({'state':1})


# 获取电影信息
@bp.route('/movie', methods=['GET',])
def movie():
    filters = [Movie.title, Movie.info]
    data = Movie_(request, Movie, filters).exec()
    return jsonify(data)

# 获取电影详细信息
@bp.route('/movie/detail', methods=['GET',])
def movie_detail():
    data = request.values
    title = data.get('title')
    print('title:',title)

    # 获取电影信息
    movie = Movie.filter_like(Movie.title, title).first()

    # 获取电影链接和截图信息
    images = Image.query.filter_by(movie_id=movie.id).all()
    links = Link.query.filter_by(movie_id=movie.id).all()
    #print(images)

    genres = movie.genre.split(',')
    genre_counts = list(range(len(genres)))
    l1 = random.choice(genre_counts)
    genre_counts.remove(l1)
    l2 = random.choice(genre_counts)

    other_movie = Movie.query.filter(Movie.genre.like('%{}%'.format(genres[l1]))
                                          ,Movie.genre.like('%{}%'.format(genres[l2])),Movie.id != movie.id,Movie.is_delete==1)[:6]


    base_data = to_json(movie)
    image_data = to_json(images)
    #print(image_data)
    link_data = to_json(links)


    other_data = to_json(other_movie)
    result = {'base_data':base_data, 'data': image_data, 'links': link_data, 'other_data': other_data}
    #print(result)
    print('get_movie_detail end...')
    return jsonify(result)

# 获取角色信息
@bp.route('/performer', methods=['GET',])
def performer():
    data = request.values

    print('get_performer...')
    page = int(data.get('page'))
    page_size = int(data.get('page_size'))
    total = int(data.get('total'))

    # 获取所有角色信息
    query_result = Performer.query.filter(Performer.is_delete==1)

    if not total:
        total = query_result.count()

    print('total:', total)

    data_list = query_result[(page-1)*page_size:page*page_size]
    json_data = to_json(data_list)
    print('get_performer end...')
    return jsonify({'data': json_data, 'total': total})

# 获取角色信息
@bp.route('/performers', methods=['GET',])
def performers():
    data = request.values

    print('get_performer...')
    page = int(data.get('page'))
    page_size = int(data.get('page_size'))
    total = int(data.get('total'))

    # 获取所有角色信息
    query_result = Performer.query.filter(Performer.is_delete==0)

    if not total:
        total = query_result.count()

    print('total:', total)

    data_list = query_result[(page-1)*page_size:page*page_size]
    json_data = to_json(data_list)
    print('get_performer end...')
    return jsonify({'data': json_data, 'total': total})

# 从回收站还原
@bp.route('/restore', methods=['POST',])
def restore():
    data = request.json
    ids = data.get('id_list[]')
    print(ids)
    ids = json.loads(ids)
    if isinstance(ids, list):
        performers = Performer.query.filter(Performer.id.in_(ids))
        performer_names = list(map(lambda item: item.name, performers))
        Movie.query.filter(Movie.performer.in_(performer_names)).update({'is_delete': 1}, synchronize_session=False)
        performers.update({'is_delete': 1}, synchronize_session=False)
    else:
        performer = Performer.query.get(ids)
        Movie.query.filter_by(performer=performer.name).update({'is_delete': 1})
        performer.is_delete = 1

    db.session.commit()
    print('delete end...')
    return {'state': 1}

# 查看角色详细信息
@bp.route('/performer/detail', methods=['GET',])
def performer_detail():
    data = request.values
    name = data.get('name')
    page = int(data.get('page'))
    page_size = int(data.get('page_size'))
    total = int(data.get('total'))

    # 查询当前角色信息
    print(data)
    print(name)
    #performer = Performer.filter_like(Performer.name, name).first()
    performer = Performer.query.filter(Performer.name==name).first()
    print(performer)

    base_data = to_json(performer)

    # 查询与角色相关的电影信息
    #movies = Movie.filter_like(Movie.performer, name)
    if performer.is_delete:
        movies = Movie.query.filter(or_(Movie.performer.like("%%,%s,%%" % name),Movie.performer.like("%s,%%" % name),Movie.performer.like("%%,%s" % name),Movie.performer==name),Movie.is_delete==1)
    else:
        movies = Movie.query.filter(Movie.performer.like("%%%s%%" % name), Movie.is_delete == 0)
    if not total:
        total = movies.count()

    data_list = movies[(page-1) * page_size: page * page_size]
    json_data = to_json(data_list)

    return jsonify({'base_data': base_data, 'data': json_data, 'total': total})

# 根据类别搜索
@bp.route('/genre', methods=['GET',])
def genre():
    data = request.values
    print('genre',data)
    key_data = json.loads(data.get('data'))

    key = list(key_data.keys())[0]
    value = list(key_data.values())[0]

    filter_key = {'genre': Movie.genre, 'series': Movie.series, 'vender': Movie.vender, 'studio': Movie.studio}

    page = int(data.get('page'))
    page_size = int(data.get('page_size'))
    total = int(data.get('total'))

    # 获取相关类别的电影信息
    movies = Movie.filter_like(filter_key[key], value).filter(Movie.is_delete==1)
    if not total:
        total = movies.count()
    data_list = movies[(page-1) * page_size: page * page_size]
    json_data = to_json(data_list)
    return jsonify({'data': json_data, 'total': total})

# 添加收藏
@bp.route('moviecol', methods=['GET','POST','DELETE'])
def moviecol():
    data = Moviecol_(request, Movie, []).exec()
    return jsonify(data)

# 添加关注
@bp.route('follow', methods=['GET','POST','DELETE'])
def follow():
    data = Follow_(request, Movie, []).exec()
    return jsonify(data)


# 改变状态，用于后面爬取封面
@bp.route('change_state', methods=['POST'])
def change_state():
    data = request.json
    print(data)
    ids = data.get('id_list')
    movies = Movie.query.filter(Movie.id.in_(ids))
    movies.update({'state':0},synchronize_session=False)
    db.session.commit()
    print('change_state end...')
    return jsonify({'state':1})
