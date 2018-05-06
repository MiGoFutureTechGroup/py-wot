# -*- coding: utf-8 -*-

from datetime import datetime

from django.db import models
from django.core.exceptions import ValidationError

class InvalidOibcException(ValidationError):
    def __init__(self, message):
        super().__init__(message)

# [GB 32100-2015 法人和其他组织统一社会信用代码编码规则](https://zh.wikisource.org/wiki/GB_32100-2015_%E6%B3%95%E4%BA%BA%E5%92%8C%E5%85%B6%E4%BB%96%E7%BB%84%E7%BB%87%E7%BB%9F%E4%B8%80%E7%A4%BE%E4%BC%9A%E4%BF%A1%E7%94%A8%E4%BB%A3%E7%A0%81%E7%BC%96%E7%A0%81%E8%A7%84%E5%88%99)
def validate_oibc(value):
    pass

class OibcField(models.CharField):
    default_validators = [validate_oibc,]

    def __init__(self, *args, **kwargs):
        super().__init__(\
            verbose_name=u'组织机构代码',
            max_length=18,
            null=False,
            unique=True)

