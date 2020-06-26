import pymysql

from str import DBUser, DBPw

conn = pymysql.connect(host='localhost', port=3306, user=DBUser, passwd=DBPw, database='warehouse')
curs = conn.cursor()

def query():
    curs.execute("select * from device;")
    results = curs.fetchall()
    return results