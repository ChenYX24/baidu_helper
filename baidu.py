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
        self.headers['Cookie'] = 'BIDUPSID=1B00E53394E38DC5DF5A8A0C8AA12000; PSTM=1632669581; __yjs_duid=1_adc2e0996e2a2d5580f2714e4f7f1e501632669593304; BDUSS=mlRWUg0c3hJLU9ETzJybmhWaEw2b0RjMkVnM1BrZEZadTZLSXFwRTFiRW00OEpoRVFBQUFBJCQAAAAAAAAAAAEAAAAqoj5iw87Q0div0MTp5AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAACZWm2EmVpthQ; PANWEB=1; Hm_lvt_fa0277816200010a74ab7d2895df481b=1672578884; BDUSS_BFESS=mlRWUg0c3hJLU9ETzJybmhWaEw2b0RjMkVnM1BrZEZadTZLSXFwRTFiRW00OEpoRVFBQUFBJCQAAAAAAAAAAAEAAAAqoj5iw87Q0div0MTp5AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAACZWm2EmVpthQ; BAIDUID=733F6987812207206DB80042F6ED71D6:FG=1; H_WISE_SIDS=219946_114550_219564_216842_213357_214800_219943_213039_230178_204919_110085_236312_243706_243881_244726_245412_247146_250304_250890_249892_240590_254734_233835_253426_250887_255938_255979_107314_256083_253993_256121_256257_255661_255476_256500_254831_256739_251973_256589_257079_254075_257291_257284_254317_251058_257406_254299_255324_257542_257659_257745_257786_257938_257167_257903_258073_257823_257586_257401_255231_253900_258192_258248_257996_258525_258374_258369_258395_258641_258724_258728_258921_258938_257302_258982_258958_258698_230288_259049_259067_257576_259190_259193_256223_259405_259391_259430_211987_259568_259606_259626_256999_259558_259644_259648_251785_258773_234296_234207_259909_259888_259643_255909_8000088_8000102_8000120_8000135_8000149_8000166_8000175_8000178_8000188; H_WISE_SIDS_BFESS=219946_114550_219564_216842_213357_214800_219943_213039_230178_204919_110085_236312_243706_243881_244726_245412_247146_250304_250890_249892_240590_254734_233835_253426_250887_255938_255979_107314_256083_253993_256121_256257_255661_255476_256500_254831_256739_251973_256589_257079_254075_257291_257284_254317_251058_257406_254299_255324_257542_257659_257745_257786_257938_257167_257903_258073_257823_257586_257401_255231_253900_258192_258248_257996_258525_258374_258369_258395_258641_258724_258728_258921_258938_257302_258982_258958_258698_230288_259049_259067_257576_259190_259193_256223_259405_259391_259430_211987_259568_259606_259626_256999_259558_259644_259648_251785_258773_234296_234207_259909_259888_259643_255909_8000088_8000102_8000120_8000135_8000149_8000166_8000175_8000178_8000188; BDORZ=B490B5EBF6F3CD402E515D22BCDA1598; STOKEN=36c9178c694f4fc54aaed938525c5ebbfce3c03ce387eeb35425f28848a9f7d1; newlogin=1; Hm_lvt_7a3960b6f067eb0085b7f96ff5e660b0=1694927867; BDCLND=mB8yf%2BHwkT%2B9idq1LkrO%2FL%2B%2BZ%2FU9Kmn%2BapStpOCvSaM%3D; H_PS_PSSID=39311_39368_39353_39348_39407_39097_39411_39439_39345_39358_39307_39233_26350_39428; BAIDUID_BFESS=733F6987812207206DB80042F6ED71D6:FG=1; BA_HECTOR=aka4252ha02k8k0g81000k011igr7bt1o; ZFY=KlpL72Vxx5RSqpteBx:AWOEYyrC0r9NaXIamOqWZ5Ufo:C; BCLID=7283200180341604545; BCLID_BFESS=7283200180341604545; BDSFRCVID=_DkOJexroG0Jp3jqBOsK26-xHyNbUdrTDYrEjGc3VtzSGYLVFsQ6EG0Pts1-dEub6j30ogKK5mOTH6KF_2uxOjjg8UtVJeC6EG0Ptf8g0M5; BDSFRCVID_BFESS=_DkOJexroG0Jp3jqBOsK26-xHyNbUdrTDYrEjGc3VtzSGYLVFsQ6EG0Pts1-dEub6j30ogKK5mOTH6KF_2uxOjjg8UtVJeC6EG0Ptf8g0M5; H_BDCLCKID_SF=tbC8VCDKJKD3H48k-4QEbbQH-UnLqMCfW2OZ04n-ah02O4tRMRQIXntIDGDLhUv8BDrP0Pom3UTKsq76Wh35K5tTQP6rLf5eLRc4KKJxbP8aKJbH5tK-M6JQhUJiB5QLBan7_qvIXKohJh7FM4tW3J0ZyxomtfQxtNRJ0DnjtpChbC8lejuaj6bLeU5eetjK2CntsJOOaCvshpTOy4oWK441D-6jJ-TD0eOeBI_KH4n1JqrP3tOK3M04K4o9-hvT-54e2p3FBUQPqUDCQft20b0yDecb0RQaJDLeon7jWhkhDq72y5jvQlRX5q79atTMfNTJ-qcH0KQpsIJM5-DWbT8IjHCeJ6F8tRFfoCvMKRu_HRjYbb__-P4DennRaMRZ56bHWh0MWtt5j4jtXnbvD65D2-78WtjP5TrnKUT-3RcnHIOK5b66QpFT34jeQ6543bRTLP8hHRbpfJ_CM6-2hP-UyNoLWh37Je3lMKoaMp78jR093JO4y4Ldj4oxJpOJ5JbMopCafJOKHICmDjDWDUK; H_BDCLCKID_SF_BFESS=tbC8VCDKJKD3H48k-4QEbbQH-UnLqMCfW2OZ04n-ah02O4tRMRQIXntIDGDLhUv8BDrP0Pom3UTKsq76Wh35K5tTQP6rLf5eLRc4KKJxbP8aKJbH5tK-M6JQhUJiB5QLBan7_qvIXKohJh7FM4tW3J0ZyxomtfQxtNRJ0DnjtpChbC8lejuaj6bLeU5eetjK2CntsJOOaCvshpTOy4oWK441D-6jJ-TD0eOeBI_KH4n1JqrP3tOK3M04K4o9-hvT-54e2p3FBUQPqUDCQft20b0yDecb0RQaJDLeon7jWhkhDq72y5jvQlRX5q79atTMfNTJ-qcH0KQpsIJM5-DWbT8IjHCeJ6F8tRFfoCvMKRu_HRjYbb__-P4DennRaMRZ56bHWh0MWtt5j4jtXnbvD65D2-78WtjP5TrnKUT-3RcnHIOK5b66QpFT34jeQ6543bRTLP8hHRbpfJ_CM6-2hP-UyNoLWh37Je3lMKoaMp78jR093JO4y4Ldj4oxJpOJ5JbMopCafJOKHICmDjDWDUK; csrfToken=hs-CO2JWNcWKkMweFp9ruwBn; PANPSC=16162519696563325585%3ACU2JWesajwDE3oP99pMv7xGy4OU887ORVNbGxeMGSdR7gvgDy7JBfVZyeLTzW4IXgEmtLzrwSnIr2wqYbSNJzI7%2BuszIM%2FQF9jqImtiV9t4uRevHA8Yw6ivUNQZ%2Bmpo%2BKs%2BlyV4xxrIh7IX89yGaj01oE1oKWHdrHwnsXTVs8ITR4SeWmT6baF9K9yVk1uvA4i2i1JdCg%2BQoj3hBKvZymPgT7Eg6UyTb; ndut_fmt=360D694FAB922F36F0BC73F53860958E32592717115867F2511DD3566349DFF8; ab_sr=1.0.1_ZjBhNDM4N2JkZjY0ZDlhZGRhNjE5YTg4YWU0ZDExZGU5MmY2ZmRmMjE5NDk2ZmNlMzYxMzNlYWUwMGY4MTAxYzZiM2UyN2JkNzQ4NzFlNzFiNGE0M2I4N2RiNTIyYmU1NWYyN2RiYjU3NDA1Yzk5ZTc0N2EyZDVkMzUwMTk5MDMwYmM4MjAyODhkYzdiNWRiZWU1NWY4MjA3MGU0MWMyZGY3MTcxNjI2OGFjZDlhZGYwOGM5MTRlMDJmZWVmZmI4'

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

    def folder_add(self, path, folder_name):
        """
        添加文件夹
        """
        url = 'https://pan.baidu.com/api/create'
        payload = {
            'a': 'commit',
            'bdstoken': '8a902ff8d133bc0b26e061b565dffe53',
            'clienttype': '0',
            'app_id': '250528',
            'web': '1',
            'dp-logid': '43865200699754060045',
        }
        form_data = {
            'path': f'{path}{folder_name}',
            'isdir': '1',
            'block_list': '[]',
        }
        response = requests.post(
            url, headers=self.headers, data=form_data, params=payload)
        response_content = json.loads(response.content.decode("utf-8"))
        return response_content

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
        return response_content

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
        return response_content

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
        return response_content

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
        return response_content

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
        response = requests.post(
            url, headers=self.headers, params=params, data=data)
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
        response = requests.post(
            url, headers=self.headers, params=params, data=data)
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
    # r = baidu.get_friend_list()
    # print(r)

    # 分享给群组
    # r = baidu.share_to_group(["1048666503551696519"], [190704352051208])
    # print(r)

    # 发消息给群组
    # r = baidu.send_msg_to_group(["1048666503551696519"], "测试")
    # print(r)
