import requests
from bs4 import BeautifulSoup
from mysql import *

def get_conn(url):
    resp = requests.get(url)
    content = resp.content
    resp.close()
    return content



class Bsp(BeautifulSoup):
    def __init__(self, html):
        BeautifulSoup.__init__(self, html, 'html.parser')


class Performer:
    def __init__(self, base_url):
        self.base_url = base_url
        self.x = 1

    def get_urls(self):
        html = get_conn(self.base_url)
        bs_obj = Bsp(html)
        bs_query = bs_obj.findAll("a", {"class": "avatar-box text-center"})
        permerfor_urls = map(lambda item: item.get('href'), bs_query)
        return permerfor_urls

    def get_data(self, url):
        html = get_conn(url)
        print('获取html....')
        bs_obj = Bsp(html)
        print('获取bs_obj对象....')
        bs = bs_obj.find("div", {"class": "photo-info"})
        info_title = ['birthday', 'age', 'height', 'cup', 'bust', 'waist', 'hips', 'hometown', 'hobby']
        info_title = {'生日':'birthday','年齡':'age','身高':'height','罩杯': 'cup','胸圍':'bust','腰圍':'waist', '臀圍':'hips','出生地': 'hometown','愛好':'hobby'}
        name = bs.find('span').text.strip()
        #infos = map(lambda item: item.text.split(':')[1].strip(), bs.findAll('p'))
        infos = bs.findAll('p')
        user = {'name': name, 'url':url}

        for info in infos:
            info = info.text.split(':')
            key = info[0].strip()
            value = info[1].strip()
            user[info_title.get(key)] = value


        #user = dict(zip(info_title, infos))


        image_urls = bs_obj.findAll('a', {'class': 'movie-box'})

        image_filter = list(filter(lambda item: name in item.text, image_urls))

        images_urls = list(sorted(image_filter, key=lambda item: item.findAll('date')[1].text))

        images_url = images_urls[0].find('date').text.strip()

        image_html = get_conn('https://www.javbus.com/' + images_url)
        bs_obj_image = Bsp(image_html)
        image_url = bs_obj_image.find('a', {'class': 'bigImage'}).get('href')
        image = get_conn(image_url)
        user['image'] = image
        return user

    def main(self):
        urls = self.get_urls()
        mysql = Mysql('performer')
        for url in urls:
            try:
                print('start--: ',self.x)
                self.x += 1
                query = mysql.query({'url': url})
                if query:
                    print('跳过：', url)
                    continue
                data = self.get_data(url)
                #print('...',data['name'])


                print('插入数据----------')
                mysql.insert(data)
                print('插入完成----------')
            except Exception as e:
                print('-----------',e,url)
                continue

for i in range(41,772):
    print('page--------------: ',i)
    performer = Performer('https://www.javbus.com/actresses/%s' % i)
    performer.main()
