# coding="utf-8"

import requests
import re
import json
import time
import random
import os


'''
'''


class BaiDuPan(object):
    def __init__(self):
        self.retry_limit = 3
        self.headers = {
            'Host': 'pan.baidu.com',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.120 Safari/537.36',
        }
        self.headers['Cookie'] = 'BIDUPSID=69E28713CEF4C74FC5B9B97E2E3E9651; PSTM=1686308325; BAIDUID=69E28713CEF4C74FFE683719516B4A50:FG=1; ZFY=Te0ugrPfZ:BGiG:BnHsCyv:AOr9ZvJr:AMJ1nNzVn:B4cqao:C; BAIDUID_BFESS=69E28713CEF4C74FFE683719516B4A50:FG=1; csrfToken=Oac_XEt_vHPJKHRSXPd5MxkA; newlogin=1; BDUSS=WlOUG1FNjlmTnU4bndoaXAza0RkanVMSEJIZGV1aFlJZmVPdE9EZ2lWcDcyVEJsSVFBQUFBJCQAAAAAAAAAAAEAAAAqoj5iw87Q0div0MTp5AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAHtMCWV7TAllZ; BDUSS_BFESS=WlOUG1FNjlmTnU4bndoaXAza0RkanVMSEJIZGV1aFlJZmVPdE9EZ2lWcDcyVEJsSVFBQUFBJCQAAAAAAAAAAAEAAAAqoj5iw87Q0div0MTp5AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAHtMCWV7TAllZ; STOKEN=e2cf9f58dd40c71548dd5b7b83a63bdf8ef9f41d2c34dde2bb030bed97a03284; PANPSC=3354585111300780618%3ACU2JWesajwDE3oP99pMv7xGy4OU887ORVNbGxeMGSdR7gvgDy7JBfVZyeLTzW4IXgEmtLzrwSnIr2wqYbSNJzI7%2BuszIM%2FQF111fkOADSnwuRevHA8Yw6ivUNQZ%2Bmpo%2BKs%2BlyV4xxrIh7IX89yGaj01oE1oKWHdrHwnsXTVs8ITR4SeWmT6baF9K9yVk1uvA4i2i1JdCg%2BQoj3hBKvZymPgT7Eg6UyTb; ndut_fmt=B32D7F2CE763FA47159144F3DB233EB6BF63ECE3B8C33BF2BFF06C1A118AEC57; ab_sr=1.0.1_NzdlMjgxMTU2ZGQ0ZWE3ZmRlZDAyYTcyYWQ4NGYzM2VmOWZkMDY4NThmNDc0ZjgxZjkxYjFlZGUyZWI4MjY5MWFkZDMxZWI4ZjAxNmI0YjAwNTgyOGI0MzMwZTE3MjFiMjExMTY5NzU3MzhlMjA3ZWUyMjczNjc2YWNhZTgwYTUxNTkzNTlmZmI2ODg3Yzk3Yjc0MjYwNjJiNGJmZDNlMGY5ZjYwNjUyNGRhODZhOWRkYzU5ZDIyYTRlMDMwNDg4'

    @staticmethod
    def saveJson(title, data):  # 将数据保存为json文件
        if not os.path.exists(title):
          # 路径不存在则先创一个
            os.makedirs(os.path.dirname(title), exist_ok=True)
            with open(title, 'w') as f:
                f.write('')
        with open(title, 'w') as f:
            f.write(json.dumps(data, indent=4))

    @staticmethod
    def readJson(title):
        """
        读文件
        """
        if not os.path.exists(title):
            return ""
        with open(title, 'r') as f:
            return json.loads(f.read())

    def get_file_list(self, dir='/', retry=0):
        # 加载之前保存的进度
        progress = self.readJson('./files/progress.json')
        if progress is not None and dir in progress:
            # 如果已经遍历过该目录，直接从进度中获取列表
            file_list = progress[dir]
        else:
            print(f'遍历路径 {dir}中...')
            url = 'https://pan.baidu.com/api/list'
            # 载荷数据
            payload = {
                'clienttype': '0',
                'app_id': '250528',
                'web': '1',
                'dp-logid': '91380000697342040025',
                'order': 'time',
                'desc': '1',
                'dir': f'{dir}',
                'num': '100',
                'page': '1'
            }
            # 发送POST请求
            response = requests.post(url, data=payload, headers=self.headers)
            # 检查响应状态码
            if response.status_code == 200:
                # 处理响应数据
                file_content = response.content.decode("utf-8")
                file_content = json.loads(file_content)["list"]
                return file_content
            else:
                print(f"请求失败，状态码: {response.status_code}")

    def search_server_filename(self, keyword, recursion=1):
        url = 'https://pan.baidu.com/api/search'
        # 载荷数据
        params = {
            'clienttype': '0',
            'app_id': '250528',
            'web': '1',
            'dp-logid': '23758300368469790051',
            'order': 'time',
            'desc': '1',
            'num': '100',
            'page': '1',
            'recursion': f'{recursion}',  # 递归子目录数
            'key': f'{keyword}'      # 查找内容
        }

        # get
        response = requests.get(url, params=params, headers=self.headers)
        search_content = json.loads(response.content.decode("utf-8"))
        return search_content

    def file_folder_share():
        """文件夹
          - 分享
          - 删除
          - 重命名
          - 复制
          - 移动
          - 新建
          - 上传
        """

    def file_folder_add(self, path, folder_name):
        url = 'https://pan.baidu.com/api/create'
        payload = {
            'a': 'commit',
            'bdstoken': 'c1bf432f74b461320ff1a46c5c0d38a0',
            'clienttype': '0',
            'app_id': '250528',
            'web': '1',
            'dp-logid': '12808300274012460052',
        }
        form_data = {
            'path': f'{path}{folder_name}',
            'isdir': '1',
            'block_list': '[]',
        }
        response = requests.post(
            url, headers=self.headers, data=form_data, params=payload)
        response_content = json.loads(response.content.decode("utf-8"))
        print(response_content)

    def file_folder_delete(self, delete_list):
        url = 'https://pan.baidu.com/api/filemanager'
        payload = {
            'async': '2',
            'onnest': 'fail',
            'opera': 'delete',
            'bdstoken': 'c1bf432f74b461320ff1a46c5c0d38a0',
            'newVerify': '1',
            'clienttype': '0',
            'app_id': '250528',
            'web': '1',
            'dp-logid': '78491000811514990047',
        }
        delete_list_json = json.dumps(delete_list)
        form_data = {
            'filelist': delete_list_json,
        }
        response = requests.post(
            url, headers=self.headers, data=form_data, params=payload)
        response_content = json.loads(response.content.decode("utf-8"))
        print(response_content)

    def file_delete():
        """文件操作
        - 分享
        - 删除
        - 重命名
        - 复制
        - 移动
        - 上传
        """


if __name__ == "__main__":
    baidu = BaiDuPan()
    # file_content = baidu.get_file_list(dir='/test')
    # baidu.saveJson('./files/file_content.json', file_content)
    # file_content = baidu.readJson('./files/file_content.json')
    # search = baidu.search_server_filename('child', 1)
    # baidu.saveJson('./files/search.json', search)
    baidu.file_folder_add('/test/', 'ttt')
    baidu.file_folder_delete(
        ["/test/child1/kid2/455", "/test/child1/kid2/test3.txt"])
