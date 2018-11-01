from flask import Blueprint, flash, redirect, render_template, request, session, url_for, jsonify, Response
from werkzeug.security import check_password_hash
from app.models import *
from app.home.common import *
bp = Blueprint('home', __name__, url_prefix='/home')    # 创建蓝图

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
            session.clear()                         # 清除session信息
            session['home_user_id'] = user['id']        # 设置session user_id 为用户ID
            return jsonify({'state':1,'data':to_json(user)})       # 返回项目主页

        return jsonify({'state':state})

# 退出登录
@bp.route('/logout', methods=['POST',])
def logout():
    if request.method == 'POST':
        session.clear()  # 清空session信息
        return jsonify({'state': 1})

# 注册用户
@bp.route('/register/')
def register():
    return render_template('')

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
    movie = Movie.filter_(Movie.title, title).first()

    # 获取电影链接和截图信息
    image = movie.images
    links = movie.links

    base_data = to_json(movie)
    image_data = to_json(image)
    link_data = to_json(links)
    return jsonify({'base_data':base_data, 'data': image_data, 'links': link_data})

# 获取角色信息
@bp.route('/performer', methods=['GET',])
def performer():
    data = request.values
    print('----------------------------')
    print('data:', data)
    print('----------------------------')

    page = int(data.get('page'))
    page_size = int(data.get('page_size'))
    total = int(data.get('total'))

    # 获取所有角色信息
    query_result = Performer.query

    if not total:
        total = query_result.count()

    print('tags:', query_result)
    print('total:', total)

    data_list = query_result[(page-1)*page_size:page*page_size]
    json_data = to_json(data_list)
    return jsonify({'data': json_data, 'total': total})

# 查看角色详细信息
@bp.route('/performer/detail', methods=['GET',])
def performer_detail():
    data = request.values
    name = data.get('name')
    page = int(data.get('page'))
    page_size = int(data.get('page_size'))
    total = int(data.get('total'))

    # 查询当前角色信息
    performer = Performer.filter_(Performer.name, name).first()
    base_data = to_json(performer)

    # 查询与角色相关的电影信息
    movies = Movie.filter_(Movie.performer, name)
    if not total:
        total = movies.count()

    data_list = movies[(page-1) * page_size: page * page_size]
    json_data = to_json(data_list)

    return jsonify({'base_data': base_data, 'data': json_data, 'total': total})

# 根据类别搜索
@bp.route('/genre', methods=['GET',])
def genre():
    data = request.values
    genre = data.get('genre')
    page = int(data.get('page'))
    page_size = int(data.get('page_size'))
    total = int(data.get('total'))

    # 获取相关类别的电影信息
    movies = Movie.filter_(Movie.genre, genre)
    if total:
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
    ids = data.get('ids')
    movies = Movie.query.filter(Movie.id.in_(ids))
    movies.update({'state':0},synchronize_session=False)
    db.session.commit()

    return jsonify({'state':1})
