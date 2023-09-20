# coding="utf-8"
import string

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
        self.headers['Cookie'] = 'PANWEB=1; BIDUPSID=569C78CFDF8EDB06B5E81247D1B4D1E4; BAIDUID=9B587808DF1127A51C8E42336B18EC09:FG=1; PSTM=1682797646; BDUSS=3RXNWJ3RVFMbm0zVnk2OH43Rm1EV1RITDBReERjUFk3b1BxN1QzVk9GaDVNcUJrRVFBQUFBJCQAAAAAAAAAAAEAAAChnI3OV0NDWVpYWQAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAHmleGR5pXhkR; BDUSS_BFESS=3RXNWJ3RVFMbm0zVnk2OH43Rm1EV1RITDBReERjUFk3b1BxN1QzVk9GaDVNcUJrRVFBQUFBJCQAAAAAAAAAAAEAAAChnI3OV0NDWVpYWQAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAHmleGR5pXhkR; Hm_lvt_7a3960b6f067eb0085b7f96ff5e660b0=1689001027; STOKEN=76dca0c6950b2721c2b3968a150bdac0628d40c59cab9b57793eb9cf33154508; newlogin=1; BDCLND=sGwjLewAXYpZltYfX2rAtxVDjlxWAY2U5HBm%2FctcjcQ%3D; BAIDUID_BFESS=9B587808DF1127A51C8E42336B18EC09:FG=1; BDRCVFR[TCFer5TLIzY]=mk3SLVN4HKm; BA_HECTOR=85808gah8g212k010h81010c1igjcgl1p; ZFY=WkFG8KgRo4:BDXp5tefZD3SA2lJrVe:A7hUYR:AHZlokoI:C; delPer=0; PSINO=7; H_PS_PSSID=; BDORZ=FFFB88E999055A3F8A630C64834BD6D0; BCLID=7882234929788843196; BCLID_BFESS=7882234929788843196; BDSFRCVID=eA_OJexroG0Jp3jqWExZMBPfq9NbUdrTDYrEjGc3VtzSGYLVFsQ6EG0Pts1-dEub6j30ogKK3gOTH4DF_2uxOjjg8UtVJeC6EG0Ptf8g0M5; BDSFRCVID_BFESS=eA_OJexroG0Jp3jqWExZMBPfq9NbUdrTDYrEjGc3VtzSGYLVFsQ6EG0Pts1-dEub6j30ogKK3gOTH4DF_2uxOjjg8UtVJeC6EG0Ptf8g0M5; H_BDCLCKID_SF=tbC8VCDKJKD3H48k-4QEbbQH-UnLqboxLgOZ04n-ah02O4tRMRQRQJv-Xt5TKJ_8BDrP0Pom3UTKsq76Wh35K5tTQP6rLf5eLRc4KKJxbP8aKJbH5tK-M6JQhUJiB5JMBan7_pbIXKohJh7FM4tW3J0ZyxomtfQxtNRJ0DnjtpChbC8lejuaj6bLeU5eetjK2CntsJOOaCvnHj6Oy4oWK441D-6jJ-TDQ2TOLh6PLnQabqrP3tOK3M04K4o9-hvT-54e2p3FBUQPqUDCQft20b0yDecb0RQaJDLeon7jWhk5ep72y5OUQlRX5q79atTMfNTJ-qcH0KQpsIJM5-DWbT8IjHCeJ6F8tRFfoCvMKRu_HRjYbb__-P4DeUoCyMRZ56bHWh0MWtt5j4j5QJ7AXfDrblL8WtjP5TrnKUT-3RcnHIOK5b66QpFT34jeQ6543bRTLP8hHRbpfJ_CM6-2hP-UyNbMWh37JgnlMKoaMp78jR093JO4y4Ldj4oxJpOJ5JbMopCafJOKHICCe58W3e; H_BDCLCKID_SF_BFESS=tbC8VCDKJKD3H48k-4QEbbQH-UnLqboxLgOZ04n-ah02O4tRMRQRQJv-Xt5TKJ_8BDrP0Pom3UTKsq76Wh35K5tTQP6rLf5eLRc4KKJxbP8aKJbH5tK-M6JQhUJiB5JMBan7_pbIXKohJh7FM4tW3J0ZyxomtfQxtNRJ0DnjtpChbC8lejuaj6bLeU5eetjK2CntsJOOaCvnHj6Oy4oWK441D-6jJ-TDQ2TOLh6PLnQabqrP3tOK3M04K4o9-hvT-54e2p3FBUQPqUDCQft20b0yDecb0RQaJDLeon7jWhk5ep72y5OUQlRX5q79atTMfNTJ-qcH0KQpsIJM5-DWbT8IjHCeJ6F8tRFfoCvMKRu_HRjYbb__-P4DeUoCyMRZ56bHWh0MWtt5j4j5QJ7AXfDrblL8WtjP5TrnKUT-3RcnHIOK5b66QpFT34jeQ6543bRTLP8hHRbpfJ_CM6-2hP-UyNbMWh37JgnlMKoaMp78jR093JO4y4Ldj4oxJpOJ5JbMopCafJOKHICCe58W3e; csrfToken=thgW-VWTdJ-r43ac1Qrds1Cv; ndut_fmt=5AEC70BE75BDF0A6914D2B021B150C1906EE5B47A5F78CE0996E6D4E298E4005; ab_sr=1.0.1_ZmM4MDNlNWJlZWMxN2JlYWIxNzQ2NGQzMjgxZjIwZTc4MTA0OTQwMjM4NTNlZWZkZjYxNGM1ZDRiMjExMWNjYzAzYzNkNGZkYTAwOGViYzYyZmVmZTZhNjVlNDhmNTZiZjdmODdiYzZmNWNlNDJlYzYyYTA1MDlhMzkzY2VmY2QyZGVkYTk5NGIyNWJlYTY3NTUwYzU5YTdhNjE1ZGJhNjUwNjdlNmFiYmQwZmU5N2NhNzUyZWQzMTkyMjBjYjgy; BDRCVFR[A7hGrXFW48R]=K7PavkeTFPTUAN8ULuEQhPEUi4WU6; PANPSC=8094379039185159467%3A1hnZu9bM3mwLsjdBXCoJYFcS2d9ns3O5g0mIZdLHpdQGbqupDlB1gj8zEKyc7S8aV7l9pmSq0a3iLaLUl0KD5De4ZdaW7CoOlL98c8Ccr9ch6uZoP3DwQ9YfJggg9xZJTIlFK73X2ycdYSVq47DcpxufsfK5CTEPuA2SiUJ1YXJZKxE7zkGtkN7ltA6NmG2y'

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

    @staticmethod
    def randomStr(length):
        random_string = ''
        chars = string.ascii_letters + string.digits
        for i in range(length):
            random_string += random.choice(chars)
        return random_string

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

    def file_folder_share(self):
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

    """
    period 有效期 0-永久有效 1-一天 7-七天 30-三十天
    pwd 是否设置提取码
    """
    def create_share_link(self, fid_list, period=7, pwd=True):
        url = 'https://pan.baidu.com/share/set'
        params = {
            'channel': 'chunlei',
            'bdstoken': '7ddec910b0beba5b3380362518c759bd',
            'clienttyoe': 0,
            'app_id': 250528,
            'web': 1,
            'dp-logid': '48041200215572110069'
        }
        if (pwd):
            pwd = self.randomStr(4)

        data = {
            'schannel': 4,
            'channel_list': '[]',
            'period': period,
            'pwd': pwd,
            'fid_list': str(fid_list),
        }
        response = requests.post(url, headers=self.headers, params=params, data=data)
        json_data = response.json()
        if json_data['errno'] == 0:
            return {'errno': 0, 'err_msg': '创建分享链接成功！', 'data': {'link': json_data['link'], 'pwd': pwd}}
        else:
            return {'errno': 1, 'err_msg': '创建分享链接失败！', 'data': json_data}

    def share_to_friend(self, receiver, fs_ids, receiver_name):
        return self.send(send_type=3, receiver=receiver, msg_type=2, msg="", fs_ids=fs_ids, receiver_name=receiver_name)

    def send_msg_to_friend(self, receiver, msg, receiver_name):
        return self.send(send_type=3, receiver=receiver, msg_type=1, msg=msg, fs_ids=[], receiver_name=receiver_name)

    def share_to_group(self, receiver, fs_ids):
        return self.send(send_type=4, receiver=receiver, msg_type=2, msg="", fs_ids=fs_ids)

    def send_msg_to_group(self, receiver, msg):
        return self.send(send_type=4, receiver=receiver, msg_type=1, msg=msg, fs_ids=[])

    def send(self, send_type, receiver, msg_type, msg, fs_ids, receiver_name=""):
        url = 'https://pan.baidu.com/imbox/msg/send'
        params = {
            'clienttype': '0',
            'app_id': '250528',
            'web': '1',
            'dp-logid': '48041200215572110132'
        }
        _data = {
            "send_type": send_type,
            "receiver": receiver,
            "msg_type": msg_type,
            "msg": msg,
            "fs_ids": fs_ids
        }
        if send_type == 3:
            _data["receiver_name"] = receiver_name

        data = {
            'data': json.dumps(_data)
        }
        print(data)
        response = requests.post(url, headers=self.headers, params=params, data=data)
        json_data = response.json()
        if json_data['errno'] == 0:
            return {'errno': 0, 'err_msg': '分享成功', 'data': {}}
        else:
            return {'errno': 1, 'err_msg': '分享失败', 'data': json_data}

    def get_group_list(self):
        url = "https://pan.baidu.com/mbox/group/list"
        params = {
            'clienttype': '0',
            'app_id': '250528',
            'web': '1',
            'dp-logid': '48041200215572110132',
            'start': 0,
            'limit': 20,
            'type': 0
        }
        response = requests.get(url, headers=self.headers, params=params)
        json_data = response.json()
        if json_data['errno'] == 0:
            return {'errno': 0, 'err_msg': '获取成功', 'data': json_data}
        else:
            return {'errno': 1, 'err_msg': '获取失败', 'data': json_data}

    def get_friend_list(self):
        url = "https://pan.baidu.com/mbox/relation/getfollowlist"
        params = {
            'clienttype': '0',
            'app_id': '250528',
            'web': '1',
            'dp-logid': '48041200215572110132',
            'start': 0,
            'limit': 20
        }
        response = requests.get(url, headers=self.headers, params=params)
        json_data = response.json()
        if json_data['errno'] == 0:
            return {'errno': 0, 'err_msg': '获取成功', 'data': json_data}
        else:
            return {'errno': 1, 'err_msg': '获取失败', 'data': json_data}


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

    # 创建分享链接
    # r = baidu.create_share_link([690714735880835])
    # print(r)

    # 分享给好友
    # r = baidu.share_to_friend(["914179002"], [190704352051208], ["fg**vc"])
    # print(r)

    # 发消息给好友
    # r = baidu.send_msg_to_friend(["914179002"], "测试", ["fg**vc"])
    # print(r)

    # 获取群组列表
    # r = baidu.get_group_list()
    # print(r)

    # 获取好友列表
    r = baidu.get_friend_list()
    print(r)

    # 分享给群组
    # r = baidu.share_to_group(["1048666503551696519"], [190704352051208])
    # print(r)

    # 发消息给群组
    # r = baidu.send_msg_to_group(["1048666503551696519"], "测试")
    # print(r)
