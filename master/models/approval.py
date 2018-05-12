# -*- coding: utf-8 -*-

from datetime import datetime

from django.db import models
from django.conf import settings

class ApprovalModel(models.Model):

    class Meta:
        abstract = False
        get_latest_by = ('-atime',)
        verbose_name = u'批准记录'
        verbose_name_plural = u'批准记录'

    # 批准人
    approver = models.ForeignKey(\
        settings.AUTH_USER_MODEL,
        verbose_name=u'批准人 ID',
        on_delete=models.PROTECT,
        related_name='approver',
        null=False)

    # 批准时间
    atime = models.DateTimeField(\
        verbose_name=u'批准时间',
        null=False)

    ###########################################################################

    def __str__(self):
        return '{}({}[{}])'.format(\
            type(self).__name__,
            self.approver,
            self.atime.strftime('%Y/%m/%d %H:%M:%S'))

class ApprovalTarget(models.Model):

    class Meta:
        abstract = True

    approval = models.ForeignKey(\
        'ApprovalModel',
        verbose_name=u'批号',
        on_delete=models.SET_NULL,
        related_name='+',
        null=True)
