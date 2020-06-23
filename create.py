import pymysql

from str import DBUser, DBPw

conn = pymysql.connect(host='localhost', port=3306, user=DBUser, passwd=DBPw, database='warehouse')
curs = conn.cursor()

curs.execute("CREATE TABLE IF NOT EXISTS d_code("
			 "code VARCHAR(6) PRIMARY KEY,"
			 "name VARCHAR(20) NULL);")

curs.execute("CREATE TABLE IF NOT EXISTS d_in("
			 "code VARCHAR(6) NOT NULL REFERENCES d_code(code),"
			 "in_date DATE PRIMARY KEY,"
			 "provider VARCHAR(20) NULL,"
			 "in_number SMALLINT NULL,"
			 "price SMALLINT NULL,"
			 "buyer VARCHAR(10) NULL);")

curs.execute("CREATE TABLE IF NOT EXISTS d_out("
			 "code VARCHAR(6) NOT NULL REFERENCES d_code(code),"
			 "department VARCHAR(20) NULL,"
			 "out_date DATE PRIMARY KEY,"
			 "out_person VARCHAR(10) NULL,"
			 "out_number SMALLINT NOT NULL,"
			 "taker VARCHAR(10) NULL);")

curs.execute("CREATE TABLE IF NOT EXISTS device("
			 "code VARCHAR(6) PRIMARY KEY REFERENCES d_code(code),"
			 "now_number SMALLINT NULL,"
			 "total_number SMALLINT NULL);")

curs.execute("CREATE TABLE IF NOT EXISTS d_return("
			 "code VARCHAR(6) NOT NULL REFERENCES d_code(code),"
			 "return_date DATE PRIMARY KEY,"
			 "return_number SMALLINT NULL,"
			 "return_department SMALLINT NULL);")

curs.execute("CREATE OR REPLACE VIEW out_return(code,date,number,department,type) AS "
			 "SELECT code,out_date,out_number,department,'out' "
			 "FROM d_out "
			 "UNION "
			 "SELECT code,return_date,return_number,return_department,'return' "
			 "FROM d_return;")

# test
curs.execute("insert into d_out "
			 "values('ag','财务','2012-03-09','刘德华',50,'张学友');")
curs.execute("select * from out_return;")
results = curs.fetchall()
print(results)

curs.close()
conn.close()
