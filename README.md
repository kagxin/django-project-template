# django-project-template
[![Build Status](https://travis-ci.org/kagxin/django-project-template.svg?branch=master)](https://travis-ci.org/kagxin/django-project-template)
[![Language](https://img.shields.io/badge/language-python-blue.svg)](https://python.org/)
[![LICENSE](https://img.shields.io/badge/license-MIT-000000.svg)](https://github.com/kagxin/django-project-template/blob/master/LICENSE)


> Python django project template
一个携带常用模块和定制化的django的工程模板，为了快速启动一个工程进行开发,减少配置工程带来的工作量

## 快速开始
> clone工程到本地
```bash
git clone https://github.com/kagxin/django-project-template.git
```
> 安装工程依赖包
```bash
pip install requirements.txt
```

>修改settings/local.py 中的的mysql和redis地址

 ```python
DATABASES = {
    'default': {
        'NAME': 'django_template',
        'ENGINE': 'django.db.backends.mysql',
        'USER': 'root',
        'PASSWORD': 'root',
        'HOST': '127.0.0.1',
        'TEST': {
            'NAME': 'django_template_testdb',
            'CHARSET': 'utf8'
        },
        'CHARSET': 'utf8'
    }
}
CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://127.0.0.1:6379/1",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
            "PASSWORD": ""
        }
    },
    "token": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://127.0.0.1:6379/2",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
            "PASSWORD": "",
        }
    }
}
```
>执行数据库迁移
```bash
python manage.py migrate
```
>启动工程
```bash
python manage.py runserver
```
>浏览器访问测试地址
```bash
http://localhost:8000/api/v1/demo/
```
>ok
```json
{
  "message": "hello world."
}
```

## 特点
* 环境变量区分站点类型
>使用环境变量SITE_TYPE，来区分站点类型
例如使用，export SITE_TYPE=local，启动工程的时候，使用的是settings.py/local.py 中的配置

| SITE_TYPE | 站点类型 |
| ------ | ------ |
| local | 本地 (未加环境变量时的默认配置)|
| staging |测试环境|
|production|生产环境| 
|ci|ci环境|

* 重写drf mixin类的Response使http状态码为固定200, 格式固定为code，message，data三字段
> 使用 apps.utils.view 中view和viewset，返回的json格式为

```json
{
  "code": 0,
  "message":"Success",
  "data": {}
}
```
* 使用http接口返回数据格式为固定为,code message data 三个字段
> /api/v1/demo/article/?page_index=1

```json
{
    "code": 0,
    "message": "Success",
    "data": {
        "count": 0,
        "next": null,
        "previous": null,
        "results": []
    }
}
```

* 重写exception_handler,使其支持 CustomAPIException,方便raise 自定义异常
> 在你任何想要的地方终止程序

```python
from rest_framework import serializers
from apps.core.exceptions import CustomAPIException
from apps.core import response_code
from apps.demo.models import *

class ReporterSerializer(serializers.ModelSerializer):
    full_name = serializers.CharField(required=True)

    def validate_full_name(self, value):
        if 'admin' in value.lower():
            code, message = response_code.ERR_ADMIN_IN_FULLNAME
            raise CustomAPIException(code=code, message=message)  # 终止程序返回ERR_ADMIN_IN_FULLNAME，错误信息
        return value

    class Meta:
        model = Reporter
        fields = '__all__'
```
返回异常的格式
```json
{
    "code": 41001,
    "message": "admin in fullname.",
    "data": {}
}
```
> 使用示例请见app demo

## demo
> apps/demo 这个app是一个示例app,使用了apps.utils.view中的view和viewset，使用自定义的异常类 


### 一些可能使用功能or模块用
#### 校验token是否改变（可用于同时只允许一个用户登录）
* setting.py *DEFAULT_AUTHENTICATION_CLASSES* 中使用  apps.utils.exception_handler.exception_handler

```python
REST_FRAMEWORK = {
    'DEFAULT_FILTER_BACKENDS': (
        'rest_framework_filters.backends.RestFrameworkFilterBackend',
    ),
    'EXCEPTION_HANDLER': 'apps.utils.exception_handler.exception_handler',
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),
    'DEFAULT_AUTHENTICATION_CLASSES': (
        # 'rest_framework_jwt.authentication.JSONWebTokenAuthentication',
        'apps.utils.jwt.authentication.CheckTokenChangeAuthentication',
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.BasicAuthentication',
    ),
    'DATE_FORMAT': '%Y-%m-%d',
    'DATE_INPUT_FORMATS': (
        '%Y-%m-%d', ISO_8601
    ),
    'DATETIME_FORMAT': '%Y-%m-%d %H:%M:%S',
    'DATETIME_INPUT_FORMATS': (
        '%Y-%m-%d %H:%M:%S', ISO_8601
    )
}
```

* 获取，刷新，校验token接口使用apps.utils.jwt.views 中的三个对应接口

```python
from django.urls import path, include
from apps.utils.jwt.views import obtain_jwt_check_token_change, refresh_jwt_check_token_change,\
    verify_jwt_check_token_change
urlpatterns = [
    path('token/', obtain_jwt_check_token_change),
    path('token/refresh/', refresh_jwt_check_token_change),
    path('token/verify/', verify_jwt_check_token_change),
]
```
* ok 这时如果token改变则接口会返回
```json
{
    "code": 40006,
    "message": "Token has been changed.",
    "data": {}
}
```
#### 自定User
> 自定义user在account.model.UserPrfile, 可以对其删减字段重新migrate

```python
from django.contrib.auth.models import AbstractUser
from django.db import models
class UserProfile(AbstractUser):
    """
    用户
    """
    name = models.CharField(max_length=30, null=True, blank=True, verbose_name="姓名")
    birthday = models.DateField(null=True, blank=True, verbose_name="出生年月")
    gender = models.CharField(max_length=6, choices=(("male", u"男"), ("female", "女")), default="female",
                              verbose_name="性别", blank=True)
    mobile = models.CharField(null=True, blank=True, max_length=11, verbose_name="电话")
    image = models.ImageField(blank=True, null=True,
                              upload_to="image/%Y/%m/%d")

    class Meta:
        verbose_name = "用户"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.username

```

#### 添加aliyun oss上传storage [django-aliyun-oss2-storage](https://github.com/xiewenya/django-aliyun-oss2-storage)
> 配置文件中把对应的配置添加完成之后，可以到admin使用account UserPrfile中的image字段测试
使用时，补全配置参数并解开DEFAULT_FILE_STORAGE的注释

```python

## oss
ACCESS_KEY_ID = "****"
ACCESS_KEY_SECRET = "****"
END_POINT = "oss-cn-shanghai.aliyuncs.com"
BUCKET_NAME = "****"
ALIYUN_OSS_CNAME = "" # 自定义域名，如果不需要可以不填写
BUCKET_ACL_TYPE = "private" # private, public-read, public-read-write
# mediafile将自动上传
DEFAULT_FILE_STORAGE = 'aliyun_oss2_storage.backends.AliyunMediaStorage'
# staticfile将自动上传
# STATICFILES_STORAGE = 'aliyun_oss2_storage.backends.AliyunStaticStorage'

```

#### 修改默认分页类
> 重写get_paginated_response，使response格式满足code，message，data。
修改paginate_queryset，当页面大于最后一页时（或无效页面），返回最后一页数据

```python
from rest_framework.pagination import PageNumberPagination
from apps.utils.response import simple_response
from django.core.paginator import InvalidPage

class DefaultResultsSetPagination(PageNumberPagination):
    page_size = 20  #默认单页面20个
    page_size_query_param = 'page_size' #可通过该参数自己设置每页多少个
    page_query_param = "page_index"  #t通过该参数选择多少页
    max_page_size = 100     #通过url修改参数  最大单页面100个
    
    def get_paginated_response(self, data):
        reponse_data = super().get_paginated_response(data).data
        return simple_response(data=reponse_data)

    def paginate_queryset(self, queryset, request, view=None):
        """
        Paginate a queryset if required, either returning a
        page object, or `None` if pagination is not configured for this view.
        """
        page_size = self.get_page_size(request)
        if not page_size:
            return None

        paginator = self.django_paginator_class(queryset, page_size)
        page_number = request.query_params.get(self.page_query_param, 1)
        if page_number in self.last_page_strings:
            page_number = paginator.num_pages

        try:
            self.page = paginator.page(page_number)
        except InvalidPage:  # 无效的页码返回最后一页数据
            self.page = paginator.page(paginator.num_pages)

        if paginator.num_pages > 1 and self.template is not None:
            # The browsable API should display pagination controls.
            self.display_page_controls = True

        self.request = request
        return list(self.page)
```
请求响应的示例
> /api/v1/demo/article/?page_size=1&page_index=1
```json
{
    "code": 0,
    "message": "Success",
    "data": {
        "count": 0,
        "next": null,
        "previous": null,
        "results": []
    }
}
```


## 使用docker启动工程

* build 镜像，并启动
```bash
docker-compose up
```
* 执行迁移,添加admin用户,收集静态文件
```bash
docker exec -it django_template_app sh -c "cd /home/docker/code/ && python3 manage.py migrate && python3 manage.py collectstatic && python3 manage.py createsuperuser"
```
* ok 访问7000端口
>http://localhost:7000/api/v1/demo/

* [在线示例](http://47.94.110.194:7000/api/v1/demo/) username: admin password: admin123
