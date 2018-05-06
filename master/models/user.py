# -*- coding: utf-8 -*-

from django.db import models
from django.conf import settings
from django.utils import timezone as tz

from master.fields import NinField
from .creation import CreationModel

# 用户详情
class UserDetail(CreationModel):

    FEMALE = 2
    MALE = 3

    GENDER_CHOICES = (
        (FEMALE, u'女'),
        (MALE, u'男'),
    )

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

    # 性别
    gender = models.PositiveSmallIntegerField(\
        verbose_name=u'性别',
        choices=GENDER_CHOICES,
        null=True)

    # 生日
    birth = models.DateField(\
        verbose_name=u'生日',
        null=True)

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

    last_login = models.DateTimeField(\
        verbose_name=u'上次登录时间',
        editable=False,
        null=True)

    last_login_ip = models.GenericIPAddressField(\
        verbose_name=u'上次登录 IP',
        protocol='both',
        unpack_ipv4=True,
        editable=False,
        null=True)

    ###########################################################################

    def __str__(self):
        return '{}'.format(self.user.username)
