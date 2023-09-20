from baidu import BaiDuPan

baidu = BaiDuPan()

def test_create_share_link():
    # 创建分享链接
    r = baidu.create_share_link([690714735880835])
    assert(r['errno'] == 0)