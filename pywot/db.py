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

class BaseDatabaseRouter:

    def db_for_read(self, model, **hints):
        if model._meta.app_label in self.app_labels:
            return self.db_name

        return None

    def db_for_write(self, model, **hints):
        if model._meta.app_label in self.app_labels:
            return self.db_name

        return None

    def allow_relation(self, obj1, obj2, **hints):
        if obj1._meta.app_label in self.app_labels\
                or obj2._meta.app_label in self.app_labels:
            return True

        return None

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        if app_label in self.app_labels:
            return True

        return None

'''
映射实时数据库
'''
class RealtimeDatabaseRouter(BaseDatabaseRouter):
    app_labels = ('realtime',)
    db_name = 'realtime_db'

'''
映射历史数据库
'''
class HistoryDatabaseRouter(BaseDatabaseRouter):
    app_labels = ('history', 'master',)
    db_name = 'history_db'
