# -*- coding: utf-8 -*-


'''

Django 支持 MySQL 5.5 以上版本
[mysql notes](https://docs.djangoproject.com/en/dev/ref/databases/)
首先安装 [MySQL Client 1.3.12](https://pypi.python.org/pypi/mysqlclient) 模块：
```bash
pip install mysqlclient
```
再创建 MySQL 数据库：
```mysql
CREATE SCHEMA `realtime_db` DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci ;
CREATE SCHEMA `history_db` DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci ;
```

@see https://docs.djangoproject.com/en/2.0/topics/db/multi-db/#topics-db-multi-db-routing

'''

import os

'''
映射实时数据库
'''
class RealtimeDatabaseRouter:

    def db_for_read(self, model, **hints):
        if model._meta.app_label == 'realtime':
            return 'realtime_db'
        return None

    def db_for_write(self, model, **hints):
        if model._meta.app_label == 'realtime':
            return 'realtime_db'
        return None

    def allow_relation(self, obj1, obj2, **hints):
        if obj1._meta.app_label == 'realtime' or \
           obj2._meta.app_label == 'realtime':
           return True
        return None

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        if app_label == 'realtime':
            return db == 'realtime_db'
        return None

'''
映射历史数据库
'''
class HistoryDatabaseRouter:

    def db_for_read(self, model, **hints):
        if model._meta.app_label == 'history':
            return 'history_db'
        return None

    def db_for_write(self, model, **hints):
        if model._meta.app_label == 'history':
            return 'history_db'
        return None

    def allow_relation(self, obj1, obj2, **hints):
        if obj1._meta.app_label == 'history' or \
           obj2._meta.app_label == 'history':
           return True
        return None

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        if app_label == 'history':
            return db == 'history_db'
        return None
