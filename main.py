from tkinter import *
from tkinter import messagebox
from tkinter import ttk

import pymysql

from str import DBUser, DBPw

conn = pymysql.connect(host='localhost', port=3306, user=DBUser, passwd=DBPw, database='warehouse')
curs = conn.cursor()

main_window = Tk()
main_window.title('仓库数据管理系统')
main_window.geometry('850x720')
main_window.resizable(False, False)

Label(main_window, text='欢迎使用仓库管理系统', font=('', 34)).pack(side=TOP, pady=35)


def now_d_click():
	window_in = Toplevel(main_window)
	window_in.geometry('600x400')
	window_in.title('现有库存')
	window_in.resizable(False, False)

	# 查询数据
	curs.execute("SELECT device.code,d_code.name,now_number,total_number "
				 "FROM device,d_code "
				 "WHERE device.code = d_code.code;")
	results = curs.fetchall()

	# 创建表格
	form = ttk.Treeview(window_in, show="headings", columns=('code', 'name', 'now_number', 'total_number'))
	form.pack(side=TOP, pady=10)

	# 设置列宽度
	form.column('code', width=100)
	form.column('name', width=150)
	form.column('now_number', width=100)
	form.column('total_number', width=100)

	# 添加列名
	form.heading('code', text='设备编号')
	form.heading('name', text='设备名称')
	form.heading('now_number', text='现有库存')
	form.heading('total_number', text='总数')

	# 给表格中添加数据
	for i in range(len(results)):
		form.insert('', i + 1, values=list(results[i]))


def insert_click():
	window_in = Toplevel(main_window)
	window_in.geometry('500x350')
	window_in.title('设备登记')
	window_in.resizable(False, False)

	def query_d_code():
		if var_d_name.get().strip() != '' and var_d_code.get().strip() != '':
			sql = "INSERT INTO d_code VALUES (%s,%s);"
			values = (var_d_code.get(), var_d_name.get())
			curs.execute(sql, values)
			conn.commit()

		curs.execute("SELECT * FROM d_code ORDER BY code;")
		results = curs.fetchall()

		# 先清空，再给表格中添加数据
		for item in form.get_children():
			form.delete(item)
		for i in range(len(results)):
			form.insert('', i + 1, values=list(results[i]))

	var_d_code = StringVar()
	var_d_name = StringVar()

	fm_in = Frame(window_in)
	fm_in.pack(side=TOP, padx=50, pady=10)

	Label(fm_in, text='新设备编号:', font=('', 14)).grid(row=0, column=0, pady=5)
	Entry(fm_in, textvariable=var_d_code, font=('', 14)).grid(row=0, column=1, padx=10)
	Label(fm_in, text='新设备名称:', font=('', 14)).grid(row=1, column=0, pady=5)
	Entry(fm_in, textvariable=var_d_name, font=('', 14)).grid(row=1, column=1)
	Button(fm_in, text='添加', font=('', 12), command=query_d_code).grid(row=0, rowspan=2, column=2, pady=5, sticky=N + S)

	# 创建表格
	form = ttk.Treeview(window_in, show="headings", columns=('code', 'name'))
	form.pack(side=TOP, pady=10)

	# 设置列宽度
	form.column('code', width=80)
	form.column('name', width=180)

	# 添加列名
	form.heading('code', text='设备编号')
	form.heading('name', text='设备名称')

	query_d_code()


