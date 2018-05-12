# -*- coding: utf-8 -*-

from django.db import models
from django.conf import settings

from master.fields import OibcField, StatusField
from .creation import CreationModel
from .approval import ApprovalTarget

class Company(CreationModel, ApprovalTarget):

    class Meta(CreationModel.Meta):
        abstract = False
        verbose_name = u'公司'
        verbose_name_plural = u'公司'

    # 公司名称
    name = models.CharField(\
        verbose_name=u'公司名称',
        max_length=128,
        null=False)

    # 公司地址
    addr = models.CharField(\
        verbose_name=u'公司地址',
        max_length=256,
        null=True)

    # 组织机构代码
    oibc = OibcField()

    # 状态
    status = StatusField()

    ###########################################################################

    def __str__(self):
        return '{}[{}]'.format(self.name, self.oibc)

class Contact(CreationModel):

    class Meta(CreationModel.Meta):
        abstract = False
        verbose_name = u'联系方式'
        verbose_name_plural = u'联系方式'

    # 用户 ID
    user = models.ForeignKey(\
        settings.AUTH_USER_MODEL,
        verbose_name=u'用户 ID',
        related_name='user_contact',
        on_delete=models.CASCADE,
        null=False)

    # 联系方式类别（座机、手机、邮箱、QQ，等）
    tag = models.CharField(\
        verbose_name=u'联系方式类别',
        max_length=16,
        null=False)

    # 联系方式值
    val = models.CharField(\
        verbose_name=u'联系方式取值',
        max_length=32,
        null=False)

    ###########################################################################

    def __str__(self):
        return '{} : {} = {}'.format(self.user, self.tag, self.val)
