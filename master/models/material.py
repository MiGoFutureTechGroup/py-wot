# -*- coding: utf-8 -*-

from django.db import models
from django.conf import settings

from .company import Company
from .creation import CreationModel

class AbstractMaterial(CreationModel):

    class Meta(CreationModel.Meta):
        abstract = False
        ordering = ('name',)

    # 品名
    name = models.CharField(\
        verbose_name=u'品名',
        max_length=128)

    # 料号
    part_number = models.CharField(\
        verbose_name=u'料号',
        max_length=128)

    # 规格
    gauge = models.CharField(\
        verbose_name=u'规格',
        max_length=128)

    # 备注
    comment = models.CharField(\
        verbose_name=u'备注',
        max_length=1024)

    ###########################################################################

    def __str__(self):
        return '{} {}[{}]'.format(self.name, self.part_number, self.gauge)

class RealMaterial(CreationModel):

    class Meta(CreationModel.Meta):
        abstract = False
        ordering = ('material', 'provider',)

    # 物料 ID
    material = models.ForeignKey(\
        AbstractMaterial,
        verbose_name=u'抽象物料 ID',
        on_delete=models.SET_NULL,
        null=True)

    # 供应商 ID
    provider = models.ForeignKey(\
        Company,
        verbose_name=u'供应商 ID',
        on_delete=models.CASCADE,
        null=False)

    # 品牌
    brand = models.CharField(\
        verbose_name=u'品牌',
        max_length=128)

    # 供方料号
    part_number = models.CharField(\
        verbose_name=u'供方料号',
        max_length=128,
        null=False,
        blank=False)

    # 规格
    gauge = models.CharField(\
        verbose_name=u'规格',
        max_length=128)

    # 设计图纸
    design = models.CharField(\
        verbose_name=u'设计图纸',
        max_length=1024)

    # 实物照片
    photo = models.CharField(\
        verbose_name=u'实物照片',
        max_length=1024)

    # 包装量单位
    quantity_unit = models.CharField(\
        verbose_name=u'包装量单位',
        max_length=4)

    # 最小包装量
    mpq = models.PositiveIntegerField(\
        verbose_name=u'最小包装量')

    # 最小订单量
    moq = models.PositiveIntegerField(\
        verbose_name=u'最小订单量')

    # 生产周期（单位：小时）
    pp = models.PositiveSmallIntegerField(\
        verbose_name=u'生产周期（小时）')

    # 备注
    comment = models.CharField(\
        max_length=1024)

    ###########################################################################

    def __str__(self):
        return '{} {}[{}] {}'.format(self.brand, self.part_number, self.gauge, self.provider)