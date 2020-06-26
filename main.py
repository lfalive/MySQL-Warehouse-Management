from tkinter import ttk
import tkinter as tk
from func import query

main_window = tk.Tk()

main_window.title('仓库数据管理系统')
main_window.geometry('1280x720')
main_window.resizable(width=False, height=False)
title = tk.Label(main_window, text='Welcome！欢迎来到仓库管理系统', bg='gray', font=('KaiTi',40,'bold'), width=40, height=3)
title.place(x=640,y=0,anchor='n')

tips = tk.Label(main_window, text='点击按钮进行出入库登记和查询', font=('KaiTi',20), width=20, height=3)
tips.place(x=640,y=500,anchor='n')

def query_click():
	window_in = tk.Toplevel(main_window)
	window_in.geometry('800x400')
	window_in.title('现有库存')
	results = query()

	# 创建表格
	tree_date = ttk.Treeview(window_in)

	# 定义列
	tree_date['columns'] = ['code','now_number','total_number']
	tree_date.pack()

	# 设置列宽度
	tree_date.column('code',width=100)
	tree_date.column('now_number',width=200)
	tree_date.column('total_number',width=200)

	# 添加列名
	tree_date.heading('code',text='设备号')
	tree_date.heading('now_number',text='现有库存')
	tree_date.heading('total_number',text='总数')

	# 给表格中添加数据
	i = 1
	for record in results:
		tree_date.insert('',i,text=str(i),values=(record[0],str(record[1]),str(record[2])))
		i += 1
	# 第一个参数为第一层级

def in_click():
	window_in = tk.Toplevel(main_window)
	window_in.geometry('600x300')
	window_in.title('入库登记')

def out_click():
	window_in = tk.Toplevel(main_window)
	window_in.geometry('600x300')
	window_in.title('出库登记')

def return_click():
	window_in = tk.Toplevel(main_window)
	window_in.geometry('600x300')
	window_in.title('归还登记')



b1 = tk.Button(main_window, text='查看库存',font=('',15), width=30, height=5, command=query_click)
# b1.pack(side=tk.LEFT, expand=False, padx=30)
b1.place(x=10,y=250,anchor='nw')

b2= tk.Button(main_window, text='采购入库',font=('',15), width=30, height=5, command=in_click)
b2.place(x=320,y=250,anchor='nw')

b3= tk.Button(main_window, text='借用设备',font=('',15), width=30, height=5, command=out_click)
b3.place(x=630,y=250,anchor='nw')

b4= tk.Button(main_window, text='归还设备',font=('',15), width=30, height=5, command=return_click)
b4.place(x=940,y=250,anchor='nw')

main_window.mainloop()
