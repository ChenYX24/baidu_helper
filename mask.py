import json
from baidu import BaiDuWangPan

baidu = BaiDuWangPan()

"""
给出分享群名，分享文件路径，将对应的文件保存到网盘中指定位置，并生成分享链接(不能得到最终分享链接的情况属于异常情况，应抛出对应的异常信息),所有信息通过json传递
"""


def share_file_to_group(group_name, file_paths):
    try:
        baidu.create_share_link(file_paths, period=7, pwd=True)
        group_list = baidu.get_group_list()
        group_list_data = group_list.get("data").get("records")
        group_id = [item['gid']
                    for item in group_list_data if item['name'] == group_name]
        share_link = baidu.share_to_group(group_id, file_paths)
        saved_file_path = "/files/test/mask1.json"
        if not share_link:
            raise Exception("无法为文件生成分享链接。")
        return json.dumps({
            "group_name": group_name,
            "saved_file_path": saved_file_path,
            "share_link": share_link
        })
    except Exception as e:
        return json.dumps({"error": f"保存文件时出现错误: {str(e)}"})


# result = share_file_to_group("test_group", [438408946807503])


"""
输入文件路径、群、网盘位置
查找群中路径下的文件或文件夹
保存到网盘指定位置
分享链接
"""
def share_lib_file(file_name,group_name,tar_path):
    # tar_path+=f"/{file_name}"
    group_list = baidu.get_group_list()
    group_list_data = group_list.get("data").get("records")
    group_id = [item['gid'] for item in group_list_data if item['name'] == group_name]
    lib_list=baidu.get_file_library_share_list(group_id)
    lib_list_data=lib_list.get("data").get("msg_list")
    from_uk, msg_id, fs_ids = [], [], []
    for item in lib_list_data:
        if item["file_list"][0]['server_filename'] == file_name:
            from_uk.append(item['uk'])
            msg_id.append(item['msg_id'])
            fs_ids.append(item["file_list"][0]["fs_id"])

    transfer_result=baidu.transfer(from_uk[0], msg_id[0], tar_path, json.dumps(fs_ids), group_id[0])
    tar_path_files=baidu.get_file_list(dir_path=f'{tar_path}')
    tar_file_id = [item['fs_id'] for item in tar_path_files if item['server_filename'] == file_name]
    link=baidu.create_share_link(tar_file_id, period=7, pwd=True).get("data")
    return link

result=share_lib_file("10. 外 婆.flac","test_group","/group_test")

print(result)

import requests
# 定义Server酱的SCKEY，替换为你自己的SCKEY
SCKEY = "SCT225727ThAXF8I3WOtfwaGiCn0SR29PN"
# 发送消息到微信
message = f"链接：{result.get('link')}\n密码：{result.get('pwd')}"
send_url = f"https://sc.ftqq.com/{SCKEY}.send?text=新通知&desp={message}"
response = requests.get(send_url)
print("已发送消息到微信")
