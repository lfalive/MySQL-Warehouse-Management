from tkinter import *

main_window = Tk()

main_window.title('仓库数据管理系统')
main_window.geometry('1280x720')
main_window.resizable(width=False, height=False)


def click():
	window_in = Toplevel(main_window)
	window_in.geometry('300x200')
	window_in.title('输入数据')


b1 = Button(main_window, text='入库', width=20, height=2, command=click)
b1.pack(side=LEFT, expand=False, padx=30)

main_window.mainloop()
