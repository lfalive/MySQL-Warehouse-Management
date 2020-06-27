import tkinter as tk
from tkinter import ttk
import tkinter.messagebox
import pymysql

from str import DBUser, DBPw

conn = pymysql.connect(host='localhost', port=3306, user=DBUser, passwd=DBPw, database='warehouse')
curs = conn.cursor()

main_window = tk.Tk()

main_window.title('仓库数据管理系统')
main_window.geometry('850x700')
main_window.resizable(width=False, height=False)

title = tk.Label(main_window, text='欢迎使用仓库管理系统', font=('', 40)).pack(side=tk.TOP, pady=50)


def now_d_click():
	window_in = tk.Toplevel(main_window)
	window_in.geometry('800x400')
	window_in.title('现有库存')
	curs.execute("select device.code,d_code.name,now_number,total_number from device,d_code WHERE device.code = d_code.code;")
	results = curs.fetchall()

	# 创建表格
	tree_date = ttk.Treeview(window_in)

	# 定义列
	tree_date['columns'] = ['code', 'name','now_number', 'total_number']
	tree_date.pack()

	# 设置列宽度
	tree_date.column('code', width=100)
	tree_date.column('name', width=150)
	tree_date.column('now_number', width=100)
	tree_date.column('total_number', width=100)

	# 添加列名
	tree_date.heading('code', text='设备号')
	tree_date.heading('name', text='设备名称')
	tree_date.heading('now_number', text='现有库存')
	tree_date.heading('total_number', text='总数')

	# 给表格中添加数据
	i = 1
	for record in results:
		tree_date.insert('', i, text=str(i), values=(record[0], str(record[1]), str(record[2]),str(record[3])))
		i += 1


# 第一个参数为第一层级



def in_click():
	window_in = tk.Toplevel(main_window)
	window_in.geometry('600x400')
	window_in.title('采购入库登记')
	exampledate = tk.StringVar()
	exampledate.set("YYYY-mm-dd")
	ecode = tk.Entry(window_in, show = None)#显示成明文形式
	ecode.place(x=300,y=50,anchor='n')
	eindate = tk.Entry(window_in, show = None,textvariable=exampledate)#显示成明文形式
	eindate.place(x=300,y=100,anchor='n')
	eprovider = tk.Entry(window_in, show = None)#显示成明文形式
	eprovider.place(x=300,y=150,anchor='n')
	ein_number = tk.Entry(window_in, show = None)#显示成明文形式
	ein_number.place(x=300,y=200,anchor='n')
	eprice = tk.Entry(window_in, show = None)#显示成明文形式
	eprice.place(x=300,y=250,anchor='n')
	ebuyer = tk.Entry(window_in, show = None)#显示成明文形式
	ebuyer.place(x=300,y=300,anchor='n')
	tk.Label(window_in, text='设备号', font=('', 10)).place(x=200,y=50,anchor="ne")
	tk.Label(window_in, text='入库时间', font=('', 10)).place(x=200,y=100,anchor="ne")
	tk.Label(window_in, text='供应商', font=('', 10)).place(x=200,y=150,anchor="ne")
	tk.Label(window_in, text='入库数量', font=('', 10)).place(x=200,y=200,anchor="ne")
	tk.Label(window_in, text='价格', font=('', 10)).place(x=200,y=250,anchor="ne")
	tk.Label(window_in, text='采购员', font=('', 10)).place(x=200,y=300,anchor="ne")
	def in_submit():
		code = ecode.get()
		indate = eindate.get()
		provider = eprovider.get()
		in_number = ein_number.get()
		price = eprice.get()
		buyer = ebuyer.get()
		sql = "INSERT INTO d_in(code, in_date, provider, in_number, price, buyer) VALUES(%s,%s,%s,%s,%s,%s);"
		values = (code,indate,provider,int(in_number),int(price),buyer)
		curs.execute(sql,values)
		conn.commit()
		tk.messagebox.showinfo(title='Hi', message="提交完成")
		window_in.destroy()
	b_submit = tk.Button(window_in, text='提交', font=('',10), width=8, height=3, command=in_submit)
	b_submit.pack(side=tk.BOTTOM, pady=8)

