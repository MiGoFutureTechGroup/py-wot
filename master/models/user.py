# -*- coding: utf-8 -*-

from django.db import models
from django.conf import settings
from django.utils import timezone as tz

from master.fields import NinField
from .creation import CreationModel

# 用户详情
class UserDetail(CreationModel):

    class Meta(CreationModel.Meta):
        abstract = False
        verbose_name = u'用户详情'
        verbose_name_plural = u'用户详情'

    # 所属用户 ID
    user = models.ForeignKey(\
        settings.AUTH_USER_MODEL,
        verbose_name=u'用户 ID',
        on_delete=models.PROTECT,
        related_name='user',
        null=False)

    # 所属公司 ID
    company = models.ForeignKey(\
        'Company',
        verbose_name=u'公司 ID',
        on_delete=models.PROTECT,
        null=True)

    # 入职时间
    date_registration = models.DateField(\
        verbose_name=u'入职时间',
        auto_now=False,
        auto_now_add=True)

    # 离职时间
    date_resignation = models.DateField(\
        verbose_name=u'离职时间',
        default=None,
        null=True)

    # 身份证号
    nin = NinField()

    ###########################################################################

    def __str__(self):
        return '{}'.format(self.user.username)
