# -*- coding: utf-8 -*-

from django.db import models
from django.conf import settings
from django.utils import timezone as tz

from master.fields import NinField

# 用户详情
class UserDetail(models.Model):

    class Meta:
        pass

    # 所属用户 ID
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name='user')

    # 所属公司 ID
    company = models.ForeignKey('Company', on_delete=models.PROTECT)
    # 入职时间
    date_registration = models.DateField(auto_now=False, auto_now_add=True)
    # 离职时间
    date_resignation = models.DateField(default=None)
    # 身份证号
    nin = NinField()

    # 创建者 ID
    cuid = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name='cuid')
    # 创建时间
    ctime = models.DateField(auto_now=False, auto_now_add=True)
