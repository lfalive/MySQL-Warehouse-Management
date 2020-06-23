import pymysql

from str import DBUser, DBPw, DB

conn = pymysql.connect(host='localhost', port=3306, user=DBUser, passwd=DBPw, database=DB)
curs = conn.cursor()

curs.execute('SHOW TABLES;')
rows = curs.fetchall()

print(rows)

curs.close()
conn.close()