def in_click():
	window_in = Toplevel(main_window)
	window_in.geometry('600x400')
	window_in.title('采购入库登记')
	window_in.resizable(False, False)

	ecode = StringVar()
	eindate = StringVar()
	eindate.set("YYYY-mm-dd")
	eprovider = StringVar()
	ein_number = StringVar()
	eprice = StringVar()
	ebuyer = StringVar()

	Entry(window_in, textvariable=ecode).place(x=340, y=50, anchor='n')
	Entry(window_in, textvariable=eindate).place(x=340, y=100, anchor='n')
	Entry(window_in, textvariable=eprovider).place(x=340, y=150, anchor='n')
	Entry(window_in, textvariable=ein_number).place(x=340, y=200, anchor='n')
	Entry(window_in, textvariable=eprice).place(x=340, y=250, anchor='n')
	Entry(window_in, textvariable=ebuyer).place(x=340, y=300, anchor='n')

	Label(window_in, text='设备编号', font=('', 10)).place(x=240, y=50, anchor="ne")
	Label(window_in, text='入库时间', font=('', 10)).place(x=240, y=100, anchor="ne")
	Label(window_in, text='供应商', font=('', 10)).place(x=240, y=150, anchor="ne")
	Label(window_in, text='入库数量', font=('', 10)).place(x=240, y=200, anchor="ne")
	Label(window_in, text='价格', font=('', 10)).place(x=240, y=250, anchor="ne")
	Label(window_in, text='采购员', font=('', 10)).place(x=240, y=300, anchor="ne")

	def in_submit():
		sql = ("INSERT INTO d_in(code, in_date, provider, in_number, price, buyer) "
			   "VALUES(%s,%s,%s,%s,%s,%s);")
		values = (ecode.get(), eindate.get(), eprovider.get(), int(ein_number.get()),
				  int(eprice.get()), ebuyer.get())
		curs.execute(sql, values)
		conn.commit()

		messagebox.showinfo(title='Hi', message="提交完成！")
		window_in.destroy()

	b_submit = Button(window_in, text='提交', font=('', 10), width=10, height=2, command=in_submit)
	b_submit.pack(side=BOTTOM, pady=18)


def out_click():
	window_in = Toplevel(main_window)
	window_in.geometry('600x400')
	window_in.title('借用设备登记')
	window_in.resizable(False, False)

	ecode = StringVar()
	edepart = StringVar()
	eoutdate = StringVar()
	eoutdate.set("YYYY-mm-dd")
	eout_number = StringVar()
	eout_person = StringVar()
	etaker = StringVar()

	Entry(window_in, textvariable=ecode).place(x=340, y=50, anchor='n')
	Entry(window_in, textvariable=edepart).place(x=340, y=100, anchor='n')
	Entry(window_in, textvariable=eoutdate).place(x=340, y=150, anchor='n')
	Entry(window_in, textvariable=eout_number).place(x=340, y=200, anchor='n')
	Entry(window_in, textvariable=eout_person).place(x=340, y=250, anchor='n')
	Entry(window_in, textvariable=etaker).place(x=340, y=300, anchor='n')

	Label(window_in, text='设备编号', font=('', 10)).place(x=240, y=50, anchor="ne")
	Label(window_in, text='使用部门', font=('', 10)).place(x=240, y=100, anchor="ne")
	Label(window_in, text='出库时间', font=('', 10)).place(x=240, y=150, anchor="ne")
	Label(window_in, text='出库数量', font=('', 10)).place(x=240, y=200, anchor="ne")
	Label(window_in, text='经手人', font=('', 10)).place(x=240, y=250, anchor="ne")
	Label(window_in, text='领取人', font=('', 10)).place(x=240, y=300, anchor="ne")

	def out_submit():
		try:
			sql = ("INSERT INTO d_out(code, department, out_date, out_person, out_number, taker) "
				   "VALUES(%s,%s,%s,%s,%s,%s);")
			values = (ecode.get(), edepart.get(), eoutdate.get(), eout_person.get(),
					  int(eout_number.get()), etaker.get())
			curs.execute(sql, values)
			conn.commit()

			messagebox.showinfo(title='Hi', message="提交完成！")
			window_in.destroy()
		except Exception as e:
			conn.rollback()
			conn.commit()
			print(e)
			# 判断错误类型
			if str(e).split(',')[0][1:] == "1690":
				messagebox.showinfo(title='Hi', message="提交失败,库存不足！")
			elif str(e).split(',')[0][1:] == "1292":
				messagebox.showinfo(title='Hi', message="提交失败,日期格式错误！")
			elif str(e).split(',')[0][1:] == "1452":
				messagebox.showinfo(title='Hi', message="提交失败,无该设备！")
			else:
				messagebox.showinfo(title='Hi', message="提交失败,检查后重新提交！")
			window_in.destroy()

	b_submit = Button(window_in, text='提交', font=('', 10), width=10, height=2, command=out_submit)
	b_submit.pack(side=BOTTOM, pady=18)


