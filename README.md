### 测试
- 编写测试
```angular2html
# 测试文件
test_xxx.py

# 测试方法
def test_function_name()
    r = function_name(xx)
    assert(r == "xx")
```
- 运行测试
```
pytest  --html=./test/report.html
```
- 查看测试
```angular2html
test目录下有report.html, 在浏览器中打开即可查看
```