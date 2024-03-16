<h1 align="center">pyalioss_util</h1>

- alioss_util.py

阿里云oss，使用示例：

```python
access_key_id = ''
access_key_secret = ''
endpoint = 'http://oss-cn-hangzhou.aliyuncs.com'
bucket_name = ''

oss = AliyunOSS(access_key_id, access_key_secret, endpoint, bucket_name)

# 上传对象
object_name = 'test2/docker_test.py'
file_path = '../docker/docker_test.py'
oss.upload_object(object_name, file_path)

# 下载对象
local_file_path = './docker_test.py'
oss.download_object(object_name, local_file_path)
# 删除对象
oss.delete_object(object_name)
# 遍历存储桶中的所有对象
objects = oss.list_files_in_directory()
print(objects)
```
