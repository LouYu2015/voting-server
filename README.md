# A Voting Website Server using Django 用 Django 开发的投票网站服务器

## Introduction 简介

This repository contains the server part of UW CSSA's voting website.
For introduction of the whole project, please see the [main project page](https://github.com/LouYu2015/voting-website).

This server only exposes a REST API to the client.
The code doesn't contain a front-end implementation.
Please refer to the main project page for the corresponding front-end implemented in React.

此仓库包含 UW CSSA 投票网站的服务器部分。
关于整体介绍，请参见主文档。

该服务器只提供 REST API 接口。
代码中不包括前端。
若要获取配套的 React 前端代码，请参见主文档。

## Security Reminder 安全提示

The `settings.py` contained in this project is for local testing only.
Please [generate a new secret key](https://stackoverflow.com/questions/41298963/is-there-a-function-for-generating-settings-secret-key-in-django) for production and replace the one in `settings.py`.

Becareful: don't commit any database password to public repositories.

项目中包含的 `settings.py` 仅用于本地测试。
正式部署时，请重新生成密钥，替换 `settings.py` 中的密钥。

小心：不要把数据库密码提交到公共仓库里。

## Code Structure 代码结构

Here are a list of important files for the project.
Most logics are in `voting/models.py`, `voting/urls.py` and `voting/views.py`.

以下是主要项目文件。
主要逻辑在 `voting/models.py`, `voting/urls.py` 和 `voting/views.py` 中。

* `mysite/`
  * `settings.py`: deployment configuration / 程序部署设置
  * `urls.py`: top level URL routing rules / 顶层 URL 规则
* `voting/`
  * `admin.py`: expose database in the admin page / 在管理员界面中显示数据库内容
  * `models.py`: define database structure / 定义数据库结构
  * `serializers.py`: define how to transfer objects in the REST API / 定义 REST API 传输结构
  * `urls.py`: URL routing rules related to voting / 投票 URL 规则
  * `views.py`: request processing logic / 处理请求的逻辑

## Deployment 部署

The following commands assume that you put our repository in `voting-server/`.

下面的代码假设你的把项目储存在 `voting-server/`。

You can create an environment with the following commands:

你可以用以下命令创建环境：

```bash
python3 -m pip install django            
python3 -m pip install djangorestframework
python3 -m pip install django-cors-headers
python3 -m pip install mysqlclient  # For MySQL deployment
```

Or use a provided virtual environment (assuming you saved it to `venv/`):

或者使用现有虚拟环境（假设储存在 `venv/` 中）：

```bash
source venv/bin/activate
```

### Testing locally 本地测试

After running the following commands, you should be able to see the management page at `http://127.0.0.1:8000/admin/`.

执行以下命令后，你应该可以在 `http://127.0.0.1:8000/admin/` 看到管理界面。

```bash
cd voting-server
python3 manage.py collectstatic
python3 manage.py makemigrations voting
python3 manage.py migrate
python3 manage.py createsuperuser
python3 manage.py runserver
```

### Depoly on Internet 在互联网上部署


The server was deployed on DreamHost, but it should be possible to migrate to other web service provider as well.
Please refer to [the documentation from your service provider](https://help.dreamhost.com/hc/en-us/articles/215319598-Django-overview) on how to deploy a Django server.

服务器曾经在 DreamHost 上部署，不过也可以移植到其他云服务商。
请参考云服务商文档，搜索如何部署 Django 项目。

Before you depoly the project, make sure you to change the following settings in `mysite/settings.py`:

* Generate a new `SECRET_KEY`
* Change `DEBUG` to `False`
* Add your API domain to `ALLOWED_HOSTS`
* Connect your database in `DATABASES`
* Add your frontend domain to `CORS_ORIGIN_WHITELIST`

在部署之前，请修改 `mysite/settings.py`：

* 生成新的 `SECRET_KEY`
* 把 `DEBUG` 改为 `False`
* 在 `ALLOWED_HOSTS` 中加入 API 的域名
* 在 `DATABASES` 中输入数据库信息
* 在 `CORS_ORIGIN_WHITELIST` 中添加前端的域名


It's a good practice to save the production settings in `setting_deploy.py` and write a script to override `settings.py` in production.

建议在 `setting_deploy.py` 中保存正式的部署设置，然后用脚本来自动替换 `settings.py`。
