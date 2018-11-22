import requests
from bs4 import BeautifulSoup as bsp
from mysql import *
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from urllib3.exceptions import ReadTimeoutError
import os

import socket
socket.setdefaulttimeout(30)

class Movie:
    def __init__(self, base_url=None):
        self.base_url = base_url
        self.x = 0
        option = webdriver.FirefoxOptions()
        option.set_headless()
        self.browser = webdriver.Firefox(firefox_options=option)
        self.browser.set_page_load_timeout(20)
        self.browser.set_script_timeout(20)

    def conn(self, url):
        resp = requests.get(url)
        content = resp.content
        resp.close()
        return content

    # 获取url链接
    def get_urls(self, url=None):
        html = self.conn(url or self.base_url)
        soup = bsp(html, 'lxml')
        urls = soup.find_all('a',{'class':'movie-box'})
        return map(lambda item: item.get('href'), urls)

    # 获取电影数据
    def get_data(self, url):
        print('get_start:',url.split('/')[-1])
        try:
            self.browser.get(url)
        except TimeoutException as e:
            print('连接超时...')
        print('get_down..........')
        html = self.browser.page_source
        #self.browser.close()
        print('close...........')
        soup = bsp(html, 'lxml')
        print('获取html...')
        main = soup.find('div',{'class':'container'})

        # 获取电影链接
        table = soup.find('table', {'id': 'magnet-table'})
        link_obj = table.find_all('tr')[1:]

        print('link_obj', len(link_obj))
        if not link_obj:
            return {}
        links = []
        for link in link_obj:
            tds = link.find_all('td')
            link_url = tds[0].find('a').get('href')
            link_name = tds[0].find('a').text.strip()
            link_size = tds[1].find('a').text.strip()
            link_date = tds[2].find('a').text.strip()
            links.append({'name': link_name, 'url': link_url, 'size': link_size, 'share_date': link_date})

        # 获取电影标题
        title = main.find('h3').text

        name = title.split(' ')[0]
        info = title.split(' ')[1]

        # 创建图片文件夹
        if not os.path.exists('movie'):
            os.mkdir('movie')

        if not os.path.exists('movie/' + name):
            os.mkdir('movie/' + name)

        # 获取电影图片
        image_url = main.find('a',{'class':'bigImage'}).get('href')
        image_text = self.conn(image_url)

        print('save logo...')
        # 保存图片
        logo = '%s/%s.jpg' % (name, name)
        with open('movie/' + logo, 'wb') as f:
            f.write(image_text)

        print('get info...')
        # 获取电影信息
        infos = main.find('div',{'class':'col-md-3 info'})
        headers = infos.find_all('span',{'class':'header'})

        # 获取发行时间
        release_time = headers[1].next_sibling

        # 获取电影长度
        length = headers[2].next_sibling

        # 获取电影类别
        genres = infos.find_all('span',{'class':'genre','onmouseout':''})
        genre = ','.join(map(lambda item: item.find('a').text, genres))

        print('get performer...')
        # 获取演员列表
        performers = infos.find_all('div',{'class':'star-name'})
        performer = ','.join(map(lambda item: item.find('a').text, performers))

        print('save image ...')
        # 获取电影截图
        images = []
        image_obj = main.find_all('a',{'class':'sample-box'})
        for image in image_obj:
            image_name = image.find('img').get('title')
            image_url = image.get('href')
            image_logo = '%s/%s' % (name, image_url.split('/')[-1])
            image_text = self.conn(image_url)

            # 保存图片
            with open('movie/' + image_logo, 'wb') as f:
                f.write(image_text)

            images.append({'url': image_logo, 'name': image_name})

        return {'title':name, 'url': url, 'logo': logo, 'genre': genre, 'info': info,
                'length': length, 'release_time': release_time, 'performer': performer,
                'links': links, 'images':images}

    def main(self, base_url):
        urls = self.get_urls(base_url)
        #mysql = Mysql('movie')
        for url in urls:
            self.mysql.table = 'movie'
            print('start--------------------------------------------: ',self.x)
            self.x += 1
            query = self.mysql.query({'url': url.split('/')[-1]}, like=True)
            if query:
                print('continue：', url.split('/')[-1])
                continue
            try:
                data = self.get_data(url)
            except ReadTimeoutError as e:
                print('time out:',url)
                continue

            if not data:
                print('not links，continue:' ,url)
                continue

            images = data.pop('images')
            links = data.pop('links')

            print('insert data')
            print('link', len(links))
            movie_id = self.mysql.insert(data, False)
            print('movie_id:', movie_id)
            self.mysql.table = 'link'
            for link in links:
                link['movie_id'] = movie_id

            for image in images:
                image['movie_id'] = movie_id

            print('insert links...')
            self.mysql.insert(links, False)

            if not images:
                self.mysql.commit()
            else:
                self.mysql.table = 'image'
                print('insert images...')
                self.mysql.insert(images)

            print('end---------------------------------------------')

    def exec(self):
        self.mysql = Mysql('performer')
        query = self.mysql.query({'url':''},True)
        performers = query.get('data')
        for performer in performers:
            url = performer.get('url')
            self.main(url)

if __name__ == '__main__':
    movie = Movie()
    movie.exec()



