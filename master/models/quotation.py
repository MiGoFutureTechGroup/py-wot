# -*- coding: utf-8 -*-

from django.db import models
from django.conf import settings

class QuotationSheet(models.Model):

    class Meta:
        get_latest_by = 'ctime'
        ordering = ('date_onset',)

    # 需方公司 ID
    demander = models.ForeignKey('Company', on_delete=models.CASCADE, related_name='demander')
    # 供方公司 ID
    supplier = models.ForeignKey('Company', on_delete=models.CASCADE, related_name='supplier')
    # 起效时间
    date_onset = models.DateField(auto_now=True, auto_now_add=False)
    # 有效时间（单位：天）
    date_offset = models.PositiveSmallIntegerField()

    # TODO 数字签章

    # 创建者 ID
    cuid = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)
    # 创建时间
    ctime = models.DateField(auto_now=False, auto_now_add=True)

class QuotationDetail(models.Model):

    class Meta:
        pass

    # 报价单 ID
    quotation_sheet = models.ForeignKey('QuotationSheet', on_delete=models.CASCADE)
    # 物料 ID
    real_material = models.ForeignKey('RealMaterial', on_delete=models.CASCADE)

    # 价格单位
    price_unit = models.CharField(max_length=4)
    # 税前单价
    price = models.FloatField()
    # 税率
    # FIXME 税率应该独立于报价单
    #       可以考虑使用外键代替
    tax_rate = models.FloatField()
