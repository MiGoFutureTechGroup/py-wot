# -*- coding: utf-8 -*-

from django.contrib import admin

from .models import *

# Register your models here.
admin.site.register(Company)
admin.site.register(Contact)
admin.site.register(AbstractMaterial)
admin.site.register(RealMaterial)
admin.site.register(QuotationSheet)
admin.site.register(QuotationDetail)
admin.site.register(UserDetail)
admin.site.register(CreationStatus)
