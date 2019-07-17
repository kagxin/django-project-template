
"""
create database django_template character set utf8;
"""
DATABASES = {
    'default': {
        'NAME': 'django_template',
        'ENGINE': 'django.db.backends.mysql',
        'USER': 'root',
        'PASSWORD': 'root',
        'HOST': '',
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

MONGODB_DATABASES = {
    "default": {
        "name": 'django_template',
        "host": 'localhost:3717',
        "password": 'password',
        "username": 'username',
        "tz_aware": True,  # if you using timezones in django (USE_TZ = True)
    },
}

## other local setting
