## 腾讯文档 API SDK

根据《[腾讯文档——开发文档](https://docs.qq.com/open/document/app/openapi/v2/)》实现了 API 接口。

请区分**腾讯文档**和**企业微信文档**，前者域名 docs.qq.com，后者域名是 doc.weixin.qq.com

功能特点：

- token 有 cache
- 基本接口有封装
- 合并接口封装，比如单接口实现上传文档等

### 安装

```bash
pip install qq-doc
```

### 上传 xlsx 文件并转换的示例

Demo 中有 xlsx 的文档上传到指定目录下的示例，需要替换自己的 `client_id` 和 `client_secret`。

```python
from qq_doc import QQDocAPI

client_id = "your_client_id"
client_secret = "your_client_secret"
folder_name = "test"
filename = "test.xlsx"

api = QQDocAPI(client_id, client_secret)
folder = api.create_folder_if_not_exist(folder_name)
new_file = api.upload_file(filename, folder["ID"])

# 加一个公开写权限，也可以使用publicRead, private, members
api.set_file_permission(new_file["ID"], "publicWrite")
print(new_file)
```

<img src="./images/demo.png" alt="demo.png" style="zoom:50%;" />

**注意**：腾讯文档支持同名文件的存在，所以如果多次执行，会产生多个文件，他们的ID不同，但是命名相同。请记得清理

## 接口实现情况

### 文件操作

| 接口                                                         | 方法名称      |
| :----------------------------------------------------------- | :------------ |
| [新建文档](https://docs.qq.com/open/document/app/openapi/v2/file/files/create.html) |               |
| [查询文档](https://docs.qq.com/open/document/app/openapi/v2/file/files/metadata.html) |               |
| [重命名文档](https://docs.qq.com/open/document/app/openapi/v2/file/files/update.html) |               |
| [移动文档](https://docs.qq.com/open/document/app/openapi/v2/file/files/move.html) |               |
| [删除文档](https://docs.qq.com/open/document/app/openapi/v2/file/files/delete.html) | delete_folder |
| [生成副本](https://docs.qq.com/open/document/app/openapi/v2/file/files/copy.html) |               |
| [收藏文档](https://docs.qq.com/open/document/app/openapi/v2/file/files/star.html) |               |
| [置顶文档](https://docs.qq.com/open/document/app/openapi/v2/file/files/pin.html) |               |
| [设置水印](https://docs.qq.com/open/document/app/openapi/v2/file/files/watermark/set.html) |               |
| [创建快捷方式](https://docs.qq.com/open/document/app/openapi/v2/file/files/shortcut.html) |               |
| [恢复文档](https://docs.qq.com/open/document/app/openapi/v2/file/files/recover.html) |               |

### 导入文件

| 接口                                                         | 方法名称              |
| :----------------------------------------------------------- | :-------------------- |
| [预导入文档](https://docs.qq.com/open/document/app/openapi/v2/file/import/pre_import.html) | create_import_info    |
| [异步导入文档](https://docs.qq.com/open/document/app/openapi/v2/file/import/async_import.html) | async_import_document |
| [查询导入进度](https://docs.qq.com/open/document/app/openapi/v2/file/import/import_progress.html) | get_import_progress   |
| [[封装]同步导入文档](https://docs.qq.com/open/document/app/openapi/v2/file/import/) | upload_file           |

### 导出文件

| 接口                                                         | 方法名称 |
| :----------------------------------------------------------- | :------- |
| [导出文档](https://docs.qq.com/open/document/app/openapi/v2/file/export/async_export.html) |          |
| [导出进度查询](https://docs.qq.com/open/document/app/openapi/v2/file/export/export_progress.html) |          |

### 文件夹操作

| 接口                                                         | 方法名称                   |
| :----------------------------------------------------------- | :------------------------- |
| [获取文档列表](https://docs.qq.com/open/document/app/openapi/v2/file/folders/list.html) | list_folder_contents       |
| [查询文件夹信息](https://docs.qq.com/open/document/app/openapi/v2/file/folders/metadata.html) | get_folder_metadata        |
| [封装]根据文件名获得文件列表                                 | get_folder_by_name         |
| [添加文件夹](https://docs.qq.com/open/document/app/openapi/v2/file/folders/add.html) | create_folder              |
| [封装]创建文件夹如果不存在                                   | create_folder_if_not_exist |
| [删除文件夹](https://docs.qq.com/open/document/app/openapi/v2/file/folders/delete.html) | delete_folder              |
| [查询文件夹权限](https://docs.qq.com/open/document/app/openapi/v2/file/folders/get_permission.html) |                            |
| [移动文件夹](https://docs.qq.com/open/document/app/openapi/v2/file/folders/move.html) |                            |
| [重命名文件夹](https://docs.qq.com/open/document/app/openapi/v2/file/folders/update.html) |                            |

### 文档权限

| 接口                                                         | 方法名称            |
| :----------------------------------------------------------- | :------------------ |
| [查询用户访问权限](https://docs.qq.com/open/document/app/openapi/v2/file/files/access.html) | get_file_access     |
| [转让文档所有权](https://docs.qq.com/open/document/app/openapi/v2/file/files/ownership.html) |                     |
| [查看文档权限](https://docs.qq.com/open/document/app/openapi/v2/file/files/permission/get.html) | get_file_permission |
| [设置文档权限](https://docs.qq.com/open/document/app/openapi/v2/file/files/permission/set.html) | set_file_permission |
| [申请文档权限](https://docs.qq.com/open/document/app/openapi/v2/file/files/permission/apply.html) |                     |
| [添加协作成员](https://docs.qq.com/open/document/app/openapi/v2/file/files/collaborators/add.html) | add_collaborators   |
| [移除协作成员](https://docs.qq.com/open/document/app/openapi/v2/file/files/collaborators/delete.html) |                     |
| [查询协作成员](https://docs.qq.com/open/document/app/openapi/v2/file/files/collaborators/get.html) | get_collaborators   |

### 搜索

| 接口                                                         | 方法名称 |
| :----------------------------------------------------------- | :------- |
| [列表过滤](https://docs.qq.com/open/document/app/openapi/v2/file/filter/filter.html) |          |
| [关键字搜索](https://docs.qq.com/open/document/app/openapi/v2/file/search/search.html) |          |

### 功能接口

| 接口                                                         | 方法名称 |
| :----------------------------------------------------------- | :------- |
| [fileID 转换](https://docs.qq.com/open/document/app/openapi/v2/file/util/converter.html) |          |
| [上传图片](https://docs.qq.com/open/document/app/openapi/v2/resourceapi/image/upload_image.html) |          |

### 通知

| 接口                                                         | 方法名称 |
| :----------------------------------------------------------- | :------- |
| [查询消息列表未读数量](https://docs.qq.com/open/document/app/openapi/v2/file/notification/unread_count.html) |          |