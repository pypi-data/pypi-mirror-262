<h1 align="center">pydocker_util</h1>

- docker_util.py

检测/控制docker，使用示例：

```python
# 当前运行的服务
remote_host = "tcp://192.168.1.1:2375"
test = DockerController(remote_host)
print(f"总共有这些服务正在运行：{test.list_running_object_containers()}")

# 暂停容器
test.stop_container('postgres')

# 删除容器
test.remove_container('postgres')

# 获取单个容器
test.inspect_container('postgres')
```
