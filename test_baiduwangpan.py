from baidu import BaiDuPan

baidu = BaiDuPan()


def test_create_share_link():
    # 创建分享链接
    r = baidu.create_share_link([690714735880835])
    assert (r['errno'] == 0)


def test_get_file_list():
    # 获取文件列表
    r = baidu.get_file_list(dir='/test')
    assert isinstance(r, list)


def test_search_server_filename():
    r = baidu.search_server_filename('kid1', 1)
    assert (r['errno'] == 0)
    assert (len(r['list']) != 0)


def test_folder_add():
    path = '/test/'
    folder_name = 'hhh'
    file_list1 = baidu.get_file_list(dir=path)
    r = baidu.folder_add(path=path, folder_name=folder_name)
    assert (r['errno'] == 0)
    file_list2 = baidu.get_file_list(dir=path)
    assert (file_list1 != file_list2)
    new_element = None
    for item in file_list2:
        if item not in file_list1:
            new_element = item
            break
    assert new_element["server_filename"] == folder_name


def test_file_folder_delete1():
    path = '/test/'
    file_list1 = baidu.get_file_list(dir=path)
    test_list = ["/test/hhh", "/test/new_name.txt"]
    r = baidu.file_folder_delete(test_list)
    assert (r['errno'] == 0)
    file_list2 = baidu.get_file_list(dir=path)
    assert (file_list1 != file_list2)
    new_elements = []
    for item in file_list2:
        if item not in file_list1:
            new_elements.append(item)
            break
    for element in new_elements:
        assert (element in test_list)


def test_file_folder_rename():
    path = '/test/'
    file_list1 = baidu.get_file_list(dir=path)
    r = baidu.file_folder_rename(
        ['/test/new_name2', '/test/new_name.txt'], ['new_name', 'name.txt'])
    assert (r['errno'] == 0)
    file_list2 = baidu.get_file_list(dir=path)
    assert (file_list1 != file_list2)


def test_file_folder_copy():
    path = '/test/kid2/'
    file_list1 = baidu.get_file_list(dir=path)
    copy_list = [
        {"path": "/test/new_name.txt", "dest": "/test/kid2",
            "newname": "new_name3.txt"},
        {"path": "/test/new_name.txt", "dest": "/test/kid2"}
    ]
    r = baidu.file_folder_copy(copy_list)
    assert r['errno'] == 0
    file_list2 = baidu.get_file_list(dir=path)
    assert file_list1 != file_list2

    copied_elements = []
    for item in file_list2:
        if item not in file_list1:
            copied_elements.append(item)

    for element in copied_elements:
        copied_path = element['path']
        copied_dest = element['parent_path']
        copied_newname = element['server_filename']
        for copy_item in copy_list:
            if copy_item['path'] == copied_path and copy_item['dest'] == copied_dest and copy_item.get('newname', '') == copied_newname:
                break
        else:
            assert False


def test_file_folder_move():
    move_list = [{"path": "/test/kid1/new_name.txt",
                  "dest": "/test/kid1/child4", "newname": "new_name.txt"}]
    r = baidu.file_folder_move(move_list)
    assert r['errno'] == 0
    for move_item in move_list:
        moved_element = None
        destination_path = move_item['dest'] + '/' + move_item['newname']
        file_list = baidu.get_file_list(dir=move_item['dest'])
        for item in file_list:
            if item['path'] == destination_path:
                moved_element = item
                break
        assert moved_element is not None

def test_get_recycle_list():
    r=baidu.get_recycle_list()
    # baidu.saveJson('./files/recycle.json',r)
    assert (r['errno'] == 0)
    assert isinstance(r['list'], list)

def test_recycle_delete():
    file_list1 = baidu.get_recycle_list()['list']
    test_list=[1031287892492128]
    r=baidu.recycle_delete(delete_list=test_list)
    assert (r['errno'] == 0)
    file_list2 = baidu.get_recycle_list()['list']
    assert (file_list1 != file_list2)
    new_elements = []
    for item in file_list2:
        if item not in file_list1:
            new_elements.append(item)
            break
    for element in new_elements:
        assert (element['fs_id'] in test_list)





def test_recycle_restore():
    # file_list1 = baidu.get_recycle_list()['list']
    test_list=[461895645069165]
    r=baidu.recycle_restore(restore_list=test_list)
    assert (r['errno'] == 0)
    assert(len(r['faillist'])==0)


def test_recycle_clear():
    r=baidu.recycle_clear()
    assert (r['errno'] == 0)
    is_ok=True
    while(is_ok):
        res=baidu.test_task_status(taskid=r['taskid'])
        assert res
        if res['status']=='success':
            print('task done')
            is_ok=False
    r2=baidu.get_recycle_list()
    assert (r2['errno'] == 0)
    assert (len(r2['list'])==0)

def test_get_quota():
    r=baidu.get_quota()
    assert (r['errno'] == 0)
    assert (r['total'] != 0)
    assert (r['used'] != 0)
    print(r['total'] ,r['used'])


test_get_quota()
