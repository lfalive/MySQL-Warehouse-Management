import pymysql

from str import DBUser, DBPw

conn = pymysql.connect(host='localhost', port=3306, user=DBUser, passwd=DBPw, database='warehouse')
curs = conn.cursor()

# TABLE
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
			 "return_department VARCHAR(20) NULL);")

# VIEW
curs.execute("CREATE OR REPLACE VIEW in_out_return(code,name,type,date,number,department) AS "
			 "SELECT OP.code,d_code.name,'in',OP.in_date,OP.in_number,'-' "
			 "FROM d_in OP,d_code "
			 "WHERE OP.code=d_code.code "
			 "UNION "
			 "SELECT OP.code,d_code.name,'out',OP.out_date,OP.out_number,OP.department "
			 "FROM d_out OP,d_code "
			 "WHERE OP.code=d_code.code "
			 "UNION "
			 "SELECT OP.code,d_code.name,'return',OP.return_date,OP.return_number,OP.return_department "
			 "FROM d_return OP,d_code "
			 "WHERE OP.code=d_code.code ;")

# TRIGGER
curs.execute("CREATE TRIGGER TRI_d_out_device "
			 "AFTER INSERT ON d_out "
			 "FOR EACH ROW "
			 "UPDATE device SET now_number = now_number - NEW.out_number "
			 "				WHERE code = NEW.code;")

curs.execute("CREATE TRIGGER TRI_d_return_device "
			 "AFTER INSERT ON d_return "
			 "FOR EACH ROW "
			 "UPDATE device SET now_number = now_number + NEW.return_number "
			 "				WHERE code = NEW.code;")

curs.execute("CREATE TRIGGER TRI_d_in_device "
			 "AFTER INSERT ON d_in "
			 "FOR EACH ROW "
			 "UPDATE device SET now_number = now_number + NEW.in_number , total_number = total_number + NEW.in_number"
			 "				WHERE code = NEW.code;")

# test view
# curs.execute("insert into d_out "
# 			 "values('ag','财务','2012-03-09','刘德华',50,'张学友');")
# curs.execute("insert into d_return "
# 			 "values('ag','2012-03-10',50,'财务');")
# 提交之后才会保存本地
# conn.commit()
# curs.execute("select * from out_return;")
# results = curs.fetchall()
# print(results)

# test trigger
sql = "INSERT INTO d_code VALUES(%s,%s);"
data = [
	('001', 'Macbook Pro'),
	('002', 'iPad Pro 2020'),
	('003', 'iPhone 11 Max Pro')
]
# 拼接并执行sql语句
curs.executemany(sql, data)
sql = "INSERT INTO device VALUES(%s,%s,%s);"
data = [
	('001', 500, 500),
	('002', 600, 600),
	('003', 600, 600)
]
# 拼接并执行sql语句
curs.executemany(sql, data)
# 提交之后才会保存本地
conn.commit()

curs.execute("SELECT * FROM d_code;")
results = curs.fetchall()
print("DEVICE INFO: ", end="")
print(results)
curs.execute("SELECT * FROM device;")
results = curs.fetchall()
print("DEVICE INFO ", end="")
print(results)

# # out
curs.execute("SELECT * FROM device;")
results = curs.fetchall()
print("\nBEFORE OUT ", end="")
print(results)
curs.execute("INSERT INTO d_out VALUES('001','财务','2020-06-09','梅西',100,'C罗');")
# 提交
conn.commit()
curs.execute("SELECT * FROM device;")
results = curs.fetchall()
print("AFTER OUT ", end="")
print(results)

# # return
curs.execute("SELECT * FROM device;")
results = curs.fetchall()
print("\nBEFORE RETURN ", end="")
print(results)
curs.execute("INSERT INTO d_return VALUES('001','2020-06-09',100,'财务');")
# 提交
conn.commit()
curs.execute("SELECT * FROM device;")
results = curs.fetchall()
print("AFTER RETURN ", end="")
print(results)

# # in
curs.execute("SELECT * FROM device;")
results = curs.fetchall()
print("\nBEFORE IN ", end="")
print(results)
curs.execute("INSERT INTO d_in VALUES('001','2020-06-09','Apple',20,6999,'Tony');")
# 提交
conn.commit()
curs.execute("SELECT * FROM device;")
results = curs.fetchall()
print("AFTER IN ", end="")
print(results)

curs.close()
conn.close()
