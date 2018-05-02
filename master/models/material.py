# -*- coding: utf-8 -*-

from django.db import models
from django.conf import settings

from .company import Company

class AbstractMaterial(models.Model):

    class Meta:
        get_latest_by = 'ctime'
        ordering = ('name',)

    # 品名
    name = models.CharField(max_length=128)
    # 料号
    part_number = models.CharField(max_length=128)
    # 规格
    gauge = models.CharField(max_length=128)
    # 备注
    comment = models.CharField(max_length=1024)

    # 创建者 ID
    cuid = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)
    # 创建时间
    ctime = models.DateField(auto_now=False, auto_now_add=True)

    def __str__(self):
        return '{} {}[{}]'.format(self.name, self.part_number, self.gauge)

class RealMaterial(models.Model):

    class Meta:
        get_latest_by = 'ctime'
        ordering = ('material', 'provider',)

    # 物料 ID
    material = models.ForeignKey(AbstractMaterial, on_delete=models.SET_NULL, null=True)
    # 供应商 ID
    provider = models.ForeignKey(Company, on_delete=models.CASCADE, null=False)
    # 供方料号
    part_number = models.CharField(max_length=128, blank=True)

    # 外观特征
    guise = models.CharField(max_length=128)
    # 设计图纸
    design = models.CharField(max_length=1024)
    # 实物照片
    photo = models.CharField(max_length=1024)

    # 包装量单位
    quantity_unit = models.CharField(max_length=4)
    # 最小包装量
    mpq = models.PositiveIntegerField()
    # 最小订单量
    moq = models.PositiveIntegerField()
    # 生产周期（单位：小时）
    pp = models.PositiveSmallIntegerField()
    # 备注
    comment = models.CharField(max_length=1024)

    # 创建者 ID
    cuid = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)
    # 创建时间
    ctime = models.DateField(auto_now=False, auto_now_add=True)
