# django-project-template
> Python django project template
一个携带常用模块和定制化的django的工程模板，为了快速启动一个工程进行开发,减少配置工程带来的工作量

## demo
> apps/demo 这个app是一个示例app 

## 特点
* 环境变量区分站点类型 SITE_TYPE=staging, SITE_TYPE=production
* 重写drf mixin类的Response使http状态码为固定200
* 使用http接口返回数据格式为固定为,code message data 三个字段
* 重写exception_handler,使其支持 CustomAPIException,方便raise 自定义异常

> 使用示例请见app demo

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

#### 添加oss上传storage [django-aliyun-oss2-storage](https://github.com/xiewenya/django-aliyun-oss2-storage)
> 配置文件中把对应的配置添加完成之后，可以到admin使用account UserPrfile中的image字段测试

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
#### 

#### 修改默认分页类
```python
from rest_framework.pagination import PageNumberPagination
class DefaultResultsSetPagination(PageNumberPagination):
    page_size = 20  #默认单页面20个
    page_size_query_param = 'page_size' #可通过该参数自己设置每页多少个
    page_query_param = "page_index"  #t通过该参数选择多少页
    max_page_size = 100     #通过url修改参数  最大单页面100个
```
> /api/v1/demo/article/?page_size=1&page_index=1


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
