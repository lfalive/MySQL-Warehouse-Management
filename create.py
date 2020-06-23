import pymysql

from str import DBUser, DBPw

conn = pymysql.connect(host='localhost', port=3306, user=DBUser, passwd=DBPw, database='warehouse')
curs = conn.cursor()

sql = ("CREATE TABLE d_code("
	   "code VARCHAR(6) PRIMARY KEY,"
	   "name VARCHAR(20) NULL);")
curs.execute(sql)

sql = ("CREATE TABLE d_in("
	   "code VARCHAR(6) NOT NULL,"
	   "in_date DATE PRIMARY KEY,"
	   "provider VARCHAR(20) NULL,"
	   "telenno VARCHAR(10) NULL,"
	   "in_number SMALLINT NULL,"
	   "price SMALLINT NULL,"
	   "buyer VARCHAR(10) NULL);")
curs.execute(sql)

sql = ("CREATE TABLE d_out("
	   "code VARCHAR(6) NOT NULL,"
	   "department VARCHAR(20) NULL,"
	   "out_date DATE PRIMARY KEY,"
	   "out_person VARCHAR(10) NULL,"
	   "out_number SMALLINT NOT NULL,"
	   "taker VARCHAR(10) NULL);")
curs.execute(sql)

sql = ("CREATE TABLE device("
	   "code VARCHAR(6) PRIMARY KEY,"
	   "now_number SMALLINT NULL,"
	   "total_number SMALLINT NULL);")
curs.execute(sql)

sql = ("CREATE TABLE d_return("
	   "code VARCHAR(6) NOT NULL,"
	   "return_date DATE PRIMARY KEY,"
	   "return_number SMALLINT NULL,"
	   "return_apartment SMALLINT NULL);")
curs.execute(sql)

curs.close()
conn.close()
