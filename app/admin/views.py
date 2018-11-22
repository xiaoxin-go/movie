from flask import Blueprint, flash, redirect, render_template, request, session, url_for, jsonify, Response
from werkzeug.security import check_password_hash
from app.models import *
from app.admin.common import to_json, Base, Movie_, Performer_

bp = Blueprint('admin', __name__, url_prefix='/admin')  # 创建蓝图

import pymysql

def get_conn():
    return pymysql.connect('localhost','root','xiaoxin','movie')

@bp.route('/')
def index():
    return render_template('admin/index.html')

@bp.route('/menu', methods=['GET',])
def menu():
    query_list = Auth.query.all()
    json_data = to_json(query_list)
    return jsonify(json_data)

# 标签管理
@bp.route('/tag', methods=['GET', 'POST', 'PUT', 'DELETE'])
def tag():
    # 获取数据
    filters = [Tag.name]
    data = Base(request, Tag, filters).exec()
    return jsonify(data)

# 电影管理
@bp.route('/movie', methods=['GET', 'POST', 'PUT', 'DELETE'])
def movie():
    filters = [Movie.title, Movie.info]
    data = Movie_(request, Movie, filters).exec()
    return jsonify(data)

# 预告管理
@bp.route('/preview', methods=['GET', 'POST', 'PUT', 'DELETE'])
def preview():
    filters = [Preview.title]
    data = Movie_(request, Preview, filters).exec()
    return jsonify(data)

# 会员管理
@bp.route('/user', methods=['GET', 'PUT', 'DELETE'])
def user():
    filters = [User.name, User.email, User.phone, User.info]
    data = Base(request, User, filters).exec()
    return jsonify(data)

# 评论管理
@bp.route('/comment', methods=['GET', 'DELETE'])
def comment():
    filters = [Comment.content]
    data = Base(request, Comment, filters).exec()
    return jsonify(data)

# 收藏管理
@bp.route('/moviecol', methods=['GET', 'PUT', 'DELETE'])
def moviecol():
    filters = [Movie.title, User.name]
    data = Base(request, Moviecol, filters).exec()
    return jsonify(data)

# 日志管理
@bp.route('/log', methods=['GET', 'POST', 'PUT', 'DELETE'])
def log():
    if request.method == 'GET':
        pass

    if request.method == 'POST':
        pass

    if request.method == 'PUT':
        pass

    if request.method == 'DELETE':
        pass

# 权限管理
@bp.route('/auth', methods=['GET', 'POST', 'PUT', 'DELETE'])
def auth():
    filters = [Auth.name, Auth.url]
    data = Base(request, Auth, filters).exec()
    return jsonify(data)


# 角色管理
@bp.route('/role', methods=['GET', 'POST', 'PUT', 'DELETE'])
def role():
    filters = [Role.name]
    data = Base(request, Role, filters).exec()
    return jsonify(data)

# 管理员管理
@bp.route('/admin', methods=['GET', 'POST', 'PUT', 'DELETE'])
def admin():
    filters = [Admin.name]
    data = Base(request, Admin, filters).exec()
    return jsonify(data)

# 演员管理
@bp.route('/performer', methods=['GET', 'POST', 'PUT', 'DELETE'])
def performer():
    filters = [Performer.name]
    data = Performer_(request, Performer, filters).exec()
    return jsonify(data)

# 修改电影封面
@bp.route('/performerlogo', methods=['PUT',])
def performerlogo():
    data = request.json
    id = data.get('id')
    movie_id = data.get('movie_id')
    movie = Movie.query.filter_by(id=movie_id).first()
    performer = Performer.query.filter_by(id=id).first()
    title = movie.title.split(' ')[0]
    import os
    print(os.getcwd())
    movie_file = open(r'F:\httpd-2.4.37-win64-VC15\Apache24\htdocs\image\movie\%s' % title + '\\' + title + '.jpg','rb')
    text = movie_file.read()
    movie_file.close()

    with open(r'F:\httpd-2.4.37-win64-VC15\Apache24\htdocs\image\performer\%s' % performer.name + '.jpg','wb') as f:
        f.write(text)
    performer.save()
    print(performer.name)
    return jsonify({'state':1})

# 管理员登录
@bp.route('/login', methods=('GET', 'POST'))
def login():                        # 登录函数
    if request.method == 'POST':
        username = request.form['username']         # 获取用户名
        password = request.form['password']         # 获取密码
        error = None
        user = db.execute(
            'SELECT * FROM user WHERE username = ?', (username,)    # 查询用户信息
        ).fetchone()

        if user is None:
            error = 'Incorrect username'
        elif not check_password_hash(user['password'], password):   # 检查用户密码是否一致
            error = 'Incorrect password.'

        if error is None:       # 若用户名和密码相同
            session.clear()                         # 清除session信息
            session['admin_user_id'] = user['id']        # 设置session user_id 为用户ID
            return redirect(url_for('index'))       # 返回项目主页

        flash(error)

    return render_template('auth/login.html')       # 否则返回登录页面

# 退出登录
@bp.route('/logout', methods=['POST',])
def logout():
    if request.method == 'POST':
        session.clear()  # 清空session信息
        return redirect(url_for('index'))

# 上传图片
@bp.route('/upload_logo', methods=['POST'])
def upload_logo():
    if request.method == 'POST':
        print('files:',request.files)
        file = request.files.get('file')


        print(file.__dict__)
        filename = file.filename
        content = file.read()
        with open(filename, 'wb') as f:
            f.write(content)

        print(filename)
        import base64

        return Response(base64.b64encode(content))

@bp.route('/logo',methods=['GET'])
def get_image():
    with open('logo.jpg', 'rb') as f:
        image = f.read()
        return Response(image, mimetype='image/jpeg')