def return_click():
	window_in = Toplevel(main_window)
	window_in.geometry('600x300')
	window_in.title('归还设备登记')
	window_in.resizable(False, False)

	ecode = StringVar()
	ereturndate = StringVar()
	ereturndate.set("YYYY-mm-dd")
	ereturn_number = StringVar()
	ereturn_depart = StringVar()

	Entry(window_in, textvariable=ecode).place(x=340, y=50, anchor='n')
	Entry(window_in, textvariable=ereturndate).place(x=340, y=100, anchor='n')
	Entry(window_in, textvariable=ereturn_number).place(x=340, y=150, anchor='n')
	Entry(window_in, textvariable=ereturn_depart).place(x=340, y=200, anchor='n')

	Label(window_in, text='设备编号', font=('', 10)).place(x=240, y=50, anchor="ne")
	Label(window_in, text='还库时间', font=('', 10)).place(x=240, y=100, anchor="ne")
	Label(window_in, text='归还数量', font=('', 10)).place(x=240, y=150, anchor="ne")
	Label(window_in, text='归还部门', font=('', 10)).place(x=240, y=200, anchor="ne")

	def return_submit():
		sql = ("INSERT INTO d_return(code, return_date, return_number, return_department) "
			   "VALUES(%s,%s,%s,%s);")
		values = (ecode.get(), ereturndate.get(), ereturn_number.get(), ereturn_depart.get())
		curs.execute(sql, values)
		conn.commit()

		messagebox.showinfo(title='Hi', message="提交完成！")
		window_in.destroy()

	b_submit = Button(window_in, text='提交', font=('', 10), width=10, height=2, command=return_submit)
	b_submit.pack(side=BOTTOM, pady=18)


def query_d_click():
	window_in = Toplevel(main_window)
	window_in.geometry('800x400')
	window_in.title('按设备查询出入库记录')
	window_in.resizable(False, False)

	def query_d():
		sql = ("SELECT in_out_return.*,d_code.name "
			   "FROM in_out_return,d_code "
			   "WHERE in_out_return.code=%s AND in_out_return.code=d_code.code "
			   "ORDER BY date;")
		curs.execute(sql, var_code.get())
		results = curs.fetchall()

		# 先清空，再给表格中添加数据
		for item in form.get_children():
			form.delete(item)
		for i in range(len(results)):
			form.insert('', i + 1, values=list(results[i]))

	var_code = StringVar()

	fm_in = Frame(window_in)
	fm_in.pack(side=TOP, padx=50, pady=10)
	Label(fm_in, text='设备编号:', font=('', 14)).pack(side=LEFT)
	Entry(fm_in, textvariable=var_code, font=('', 14)).pack(side=LEFT)
	Button(fm_in, text='查询', font=('', 12), command=query_d).pack(side=LEFT, padx=20)

	# 创建表格
	form = ttk.Treeview(window_in, show="headings",
						columns=('code', 'name', 'type', 'date', 'number', 'department', 'provider'))
	form.pack(side=TOP, pady=10)

	# 设置列宽度
	form.column('code', width=80)
	form.column('name', width=180)
	form.column('type', width=80)
	form.column('date', width=150)
	form.column('number', width=80)
	form.column('department', width=100)
	form.column('provider', width=100)

	# 添加列名
	form.heading('code', text='设备编号')
	form.heading('name', text='设备名称')
	form.heading('type', text='操作类型')
	form.heading('date', text='时间')
	form.heading('number', text='数量')
	form.heading('department', text='部门')
	form.heading('provider', text='供应商')


def query_dp_click():
	window_in = Toplevel(main_window)
	window_in.geometry('800x400')
	window_in.title('按部门查询出入库记录')
	window_in.resizable(False, False)

	def query_dp():
		sql = ("SELECT in_out_return.*,d_code.name "
			   "FROM in_out_return,d_code "
			   "WHERE in_out_return.department=%s AND in_out_return.code=d_code.code "
			   "ORDER BY date;")
		curs.execute(sql, var_depart.get())
		results = curs.fetchall()

		# 先清空，再给表格中添加数据
		for item in form.get_children():
			form.delete(item)
		for i in range(len(results)):
			form.insert('', i + 1, values=list(results[i]))

	var_depart = StringVar()

	fm_in = Frame(window_in)
	fm_in.pack(side=TOP, padx=50, pady=10)
	Label(fm_in, text='部门名称:', font=('', 14)).pack(side=LEFT)
	Entry(fm_in, textvariable=var_depart, font=('', 14)).pack(side=LEFT)
	Button(fm_in, text='查询', font=('', 12), command=query_dp).pack(side=LEFT, padx=20)

	# 创建表格
	form = ttk.Treeview(window_in, show="headings",
						columns=('code', 'name', 'type', 'date', 'number', 'department', 'provider'))
	form.pack(side=TOP, pady=10)

	# 设置列宽度
	form.column('code', width=80)
	form.column('name', width=180)
	form.column('type', width=80)
	form.column('date', width=150)
	form.column('number', width=80)
	form.column('department', width=100)
	form.column('provider', width=100)

	# 添加列名
	form.heading('code', text='设备编号')
	form.heading('name', text='设备名称')
	form.heading('type', text='操作类型')
	form.heading('date', text='时间')
	form.heading('number', text='数量')
	form.heading('department', text='部门')
	form.heading('provider', text='供应商')


