from contextlib import closing

from django.db import connection


def get_all_users():
    sql = "select * from referer_tgUser"
    with closing(connection.cursor()) as cursor:
        cursor.execute(sql)
        result = cursor.fetchall()
    return result
