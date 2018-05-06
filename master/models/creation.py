# -*- coding: utf-8 -*-

from django.db import models
from django.conf import settings

class CreationModel(models.Model):

    class Meta:
        abstract = True
        get_latest_by = ('-ctime',)

    # 创建者 ID
    cuid = models.ForeignKey(\
        settings.AUTH_USER_MODEL,
        verbose_name=u'创建者 ID',
        on_delete=models.PROTECT)

    # 创建时间
    ctime = models.DateTimeField(\
        verbose_name=u'创建时间',
        auto_now=False,
        auto_now_add=True)

class CreationStatus(models.Model):

    class Meta:
        abstract = False
        ordering = ('value',)

    # 【主键】状态值
    value = models.PositiveIntegerField(\
        verbose_name=u'状态值',
        primary_key=True,
        null=False)

    # 状态名
    name = models.CharField(\
        verbose_name=u'状态名',
        max_length=32,
        unique=True,
        null=False)