def query_op_click():
	window_in = Toplevel(main_window)
	window_in.geometry('800x400')
	window_in.title('按操作类型查询记录出入库记录')
	window_in.resizable(False, False)

	def query_op():
		sql = ("SELECT in_out_return.*,d_code.name "
			   "FROM in_out_return,d_code "
			   "WHERE in_out_return.type=%s AND in_out_return.code=d_code.code "
			   "ORDER BY date;")
		curs.execute(sql, var_op.get())
		results = curs.fetchall()

		# 先清空，再给表格中添加数据
		for item in form.get_children():
			form.delete(item)
		for i in range(len(results)):
			form.insert('', i + 1, values=list(results[i]))

	var_op = StringVar()
	var_op.set('采购入库')

	fm_in = Frame(window_in)
	fm_in.pack(side=TOP, padx=50, pady=10)
	Radiobutton(fm_in, text='采购入库', variable=var_op, value='采购入库', command=query_op).pack(side=LEFT)
	Radiobutton(fm_in, text='借用设备', variable=var_op, value='借用设备', command=query_op).pack(side=LEFT)
	Radiobutton(fm_in, text='归还设备', variable=var_op, value='归还设备', command=query_op).pack(side=LEFT)

	# 创建表格
	form = ttk.Treeview(window_in, show="headings",
						columns=('code', 'name', 'type', 'date', 'number', 'department', 'provider'))
	form.pack(side=TOP, pady=10)

	# 设置列宽度
	form.column('code', width=80)
	form.column('name', width=180)
	form.column('type', width=80)
	form.column('date', width=150)
	form.column('number', width=80)
	form.column('department', width=100)
	form.column('provider', width=100)

	# 添加列名
	form.heading('code', text='设备编号')
	form.heading('name', text='设备名称')
	form.heading('type', text='操作类型')
	form.heading('date', text='时间')
	form.heading('number', text='数量')
	form.heading('department', text='部门')
	form.heading('provider', text='供应商')

	query_op()


# 关闭窗口前先断开数据库连接
def on_closing():
	curs.close()
	conn.close()
	main_window.destroy()


fm = Frame(main_window)
fm.pack(side=TOP)
button_style = {'font': "(\'\',15)", 'width': 25, 'height': 4}

Button(fm, text='当前库存', command=now_d_click, **button_style).grid(row=0, column=0, padx=20, pady=18)
Button(fm, text='设备登记', command=insert_click, **button_style).grid(row=0, column=1, padx=20, pady=18)
Button(fm, text='采购入库', command=in_click, **button_style).grid(row=1, column=0, padx=20, pady=18)
Button(fm, text='借用设备', command=out_click, **button_style).grid(row=1, column=1, padx=20, pady=18)
Button(fm, text='归还设备', command=return_click, **button_style).grid(row=2, column=0, padx=20, pady=18)
Button(fm, text='按设备查询', command=query_d_click, **button_style).grid(row=2, column=1, padx=20, pady=18)
Button(fm, text='按部门查询', command=query_dp_click, **button_style).grid(row=3, column=0, padx=20, pady=18)
Button(fm, text='按操作查询', command=query_op_click, **button_style).grid(row=3, column=1, padx=20, pady=18)

info = Label(main_window, text='通信中英1701班，吴警彤 & 胡力夫', font=('microsoft yahei', 15))
info.pack(side=BOTTOM, pady=8)

main_window.protocol('WM_DELETE_WINDOW', on_closing)
main_window.mainloop()
