import requests
from bs4 import BeautifulSoup as bsp
from mysql import *
import os

def get_conn(url):
    resp = requests.get(url)
    content = resp.content
    resp.close()
    return content

class Performer:
    def __init__(self, base_url):
        self.base_url = base_url
        self.x = 1

    def get_urls(self):
        # 从主页面获取所有子页面的URL
        html = get_conn(self.base_url)
        soup = bsp(html, 'lxml')
        slider = soup.find('div',{'class':'slider'})
        new_home_box = soup.find_all('div',{'class':'new-home-box'})
        urls_obj = []
        for item in [slider] + new_home_box:
            urls_obj.extend(item.find_all('a'))

        permerfor_urls = map(lambda item: item.get('href'), urls_obj)
        return permerfor_urls

    def get_data(self, url):
        # 获取子页面内容
        html = get_conn(url)
        soup = bsp(html, 'lxml')

        # 获取主DIV
        main = soup.find('div',{'id':"content"})

        # 获取电影名称
        title = main.find('h1').text.split('][')[0][1:]

        if not os.path.exists('movie'):
            os.mkdir('movie')

        if not os.path.exists('movie/' + title):
            os.mkdir('movie/' + title)

        # 获取电影封面URL
        img_url = main.find('div',{'id':'poster_src'}).find('img').get('src')

        # 将电影封面保存到文件里
        img_text = get_conn(img_url)
        logo = title + '/' + img_url.split('/')[-1]
        with open('movie/' + logo, 'wb') as f:
            f.write(img_text)
        print('logo:',logo)
        # 获取电影演员信息
        info_obj = soup.find('div',{'id':'movie_info'}).text.split(' ')
        p_i_start = info_obj.index('主演:') + 1
        p_i_end = info_obj.index(list(filter(lambda item:':' in item, info_obj[p_i_start:]))[0])
        performer = ''.join(info_obj[p_i_start: p_i_end]).replace('/',',')

        # 获取电影类型
        g_i_start = info_obj.index('类型:') + 1
        g_i_end = info_obj.index(list(filter(lambda item: ':' in item, info_obj[g_i_start:]))[0])
        genre = ''.join(info_obj[g_i_start: g_i_end]).replace('/',',')

        # 获取电影长度
        l_i_start = info_obj.index('片长:') + 1
        l_i_end = info_obj.index(list(filter(lambda item: ':' in item, info_obj[l_i_start:]))[0])
        length = ''.join(info_obj[l_i_start: l_i_end]).replace('/',',')

        # 获取电影磁力链接信息
        links = []
        link_obj = main.find_all('div',{'id':'zdownload'})
        for link in link_obj:
            item = link.find('a')
            links.append({'name':item.get('title').split(' ')[1],'url':item.get('href')})

        # 获取电影截图信息， 将图片截取到本地，并将信息保存
        images = []
        image_obj = main.find('ul',{'class':'moviepic-img'}).find_all('img')
        for img in image_obj:
            img_url = img.get('src')
            image_text = get_conn(img_url)
            image_url = title + '/' + img_url.split('/')[-1]
            with open('movie/' + image_url ,'wb') as f:
                f.write(image_text)
            images.append({'name':img.get('alt'),'url':image_url})

        # 获取电影简介
        description = main.find('div',{'id':'movie_description'}).text

        return {'title': title, 'logo': logo, 'performer':performer, 'genre': genre, 'length': length, 'links': links, 'images': images, 'info': description, 'url': url}

    def main(self):
        urls = self.get_urls()
        mysql = Mysql('movie')
        for url in urls:
            mysql.table = 'movie'
            print('start--: ',self.x)
            self.x += 1
            query = mysql.query({'url': url})
            if query:
                print('跳过：', url)
                continue
            data = self.get_data(url)
            if mysql.query({'title':data.get('title')}):
                print('跳过：', url)
                continue
            images = data.pop('images')
            links = data.pop('links')

            print('插入数据----------')
            print(data)
            print('link', links)
            movie_id = mysql.insert(data, False)
            print('movie_id:', movie_id)
            mysql.table = 'link'
            for link in links:
                link['movie_id'] = movie_id

            for image in images:
                image['movie_id'] = movie_id
            mysql.insert(links, False)

            mysql.table = 'image'
            mysql.insert(images)

            print('插入完成----------')

performer = Performer('https://www.btdx8.com')
urls = performer.get_urls()
print(list(urls))
performer.main()