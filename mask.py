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


result = share_file_to_group("test_group", [438408946807503])
