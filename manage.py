from app import app
from flask_script import Manager,Server
from app.models import Tag
from app import db
import socket

server_ip = socket.gethostbyname(socket.gethostname())

manager = Manager(app)
manager.add_command('start', Server(host=server_ip, port=80))
@manager.command
def dev():                      # 执行 python Sample.py dev   更新文件时，会自动重启服务器
    from livereload import Server
    live_server = Server(app)
    live_server.watch('**/*.*')
    live_server.serve()

@manager.command
def add():
    tag = Tag(name = '战争')
    #tag.save()
    #db.session.add(tag)
    print(Tag.query.filter(Tag.name=='战争').first())
    tag = tag.search()
    db.session.commit()

@manager.command
def get():
    tag = Tag.query.all()
    print(tag[0])

if __name__ == '__main__':
    manager.run()
