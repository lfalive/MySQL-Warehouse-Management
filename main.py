import tkinter as tk
from tkinter import ttk

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
	curs.execute("select * from device;")
	results = curs.fetchall()

	# 创建表格
	tree_date = ttk.Treeview(window_in)

	# 定义列
	tree_date['columns'] = ['code', 'now_number', 'total_number']
	tree_date.pack()

	# 设置列宽度
	tree_date.column('code', width=100)
	tree_date.column('now_number', width=200)
	tree_date.column('total_number', width=200)

	# 添加列名
	tree_date.heading('code', text='设备号')
	tree_date.heading('now_number', text='现有库存')
	tree_date.heading('total_number', text='总数')

	# 给表格中添加数据
	i = 1
	for record in results:
		tree_date.insert('', i, text=str(i), values=(record[0], str(record[1]), str(record[2])))
		i += 1


# 第一个参数为第一层级

def in_click():
	window_in = tk.Toplevel(main_window)
	window_in.geometry('600x300')
	window_in.title('采购入库登记')


def out_click():
	window_in = tk.Toplevel(main_window)
	window_in.geometry('600x300')
	window_in.title('借用设备登记')


def return_click():
	window_in = tk.Toplevel(main_window)
	window_in.geometry('600x300')
	window_in.title('归还设备登记')


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
