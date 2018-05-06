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

    # 报价单编号
    quotation_number = models.CharField(\
        verbose_name=u'报价单编号',
        max_length=32,
        null=False)

    # 需方公司 ID
    demander = models.ForeignKey(\
        'Company',
        verbose_name=u'需方公司 ID',
        on_delete=models.CASCADE,
        related_name='demander',
        null=False)

    # 供方公司 ID
    supplier = models.ForeignKey(\
        'Company',
        verbose_name=u'供方公司 ID',
        on_delete=models.CASCADE,
        related_name='supplier',
        null=False)

    # 起效时间
    date_onset = models.DateField(\
        verbose_name=u'起效时间',
        auto_now=True,
        auto_now_add=False)

    # 有效时间
    # 本字段为空（NULL）时，表示该报价单直至新报价单生效前长期有效
    date_offset = models.DurationField(\
        verbose_name=u'有效时间',
        null=True)

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
        on_delete=models.CASCADE,
        null=False)

    # 物料 ID
    real_material = models.ForeignKey(\
        'RealMaterial',
        verbose_name=u'真实物料 ID',
        on_delete=models.CASCADE,
        null=False)

    # 价格单位
    price_unit = models.CharField(\
        verbose_name=u'价格单位',
        max_length=4,
        null=False)

    # 条件价格
    # TODO 不同条件下有不同的价格
    # 例如，期市铜价浮动会影响铜制品单价
    price_condition = models.BooleanField(\
        verbose_name=u'条件价格',
        default=False)

    # 税前单价
    price = models.FloatField(\
        verbose_name=u'税前单价',
        null=False)

    # 税率
    tax_rate = models.FloatField(\
        verbose_name=u'税率',
        null=True)

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
        return '{} : {} = {} {} {}/{}'.format(\
            self.quotation_sheet,
            self.real_material,
            self.tax_rate and u'含税' or u'未税',
            self.price * (1.0 + self.tax_rate or 0.0),
            self.price_unit,
            self.real_material.quantity_unit)

class QuotationPrice(models.Model):

    # 铜
    CU = 29
    # 铝
    AL = 13
    # 锌
    ZN = 30
    # 铅
    PB = 82
    # 镍
    NI = 28
    # 锡
    SN = 50
    # 金
    AU = 79
    # 银
    AG = 47
    # 螺纹钢
    RB = 10001
    # 线材
    WR = 10002
    # 热轧卷板
    HC = 10003
    # 燃料油
    FU = 10004
    # 石油沥青
    BU = 10005
    # 天然橡胶
    RU = 10006

    CONDITION_TARGETS = (
        (CU, u'铜'),
        (AL, u'铝'),
        (ZN, u'锌'),
        (PB, u'铅'),
        (NI, u'镍'),
        (SN, u'锡'),
        (AU, u'金'),
        (AG, u'银'),
        (RB, u'螺纹钢'),
        (WR, u'线材'),
        (HC, u'热轧卷板'),
        (FU, u'燃料油'),
        (BU, u'石油沥青'),
        (RU, u'天然橡胶'),
    )

    class Meta(CreationModel.Meta):
        abstract = False
        verbose_name = u'条件价格'
        verbose_name_plural = u'条件价格'

    # 报价明细 ID
    detail = models.ForeignKey(\
        'QuotationDetail',
        verbose_name=u'报价明细 ID',
        on_delete=models.CASCADE,
        null=False)

    # 价格条件
    condition_target = models.PositiveSmallIntegerField(\
        verbose_name=u'价格条件',
        choices=CONDITION_TARGETS,
        null=False)

    # 价格区间下界
    condition_lowerbound = models.FloatField(\
        verbose_name=u'价格区间下界',
        null=False)

    # 价格区间上界
    condition_upperbound = models.FloatField(\
        verbose_name=u'价格区间上界',
        null=False)

    # 税前单价
    price = models.FloatField(\
        verbose_name=u'税前单价',
        null=False)

    ###########################################################################

    def __str__(self):
        return '{} - {} = {} {} {}/{}'.format(\
            self.condition_lowerbound,
            self.condition_upperbound,
            self.detail.tax_rate and u'含税' or u'未税',
            self.price * (1.0 + self.detail.tax_rate or 0.0),
            self.detail.price_unit,
            self.real_material.quantity_unit)
