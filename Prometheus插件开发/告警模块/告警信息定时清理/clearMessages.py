import psycopg2
import psycopg2.extras
import os

os.system("echo `date` > /tmp/clear.log")

try:
    conn = psycopg2.connect(host='172.30.0.101', port=5432, user='postgres', password='postgres', database='prometheus')
except Exception, e:
    print 'connection error'
    exit(1)

try:
    # conn = psycopg2.connect(host='172.30.0.101', port=5432, user='postgres', password='postgres', database='prometheus')
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    sql = "delete from pending_messages where create_time < now() -interval '30 day' "
    cur.execute(sql)
    conn.commit()

    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    sql = "delete from pending_messages where create_time < now() -interval '30 day' "
    cur.execute(sql)
    conn.commit()
except Exception, e:
    print 'delete error'
finally:
    conn.close()