def out_click():
	window_in = tk.Toplevel(main_window)
	window_in.geometry('600x400')
	window_in.title('借用设备登记')
	exampledate = tk.StringVar()
	exampledate.set("YYYY-mm-dd")
	ecode = tk.Entry(window_in, show = None)#显示成明文形式
	ecode.place(x=300,y=50,anchor='n')
	edepart = tk.Entry(window_in, show = None)#显示成明文形式
	edepart.place(x=300,y=100,anchor='n')
	eoutdate = tk.Entry(window_in, show = None,textvariable=exampledate)#显示成明文形式
	eoutdate.place(x=300,y=150,anchor='n')
	eout_number = tk.Entry(window_in, show = None)#显示成明文形式
	eout_number.place(x=300,y=200,anchor='n')
	eout_person = tk.Entry(window_in, show = None)#显示成明文形式
	eout_person.place(x=300,y=250,anchor='n')
	etaker = tk.Entry(window_in, show = None)#显示成明文形式
	etaker.place(x=300,y=300,anchor='n')
	tk.Label(window_in, text='设备号', font=('', 10)).place(x=200,y=50,anchor="ne")
	tk.Label(window_in, text='使用部门', font=('', 10)).place(x=200,y=100,anchor="ne")
	tk.Label(window_in, text='出库时间', font=('', 10)).place(x=200,y=150,anchor="ne")
	tk.Label(window_in, text='出库数量', font=('', 10)).place(x=200,y=200,anchor="ne")
	tk.Label(window_in, text='经手人', font=('', 10)).place(x=200,y=250,anchor="ne")
	tk.Label(window_in, text='领取人', font=('', 10)).place(x=200,y=300,anchor="ne")
	def out_submit():
		code = ecode.get()
		depart = edepart.get()
		outdate = eoutdate.get()
		out_number = eout_number.get()
		out_person = eout_person.get()
		taker = etaker.get()
		sql = "INSERT INTO d_out(code, department, out_date, out_person, out_number, taker) VALUES(%s,%s,%s,%s,%s,%s);"
		values = (code,depart,outdate,out_person,int(out_number),taker)
		curs.execute(sql,values)
		conn.commit()
		tk.messagebox.showinfo(title='Hi', message="提交完成")
		window_in.destroy()
	b_submit = tk.Button(window_in, text='提交', font=('',10), width=8, height=3, command=out_submit)
	b_submit.pack(side=tk.BOTTOM, pady=8)


def return_click():
	window_in = tk.Toplevel(main_window)
	window_in.geometry('600x300')
	window_in.title('归还设备登记')
	exampledate = tk.StringVar()
	exampledate.set("YYYY-mm-dd")
	ecode = tk.Entry(window_in, show = None)#显示成明文形式
	ecode.place(x=300,y=50,anchor='n')
	ereturndate = tk.Entry(window_in, show = None,textvariable=exampledate)#显示成明文形式
	ereturndate.place(x=300,y=100,anchor='n')
	ereturn_number = tk.Entry(window_in, show = None)#显示成明文形式
	ereturn_number.place(x=300,y=150,anchor='n')
	ereturn_depart = tk.Entry(window_in, show = None)#显示成明文形式
	ereturn_depart.place(x=300,y=200,anchor='n')
	tk.Label(window_in, text='设备号', font=('', 10)).place(x=200,y=50,anchor="ne")
	tk.Label(window_in, text='还库时间', font=('', 10)).place(x=200,y=100,anchor="ne")
	tk.Label(window_in, text='归还数量', font=('', 10)).place(x=200,y=150,anchor="ne")
	tk.Label(window_in, text='归还部门', font=('', 10)).place(x=200,y=200,anchor="ne")
	def return_submit():
		code = ecode.get()
		returndepart = ereturn_depart.get()
		returndate = ereturndate.get()
		return_number = ereturn_number.get()
		sql = "INSERT INTO d_return(code, return_date, return_number, return_department) VALUES(%s,%s,%s,%s);"
		values = (code,returndate,int(return_number),returndepart)
		curs.execute(sql,values)
		conn.commit()
		tk.messagebox.showinfo(title='Hi', message="提交完成")
		window_in.destroy()
	b_submit = tk.Button(window_in, text='提交', font=('',10), width=8, height=3, command=return_submit)
	b_submit.pack(side=tk.BOTTOM, pady=8)


def query_d_click():
	window_in = tk.Toplevel(main_window)
	window_in.geometry('600x300')
	window_in.title('按设备查询出入库记录')


def query_dp_click():
	window_in = tk.Toplevel(main_window)
	window_in.geometry('600x300')
	window_in.title('按部门查询出入库记录')


# 关闭窗口前先断开数据库连接
def on_closing():
	curs.close()
	conn.close()
	main_window.destroy()


fm = tk.Frame(main_window)
fm.pack(side=tk.TOP, pady=10)

b1 = tk.Button(fm, text='当前库存', font=('', 15), width=25, height=4, command=now_d_click)
b1.grid(row=0, column=0, padx=20, pady=20)

b2 = tk.Button(fm, text='采购入库', font=('', 15), width=25, height=4, command=in_click)
b2.grid(row=0, column=1, padx=20, pady=20)

b3 = tk.Button(fm, text='借用设备', font=('', 15), width=25, height=4, command=out_click)
b3.grid(row=1, column=0, padx=20, pady=20)

b4 = tk.Button(fm, text='归还设备', font=('', 15), width=25, height=4, command=return_click)
b4.grid(row=1, column=1, padx=20, pady=20)

b5 = tk.Button(fm, text='按设备查询', font=('', 15), width=25, height=4, command=query_d_click)
b5.grid(row=2, column=0, padx=20, pady=20)

b6 = tk.Button(fm, text='按部门查询', font=('', 15), width=25, height=4, command=query_dp_click)
b6.grid(row=2, column=1, padx=20, pady=20)

info = tk.Label(main_window, text='通信中英1701班，吴警彤 & 胡力夫', font=('microsoft yahei', 15))
info.pack(side=tk.BOTTOM, pady=8)

main_window.protocol('WM_DELETE_WINDOW', on_closing)
main_window.mainloop()
