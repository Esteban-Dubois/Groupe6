from flask import Flask, request, render_template, redirect, url_for, abort, flash, session, g
import pymysql
import os
from urllib.parse import urlparse
import pymysql.cursors

def get_db():
    if 'db' not in g:

        if os.environ.get('DATABASE_URL'):
            url = urlparse(os.environ.get('DATABASE_URL'))
            g.db = pymysql.connect(
                host=url.hostname,
                user=url.username,
                password=url.password,
                database=url.path[1:],
                port=url.port,
                cursorclass=pymysql.cursors.DictCursor
            )

        else:
            g.db = pymysql.connect(
                host=os.environ.get('DB_HOST'),
                user=os.environ.get('DB_USER'),
                password=os.environ.get('DB_PASSWORD'),
                database=os.environ.get('DB_NAME'),
                charset='utf8mb4',
                cursorclass=pymysql.cursors.DictCursor
            )
            #activate_db_options(g.db)
    return g.db



def activate_db_options(db):
    cursor = db.cursor()
    # Vérifier et activer l'option ONLY_FULL_GROUP_BY si nécessaire
    cursor.execute("SHOW VARIABLES LIKE 'sql_mode'")
    result = cursor.fetchone()
    if result:
        modes = result['Value'].split(',')
        if 'ONLY_FULL_GROUP_BY' not in modes:
            print('MYSQL : il manque le mode ONLY_FULL_GROUP_BY')   # mettre en commentaire
            cursor.execute("SET sql_mode=(SELECT CONCAT(@@sql_mode, ',ONLY_FULL_GROUP_BY'))")
            db.commit()
        else:
            print('MYSQL : mode ONLY_FULL_GROUP_BY  ok')   # mettre en commentaire
    # Vérifier et activer l'option lower_case_table_names si nécessaire
    cursor.execute("SHOW VARIABLES LIKE 'lower_case_table_names'")
    result = cursor.fetchone()
    if result:
        if result['Value'] != '0':
            print('MYSQL : valeur de la variable globale lower_case_table_names differente de 0')   # mettre en commentaire
            cursor.execute("SET GLOBAL lower_case_table_names = 0")
            db.commit()
        else :
            print('MYSQL : variable globale lower_case_table_names=0  ok')    # mettre en commentaire
    cursor.close()
