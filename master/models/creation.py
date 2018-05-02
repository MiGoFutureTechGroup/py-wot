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
        on_delete=models.PROTECT)

    # 创建时间
    ctime = models.DateField(\
        auto_now=False,
        auto_now_add=True)
