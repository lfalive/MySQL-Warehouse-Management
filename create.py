import time

import pymysql

from str import DBUser, DBPw

# 连接数据库
conn = pymysql.connect(host='localhost', port=3306, user=DBUser, passwd=DBPw, database='warehouse')
curs = conn.cursor()

# CREATE TABLE
curs.execute("CREATE TABLE IF NOT EXISTS d_code("
			 "code VARCHAR(6) PRIMARY KEY,"
			 "name VARCHAR(20) NOT NULL UNIQUE);")

curs.execute("CREATE TABLE IF NOT EXISTS device("
			 "code VARCHAR(6) PRIMARY KEY REFERENCES d_code(code),"
			 "now_number SMALLINT UNSIGNED NULL,"
			 "total_number SMALLINT UNSIGNED NULL);")

curs.execute("CREATE TABLE IF NOT EXISTS d_in("
			 "code VARCHAR(6) NOT NULL,"
			 "in_date DATE,"
			 "provider VARCHAR(20) NULL,"
			 "in_number SMALLINT NULL,"
			 "price SMALLINT NULL,"
			 "buyer VARCHAR(10) NULL,"
			 "submitdate timestamp PRIMARY KEY DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,"
			 "FOREIGN KEY (code) REFERENCES d_code(code));")

curs.execute("CREATE TABLE IF NOT EXISTS d_out("
			 "code VARCHAR(6) NOT NULL,"
			 "department VARCHAR(20) NULL,"
			 "out_date DATE,"
			 "out_person VARCHAR(10) NULL,"
			 "out_number SMALLINT NOT NULL,"
			 "taker VARCHAR(10) NULL,"
			 "submitdate timestamp PRIMARY KEY DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,"
			 "FOREIGN KEY (code) REFERENCES d_code(code));")

curs.execute("CREATE TABLE IF NOT EXISTS d_return("
			 "code VARCHAR(6) NOT NULL,"
			 "return_date DATE,"
			 "return_number SMALLINT NULL,"
			 "return_department VARCHAR(20) NULL,"
			 "submitdate timestamp PRIMARY KEY DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,"
			 "FOREIGN KEY (code) REFERENCES d_code(code));")

# CREATE VIEW
curs.execute("CREATE OR REPLACE VIEW in_out_return(code,name,type,date,number,department,provider) AS "
			 "SELECT OP.code,d_code.name,'采购入库',OP.in_date,OP.in_number,'NONE',OP.provider "
			 "FROM d_in OP,d_code "
			 "WHERE OP.code=d_code.code "
			 "UNION "
			 "SELECT OP.code,d_code.name,'借用设备',OP.out_date,OP.out_number,OP.department,'NONE' "
			 "FROM d_out OP,d_code "
			 "WHERE OP.code=d_code.code "
			 "UNION "
			 "SELECT OP.code,d_code.name,'归还设备',OP.return_date,OP.return_number,OP.return_department,'NONE' "
			 "FROM d_return OP,d_code "
			 "WHERE OP.code=d_code.code ;")

# CREATE TRIGGER
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

curs.execute("CREATE TRIGGER TRI_d_insert_device "
			 "AFTER INSERT ON d_code "
			 "FOR EACH ROW "
			 "INSERT INTO device VALUES (new.code,0,0);")

# test trigger
sql = "INSERT INTO d_code VALUES(%s,%s);"
data = [
	('001', 'Macbook Pro'),
	('002', 'iPad Pro 2020'),
	('003', 'iPhone 11 Max Pro'),
	('004', 'HUAWEI mate 30 Pro'),
	('005', 'HUAWEI P40 Pro'),
	('006', 'XIAOMI 10')
]
# 拼接并执行sql语句
# curs.executemany(sql, data)
# sql = "INSERT INTO device VALUES(%s,%s,%s);"
# data = [
# 	('001', 0, 0),
# 	('002', 0, 0),
# 	('003', 0, 0),
# 	('004', 0, 0),
# 	('005', 0, 0),
# 	('006', 0, 0)
# ]
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

# # test in
curs.execute("SELECT * FROM device;")
results = curs.fetchall()
print("\nBEFORE IN ", end="")
print(results)
curs.execute(
	"INSERT INTO d_in(code, in_date, provider, in_number, price, buyer) "
	"VALUES('001','2020-06-09','Apple',600,6999,'Tony');")
time.sleep(1)
curs.execute(
	"INSERT INTO d_in(code, in_date, provider, in_number, price, buyer) "
	"VALUES('002','2020-06-09','Apple',600,8999,'Tony');")
time.sleep(1)
curs.execute(
	"INSERT INTO d_in(code, in_date, provider, in_number, price, buyer) "
	"VALUES('003','2020-06-09','Apple',600,9999,'Tony');")
time.sleep(1)
curs.execute(
	"INSERT INTO d_in(code, in_date, provider, in_number, price, buyer) "
	"VALUES('004','2020-07-01','Huawei',600,4999,'Tony');")
time.sleep(1)
curs.execute(
	"INSERT INTO d_in(code, in_date, provider, in_number, price, buyer) "
	"VALUES('005','2020-07-01','Huawei',600,6999,'Tony');")
time.sleep(1)
curs.execute(
	"INSERT INTO d_in(code, in_date, provider, in_number, price, buyer) "
	"VALUES('006','2020-07-01','小米',600,5999,'Tony');")
time.sleep(1)
# 提交
conn.commit()
curs.execute("SELECT * FROM device;")
results = curs.fetchall()
print("AFTER IN ", end="")
print(results)

# # test out
curs.execute("SELECT * FROM device;")
results = curs.fetchall()
print("\nBEFORE OUT ", end="")
print(results)
curs.execute("INSERT INTO d_out(code,department,out_date,out_person,out_number,taker) "
			 "VALUES('001','财务','2020-06-09','梅西',100,'C罗');")
# 提交
conn.commit()
curs.execute("SELECT * FROM device;")
results = curs.fetchall()
print("AFTER OUT ", end="")
print(results)

# # test return
curs.execute("SELECT * FROM device;")
results = curs.fetchall()
print("\nBEFORE RETURN ", end="")
print(results)
curs.execute(
	"INSERT INTO d_return(code, return_date, return_number, return_department) "
	"VALUES('001','2020-06-09',100,'财务');")
# 提交
conn.commit()
curs.execute("SELECT * FROM device;")
results = curs.fetchall()
print("AFTER RETURN ", end="")
print(results)

# test view
curs.execute("SELECT * FROM in_out_return;")
results = curs.fetchall()
for i in range(len(results)):
	print(results[i])

curs.close()
conn.close()
