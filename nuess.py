import requests
import json
import time

from apscheduler.schedulers.background import BackgroundScheduler, BlockingScheduler
from apscheduler.jobstores.base import JobLookupError

class Nessus:
    def __init__(self, username, password, server_ip='https://localhost:8834'):
        self.username = username
        self.password = password
        self.server_ip = server_ip
        self.token = self.getToken()
        self.headers = {'X-Cookie': 'token={token};'.format(token=self.token),
         'Content-type': 'application/json',
         'Accept': 'text/plain'}

    # 封装post请求
    def post(self, url, data=None, headers=None):
        """
        封装post请求
        :param url: 请求地址
        :param data: 请求数据
        :param headers: 请求头
        :return: 转换后的数据
        """
        print('url:', url)
        print('data:', data)
        resp = requests.post(url, data, headers=headers, verify=False)
        resp.close()
        if resp.status_code == 200:
            result = json.loads(resp.text)
            print(result)
            return result
        print(resp, resp.text)

    # 封装get请求
    def get(self, url, data=None, headers=None):
        """
        封装get请求
        :param url: 请求地址
        :param data: 请求数据
        :param headers: 请求头
        :return: 转换后的数据
        """
        print('url:', url)
        print('data:', data)
        resp = requests.get(url, data, headers=headers, verify=False)
        resp.close()
        if resp.status_code == 200:
            result = json.loads(resp.text)
            print(result)
            return result

    # 获取模板ID
    def getTemplateUuid(self, name='advanced'):
        """
        根据模板名称，从所有模板中，获取模板ID
        :param name: str 模板名称
        :return: int 模板ID
        """
        url = self.server_ip + '/editor/scan/templates'
        result = self.get(url, headers=self.headers)
        if result:
            templates = result.get('templates')
            for template in templates:
                if template['name'] == name:
                    return template['uuid']

    # 创建扫描任务
    def createScan(self, template_uuid, name, text_targets):
        """
        创建扫描任务
        :param template_uuid: str 模板UUID
        :param name: str 任务名称
        :param text_targets: list IP列表
        :return:  当前任务对象
        """
        url = self.server_ip + '/scans'
        data = {
            'uuid': template_uuid,
            'settings': {
                'name': name,
                'enabled': True,
                'text_targets': text_targets
            },
        }
        result = self.post(url, data, headers=self.headers)

    # 获取token
    def getToken(self):
        """
        连接获取token
        :return:  str token值
        """
        data = {
            'username': self.username,
            'password': self.password
        }
        url = self.server_ip + '/session'
        result = self.post(url, data)
        if result:
            return result.get('token')

    # 获取扫描任务列表
    def getScanList(self):
        """
        获取扫描任务列表
        :return: list 当前任务列表
        """
        url = self.server_ip + '/scans'
        result = self.get(url, headers=self.headers)
        #resp = requests.post(url)
        return result

    # 获取扫描任务ID
    def getScanId(self, scan_name):
        """
        根据扫描任务名称，获取扫描任务ID
        :param scan_name: str 任务名称
        :return: int 扫描任务ID
        """
        scan_list = self.getScanList().get('scans')
        if not scan_list:
            return
        for scan in scan_list:
            if scan['name'] == scan_name:
                return scan['id']

    # 根据scanId发起任务
    def scanLuanch(self, scan_id, ip_list):
        """
        开启扫描任务
        :param scan_id: int 扫描任务ID
        :param ip_list: list 扫描IP列表
        :return: str 扫描uuid
        """
        url = self.server_ip + '/scans/' + str(scan_id) + '/launch'
        data = {
            'alt_targets': ip_list
        }
        result = self.post(url, data, self.headers)
        if result:
            scan_uuid = result.get('scan_uuid')
            return scan_uuid

    # 动态监听任务
    def listenScan(self, scan_id):
        """
        监听扫描任务是否执行完成
        :param scan_id: int 扫描任务ID
        :return: boolean  true为扫描完成，否则扫描出错
        """
        url = self.server_ip + '/scans/' + str(scan_id)
        while True:
            result = self.get(url, headers=self.headers)
            if result:
                status = result.get('info',{}).get('status')
                if status == 'running':
                    pass
                elif status == 'completed':
                    return True
                else:
                    break
            time.sleep(30)

    # 获取下载参数
    def getExport(self, scan_id):
        """
        请求export接口，获取当前任务下载报告的参数
        :param scan_id: int 扫描任务ID
        :return: dict {'file': ...}
        """
        url = self.server_ip + '/scans/' + str(scan_id) + '/export'
        data = {
            'format': 'pdf',
            'chapters': 'vuln_hosts_summary'
        }
        result = self.post(url, data=json.dumps(data), headers=self.headers)
        return result

    # 获取生成报告状态
    def getStatus(self, scan_id, file_id):
        """
        监听生成报告的状态，判断是否生成完成
        :param scan_id: int 扫描任务ID
        :param file_id: int 文件ID
        :return: boolean
        """
        url = self.server_ip + '/scans/' + str(scan_id) + '/export/' + str(file_id) + '/status'
        while True:
            result = self.get(url, headers=self.headers)
            if result:
                status = result.get('status')
                if status == 'loading':
                    time.sleep(30)
                else:
                    return True
            else:
                return False

    # 下载报告
    def download(self, scan_id, file_id):
        """
        下载生成的报告
        :param scan_id: int 任务ID
        :param file_id: int 文件ID
        :return: None
        """
        url = self.server_ip + '/scans/' + str(scan_id) + '/export/' + str(file_id) + '/download'
        resp = requests.get(url, headers=self.headers, verify=False)
        filename = 'nessus_%s_%s.pdf' % (scan_id, file_id)
        #print(resp.text)
        with open(filename, 'wb') as f:
            f.write(resp.content)

    # 一键执行
    def main(self, scan_name):
        # 获取扫描ID
        scan_id = self.getScanId(scan_name)

        # 执行
        self.scanLuanch(scan_id, None)

        # 监听执行状态
        if not self.listenScan(scan_id):
            print('监听执行出错')
            return 

        # 获取文件ID
        file_id = self.getExport(scan_id)['file']
        if not self.getStatus(scan_id, file_id):
            print('生成报告出错')
            return 

        # 下载附件
        self.download(scan_id, file_id)

def main():
    print('start...')
    ness = Nessus('xiaoxin', 'xiaoxin901008')
    ness.main('test')

aps = BlockingScheduler()
aps.add_job(func=main, trigger='interval', minutes=1, id='test')
aps.start()
#aps.add_job(main, 'cron', day='*', hour='01', minute='01', second='01', id='test')



