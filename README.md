# 数据库

## MySQL

>Django 支持 MySQL 5.5 以上版本

首先安装 [MySQL Client 1.3.12](https://pypi.python.org/pypi/mysqlclient) 模块：

```bash
pip install mysqlclient
```

再创建 MySQL 数据库：

```mysql
CREATE SCHEMA `django_db` DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci ;
```

#### 参考文档
1. [mysql notes](https://docs.djangoproject.com/en/dev/ref/databases/)
