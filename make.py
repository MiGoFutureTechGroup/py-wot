# -*- coding: utf-8 -*-

import os
import sys

from django.conf import settings

import MySQLdb

def clean_db():
    default_db = settings.DATABASES['default']
    if default_db['ENGINE'] == 'django.db.backends.mysql':
        sql = '''
        BEGIN;
        DROP SCHEMA IF EXISTS `{0}`;
        CREATE SCHEMA `{0}`
            DEFAULT CHARACTER SET utf8mb4
            COLLATE utf8mb4_unicode_ci ;
        COMMIT;
        '''.format(default_db['NAME'])
        print('Review SQL:', sql)
        conn = MySQLdb.connect(host=default_db['HOST'],
            port=default_db['PORT'],
            user=default_db['USER'],
            passwd=default_db['PASSWORD'])
        cursor = conn.cursor()
        cursor.execute(sql)
        print('Done database cleaning.')


if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "pywot.settings")
    print('Running ...')
    clean_db()
