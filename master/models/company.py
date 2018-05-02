# -*- coding: utf-8 -*-

from django.db import models
from django.conf import settings

class Company(models.Model):

    class Meta:
        pass

    # 公司名称
    name = models.CharField(max_length=128)
    # 公司地址
    addr = models.CharField(max_length=256)
    # 组织机构代码
    oibc = models.CharField(max_length=32)

    # 创建者 ID
    cuid = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)
    # 创建时间
    ctime = models.DateField(auto_now=False, auto_now_add=True)

    def __str__(self):
        return '{}'.format(self.name)

class Contact():

    class Meta:
        pass

    # 用户 ID
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    # 联系方式类别（座机、手机、邮箱、QQ，等）
    tag = models.CharField(max_length=16)
    # 联系方式值
    val = models.CharField(max_length=32)
