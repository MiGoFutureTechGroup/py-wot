# -*- coding: utf-8 -*-

from datetime import datetime

from django.db import models
from django.core.exceptions import ValidationError

class InvalidNinException(ValidationError):
    def __init__(self, message):
        super().__init__(message)

# [GB 11643-1999 公民身份号码](https://zh.wikisource.org/wiki/GB_11643-1999_%E5%85%AC%E6%B0%91%E8%BA%AB%E4%BB%BD%E5%8F%B7%E7%A0%81)
def validate_nin(value):
    if len(value) == 18:
        # 地址码：省份
        #chunk_province  = value[:2]
        # 地址码：城市
        #chunk_city      = value[2:4]
        # 地址码：区县
        #chunk_county    = value[4:6]
        chunk_location  = value[:6]
        # 出生日期码
        chunk_birthday  = value[6:14]
        # 数字顺序码
        chunk_police    = value[14:17]
        # 校验码
        chunk_checksum  = value[17]

        # 检验出生日期
        try:
            datetime.strptime(chunk_birthday, '%Y%m%d')
        except ValueError as e:
            raise InvalidNinException(str(e))

        # 检验校验码
        try:
            total = int(value[0]) * 7 + int(value[1]) * 9 + int(value[2]) * 10 + int(value[3]) * 5 + int(value[4]) * 8 + int(value[5]) * 4 + int(value[6]) * 2 + int(value[7]) * 1 + int(value[8]) * 6 + int(value[9]) * 3 + int(value[10]) * 7 + int(value[11]) * 9 + int(value[12]) * 10 + int(value[13]) * 5 + int(value[14]) * 8 + int(value[15]) * 4 + int(value[16]) * 2
        except ValueError as e:
            raise InvalidNinException(str(e))
        else:
            total = total + ((value[17] == 'X') and 10 or int(value[17]))
            total = total % 11

            if total != 1:
                raise InvalidNinException('Invalid checksum')

    else:
        raise InvalidNinException('Invalid NIN length')

class NinField(models.CharField):
    default_validators = [validate_nin,]

    def __init__(self, *args, **kwargs):
        super().__init__(\
            verbose_name=u'身份证号',
            max_length=18,
            null=True)

