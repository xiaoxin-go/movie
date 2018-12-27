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
        url = self.server_ip + '/editor/scan/templates'
        result = self.get(url, headers=self.headers)
        if result:
            templates = result.get('templates')
            for template in templates:
                if template['name'] == name:
                    return template['uuid']

    # 创建扫描任务
    def createScan(self, template_uuid, name, text_targets):
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
        url = self.server_ip + '/scans'
        result = self.get(url, headers=self.headers)
        #resp = requests.post(url)
        return result

    # 获取扫描任务ID
    def getScanId(self, scan_name):
        scan_list = self.getScanList().get('scans')
        if not scan_list:
            return
        for scan in scan_list:
            if scan['name'] == scan_name:
                return scan['id']

    # 根据scanId发起任务
    def scanLuanch(self, scan_id, ip_list):
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
        url = self.server_ip + '/scans/' + str(scan_id) + '/export'
        data = {
            'format': 'pdf',
            'chapters': 'vuln_hosts_summary'
        }
        result = self.post(url, data=json.dumps(data), headers=self.headers)
        return result

    # 获取生成报告状态
    def getStatus(self, scan_id, file_id):
        url = self.server_ip + '/scans/' + str(scan_id) + '/export/' + str(file_id) + '/status'
        result = self.get(url, headers=self.headers)
        if result:
            return result.get('status')

    # 下载报告
    def download(self, scan_id, file_id):
        url = self.server_ip + '/scans/' + str(scan_id) + '/export/' + str(file_id) + '/download'
        resp = requests.get(url, headers=self.headers, verify=False)
        filename = 'nessus_%s_%s.pdf' % (scan_id, file_id)
        print(resp.text)
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
            print('监听请求错误')

        # 获取文件ID
        file_id = self.getExport(scan_id)['file']
        while self.getStatus(scan_id, file_id) == 'loading':
            time.sleep(10)

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



