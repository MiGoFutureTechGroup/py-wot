# -*- coding: utf-8 -*-

from django.db import models
from django.core.exceptions import ValidationError

class StatusField(models.ForeignKey):

    def __init__(self, *args, **kwargs):
        super().__init__(\
            'CreationStatus',
            verbose_name=u'状态',
            on_delete=models.PROTECT,
            null=True)
