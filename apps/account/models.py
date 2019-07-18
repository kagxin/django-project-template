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
