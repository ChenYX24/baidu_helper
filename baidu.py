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
        """
          - 分享
        """
        url = 'https://pan.baidu.com/share/set'

    def folder_add(self, path, folder_name):
        """
        添加文件夹
        """
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

    def file_folder_delete(self, delete_list: list[str]):
        """
        删除文件夹或文件，传入一个list包含每一个要删除的路径
        """
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

    def file_folder_rename(self, paths, new_names):
        """
        重命名
        两个参数对应两个数组，记录路径和新名字
        """
        url = 'https://pan.baidu.com/api/filemanager'
        payload = {
            'async': '2',
            'onnest': 'fail',
            'opera': 'rename',
            'bdstoken': 'c1bf432f74b461320ff1a46c5c0d38a0',
            'clienttype': '0',
            'app_id': '250528',
            'web': '1',
            'dp-logid': '35893700578085580069',
        }
        rename_list = [{"path": path, "newname": newname}
                       for path, newname in zip(paths, new_names)]
        rename_list_json = json.dumps(rename_list)
        form_data = {
            'filelist': rename_list_json,
        }
        response = requests.post(
            url, headers=self.headers, data=form_data, params=payload)
        response_content = json.loads(response.content.decode("utf-8"))
        print(response_content)

    def file_folder_copy(self, copy_list):
        """
        复制
        数据结构为copy_list:[{"path":"","dest":"","newname":""}]
        ondup两个可选参数,newcop,overwrite
        如果newname为空则默认为原本的名字
        """
        url = 'https://pan.baidu.com/api/filemanager'
        payload = {
            'async': '2',
            'onnest': 'fail',
            'opera': 'copy',
            'bdstoken': 'c1bf432f74b461320ff1a46c5c0d38a0',
            'clienttype': '0',
            'app_id': '250528',
            'web': '1',
            'dp-logid': '48507800776512390044',
        }
        for item in copy_list:
            if not item.get('newname'):
                item['newname'] = item['path'].split('/')[-1]
        copy_list_json = json.dumps(copy_list)
        form_data = {
            'filelist': copy_list_json,
        }
        response = requests.post(
            url, headers=self.headers, data=form_data, params=payload)
        response_content = json.loads(response.content.decode("utf-8"))
        print(response_content)

    def file_folder_move(self, move_list):
        """
        移动
        数据结构为move_list:[{"path":"","dest":"","ondup":"overwrite","newname":""}]
        ondup三个可选参数,newcop,overwrite
        如果newname为空则默认为原本的名字
        """
        url = 'https://pan.baidu.com/api/filemanager'
        payload = {
            'async': '2',
            'onnest': 'fail',
            'opera': 'move',
            'bdstoken': 'c1bf432f74b461320ff1a46c5c0d38a0',
            'clienttype': '0',
            'app_id': '250528',
            'web': '1',
            'dp-logid': '48507800776512390044',
        }
        for item in move_list:
            if not item.get('newname'):
                item['newname'] = item['path'].split('/')[-1]
        move_list_json = json.dumps(move_list)
        form_data = {
            'filelist': move_list_json,
        }
        response = requests.post(
            url, headers=self.headers, data=form_data, params=payload)
        response_content = json.loads(response.content.decode("utf-8"))
        print(response_content)

    def floder_push(self):
        """
        上传
        """
        preurl = 'https://pan.baidu.com/api/precreate'
        payload = {
            'bdstoken': 'c1bf432f74b461320ff1a46c5c0d38a0',
            'app_id': '250528',
            'channel': 'chunlei',
            'web': '1',
            'clienttype': '0',
            'dp-logid': '48507800776512390044',
        }
        form_data = {
            'path': '/test/kid1/files/file_content.json',
            'autoinit': '1',
            'target_path': '/test/kid1/',
            'block_list': '["5910a591dd8fc18c32a8f3df4fdc1761"]',
            'local_mtime': '1695178153',
        }
        """
        响应：
        {
    "path": "\/test\/kid1\/files\/file_content.json",
    "uploadid": "N1-MjE4LjE5LjQ2LjIxOToxNjk1MTkxNzQ4OjMyNjAxNzk5OTgwODY4OTQxOA==",
    "return_type": 1,
    "block_list": [
        0
    ],
    "errno": 0,
    "request_id": 326017999808689418
}
        """
        super_url = 'https://xafj-ct10.pcs.baidu.com/rest/2.0/pcs/superfile2'

        super_payload = {
            'method': 'upload',
            'logid': 'MTY5NTE5MTU1MzQ4MTAuMjE2MTU2ODI0MDQ3NTkxNzM=',
            'app_id': '250528',
            'channel': 'chunlei',
            'web': '1',
            'path': '%2Ftest%2Fkid1%2Ffiles%2Ffile_content.json',
            'uploadid': 'N1-MjE4LjE5LjQ2LjIxOToxNjk1MTkxNzQ4OjMyNjAxNzk5OTgwODY4OTQxOA==',
            'clienttype': '0',
            'uploadsign': '0',
            'partseq': '0',
            'dp-logid': '48507800776512390044',
        }
        super_form_data = {
            'file': '',  # 二进制内容
        }
        """
        响应：{md5: "d1c709b3c4e693fef814a08dd123bd9e", partseq: "0", request_id: 6090625627965506000,…}
        md5:"d1c709b3c4e693fef814a08dd123bd9e"
        partseq:"0"
        request_id:6090625627965506000
        uploadid:"N1-MjE4LjE5LjQ2LjIxOToxNjk1MTkxNzQ4OjMyNjAxNzk5OTgwODY4OTQxOA=="
        """
        url = 'https://pan.baidu.com/api/create'

        payload = {
            'isdir': '0',
            'bdstoken': 'c1bf432f74b461320ff1a46c5c0d38a0',
            'app_id': '250528',
            'channel': 'chunlei',
            'web': '1',
            'clienttype': '0',
            'dp-logid': '48507800776512390044',
        }
        form_data = {
            'path': '/test/kid1/files/file_content.json',
            'size': '4901',
            'uploadid': 'N1-MjE4LjE5LjQ2LjIxOToxNjk1MTkxNzQ4OjMyNjAxNzk5OTgwODY4OTQxOA==',
            'target_path': '/test/kid1/',
            'block_list': '["d1c709b3c4e693fef814a08dd123bd9e"]',
            'local_mtime': '1695178153'
        }
        """
        响应：
            {
                "category": 6,
                "ctime": 1695191749,
                "from_type": 1,
                "fs_id": 371055329789533,
                "isdir": 0,
                "md5": "c5c5d6995o6cc45cd000f8f971bf6d62",
                "mtime": 1695191749,
                "path": "\/test\/kid1\/files\/file_content.json",
                "server_filename": "file_content.json",
                "size": 4901,
                "errno": 0,
                "name": "\/test\/kid1\/files\/file_content.json"
            }
        """
        response = requests.post(
            url, headers=self.headers, data=form_data, params=payload)
        response_content = json.loads(response.content.decode("utf-8"))
        print(response_content)


if __name__ == "__main__":
    baidu = BaiDuPan()
    # file_content = baidu.get_file_list(dir='/test')
    # baidu.saveJson('./files/file_content.json', file_content)
    # file_content = baidu.readJson('./files/file_content.json')
    # search = baidu.search_server_filename('child', 1)
    # baidu.saveJson('./files/search.json', search)
    # baidu.folder_add('/test/', 'ttt')
    # baidu.file_folder_delete(
    #     ["/test/child1/kid2/455", "/test/child1/kid2/test3.txt"])
    # baidu.file_folder_rename(['/test/new_name','/test/test2.txt'], ['new_name2','new_name.txt'])
    # baidu.file_folder_copy([{"path":"/test/new_name.txt","dest":"/test/kid2","newname":"new_name3.txt"},{"path":"/test/new_name.txt","dest":"/test/kid2"}])
    # baidu.file_folder_move([{"path":"/test/kid1/new_name.txt","dest":"/test/kid1/child4","newname":"new_name.txt"}])
