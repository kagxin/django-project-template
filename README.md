# django-template
> Python django project template
一个携带常用模块和定制化的django的工程模板，为了快速启动一个工程进行开发

## demo
> apps/demo 这个app是一个示例app 

## 特点
* 重写mixin的Response使http状态码为固定200
* 使用http接口返回数据格式为固定为,code message data 三个字段
* 重写exception_handler,使其支持 CustomAPIException,方便raise 自定义异常
> 使用示例请见app demo

### 一些可能使用功能or模块用
#### 校验token是否改变（可用于自同时只允许一个用户登录）
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