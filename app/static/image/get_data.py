import requests
import json
import re
import pymysql
from datetime import datetime
from selenium import webdriver
import sys

class Mysql:
    def __init__(self):
        self.host = 'localhost'     # 数据库地址
        self.user = 'root'          # 数据库用户名
        self.pwd = 'root!@#$'       # 数据库密码
        self.database = 'movie'       # 数据库名

        self.conn()

    # 获取数据库连接
    def conn(self):
        self.db = pymysql.connect(self.host, self.user, self.pwd, self.database)
        self.db.set_charset('utf8')
        self.cursor = self.db.cursor()
        self.cursor.execute('SET CHARACTER SET utf8;')
        self.cursor.execute('SET character_set_connection=utf8;')

    # 插入数据
    def insert_link(self, data_list):
        print('插入链接数据.....')
        sql = "insert into link(name, url, size, share_date, movie_id) VALUES(%s,%s,%s,%s,%s)"

        self.cursor.executemany(sql,data_list)

    def insert_movie(self, data):
        print('插入电影数据.....')
        sql = "insert into movie(title, url, logo, length, performer, genre, release_time,addtime) VALUES(%s,%s,%s,%s,%s,%s,%s,%s)"

        self.cursor.execute(sql,data)
        return self.cursor.lastrowid

    def insert_image(self, data_list):
        print('插入图片数据')
        sql = "insert into image(name, url, movie_id) VALUES(%s, %s, %s)"

        self.cursor.executemany(sql, data_list)


    # 提交请求
    def commit(self):
        try:
            print('提交数据...')
            self.db.commit()
            print('提交成功....')
        except Exception as e:
            print('保存失败...:', e)

    # 关闭连接
    def close(self):
        self.cursor.close()
        print('关闭数据库连接')
        self.db.close()

class Movie:
    def __init__(self):
        option = webdriver.FirefoxOptions()
        option.set_headless()
        self.browser = webdriver.Firefox(firefox_options=option)
        self.mysql = Mysql()
        self.i = 0
        print('..............初始化次数。。。。。。。。。。。。。。。。')

    def conn(self, url):
        headers = {
            "accept": "application/json",
            "Content-Type": "application/json",
            'Connection': 'close'
        }
        resp = requests.get(url, headers=headers, verify=False)
        resp.close()
        return resp.text

    # 获取url链接
    def get_url(self, url):
        result = self.conn(url)
        url_list = re.findall('<a class="movie-box" href="(.*?)">', result)
        return url_list

    # 获取网页数据
    def get_data(self, url):
        self.browser.get(url)
        result = self.browser.page_source.replace('\r\n', '').replace('\n', '').replace('  ', '')
        self.browser.close()

        content = result.split('<div class="container">')[1]
        return content

    # 获取电影信息
    def get_movie(self, content):
        title = re.search('<h3>(.*)</h3>', content).group(1)
        genre = re.findall('<span class="genre"><a href=".*?/genre/.*?">(.*?)</a></span>',
                           content)
        genre = ','.join(genre)

        logo_url = re.search('<img src="(.*?)"', content).group(1)
        logo = requests.get(logo_url).content

        performers = re.findall(
            '<div class="star-name"><a href=".*?/.*?" title=".*?">(.*?)</a></div>', content)
        performer = ','.join(performers)

        length = re.search('<p><span class="header">長度:</span> (\w*)分鐘</p>', content).group(1)

        release_time = re.search('<p><span class="header">發行日期:</span> (.*?)</p>', content).group(1)

        return [title, title.split(' ')[0], logo, length, performer, genre, release_time, datetime.now()]

    # 获取连接信息
    def get_link(self, content, movie_id):
        links_content = re.findall("""<tr onmouseover.*?</tr>""", content)
        links = re.findall(
            """<tr onmouseover="this.style.backgroundColor='#F4F9FD';this.style.cursor='pointer';" onmouseout=.*?><td onclick="window.open(.*?)" width="70%"><a style="color:#333" rel="nofollow" title=.*? href=".*?">(.*?)</a></td><td style=.*? onclick="window.open.*?"><a style="color:#333" rel="nofollow" title=.*? href=.*?>(.*?)</a></td><td style=.*? onclick="window.open.*?"><a style="color:#333" rel="nofollow" title=".*?" href=".*?">(.*?)</a></td></tr>""",
            ''.join(links_content).replace('\t', ''))
        link_list = []
        for link in links:
            link_name = link[1].split(' ')[0][:50].split('<')[0]
            link_size = link[3].split('<')[0]
            link_share_time = link[2].split('<')[0]
            link_url = link[0].split(',')[0].split("'")[1]
            # print('link:', link_name, link_url, link_share_time, link_size)
            link_list.append([link_name, link_url, link_size, link_share_time, movie_id])

        return link_list

    # 获取图片信息
    def get_image(self, content, movie_id):
        images = re.findall('<div class="photo-frame"><img src="(.*?)" title="(.*?)"></div>', content)
        image_list = []
        for image in images:
            image_list.append([image[1], image[0], movie_id])
        return image_list

    def close(self):
        self.browser.quit()
        self.mysql.close()

    def main(self):
        print('start------------------------------')
        url_list = self.get_url('https://www.javbus.com')
        for url in url_list:
            self.i += 1
            print('get_data--------------------------,',self.i)
            if self.mysql.cursor.execute('select id from movie where url="%s"' % url):
                continue
            content = self.get_data(url)

            print('get_movie-------------------------')
            movie_data = self.get_movie(content)
            continue
            print('insert_movie-----------------------')
            movie_id = self.mysql.insert_movie(movie_data)

            print('get_link---------------------------')
            link_data = self.get_link(content, movie_id)
            if link_data:
                print('insert_link')
                try:
                    self.mysql.insert_link(link_data)
                except pymysql.err.DataError as e:
                    print(link_data)
                    print('链接插入失败')
                    self.close()
                    break

                except pymysql.err.InternalError as e:
                    print(link_data)
                    print('链接插入失败')
                    self.close()
                    break

            image_data = self.get_image(content, movie_id)
            if image_data:
                print('insert_image')
                self.mysql.insert_image(image_data)

            self.mysql.commit()

        self.close()

    def insert_image(self):
        self.mysql.cursor.execute('select id, url from movie')
        movies = self.mysql.cursor.fetchall()

        for movie in movies:
            self.i += 1
            print('start----------,',self.i)
            id = movie[0]
            url = movie[1]
            content = self.conn(url)
            image_data = self.get_image(content, id)
            if image_data:
                print('insert_image')
                try:
                    self.mysql.insert_image(image_data)
                except pymysql.err.IntegrityError as e:
                    print('图片已存在')
                    continue


            self.mysql.commit()

if __name__ == '__main__':
    movie = Movie()
    movie.main()



