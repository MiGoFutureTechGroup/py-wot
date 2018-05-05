# -*- coding: utf-8 -*-

from datetime import datetime, timedelta

from django.db import models
from django.conf import settings

from .creation import CreationModel

class QuotationSheet(CreationModel):

    class Meta(CreationModel.Meta):
        abstract = False
        ordering = ('date_onset',)
        verbose_name = u'报价单'
        verbose_name_plural = u'报价单'

    # 需方公司 ID
    demander = models.ForeignKey(\
        'Company',
        verbose_name=u'需方公司 ID',
        on_delete=models.CASCADE,
        related_name='demander')

    # 供方公司 ID
    supplier = models.ForeignKey(\
        'Company',
        verbose_name=u'供方公司 ID',
        on_delete=models.CASCADE,
        related_name='supplier')

    # 起效时间
    date_onset = models.DateField(\
        verbose_name=u'起效时间',
        auto_now=True,
        auto_now_add=False)

    # 有效时间（单位：天）
    date_offset = models.PositiveSmallIntegerField(\
        verbose_name=u'有效时间')

    # TODO 数字签章

    ###########################################################################

    def __str__(self):
        return '{}/{} [{}] {}-{}'.format(\
            self.supplier,
            self.demander,
            self.id,
            self.date_onset,
            self.date_onset + timedelta(self.date_offset))

class QuotationDetail(models.Model):

    class Meta(CreationModel.Meta):
        abstract = False
        verbose_name = u'报价明细'
        verbose_name_plural = u'报价明细'

    # 报价单 ID
    quotation_sheet = models.ForeignKey(\
        'QuotationSheet',
        verbose_name=u'报价单 ID',
        on_delete=models.CASCADE)

    # 物料 ID
    real_material = models.ForeignKey(\
        'RealMaterial',
        verbose_name=u'真实物料 ID',
        on_delete=models.CASCADE)

    # 价格单位
    price_unit = models.CharField(\
        verbose_name=u'价格单位',
        max_length=4)

    # 价格条件
    # TODO 不同条件下有不同的价格
    # 例如，期市铜价浮动会影响铜制品单价
    price_condition = None

    # 税前单价
    price = models.FloatField(\
        verbose_name=u'税前单价')

    # 税率
    tax_rate = models.FloatField(\
        verbose_name=u'税率')

    ###########################################################################

    # 批准时间
    approval_time = models.DateTimeField(\
        verbose_name=u'批准时间',
        null=True)

    # 批准人
    approver = models.ForeignKey(\
        settings.AUTH_USER_MODEL,
        verbose_name=u'批准人 ID',
        on_delete=models.PROTECT,
        related_name='approver',
        null=True)

    ###########################################################################

    def __str__(self):
        return '{} : {} = {} {}'.format(\
            self.quotation_sheet,
            self.real_material,
            self.price * (1.0 + tax_rate),
            self.price_unit)
