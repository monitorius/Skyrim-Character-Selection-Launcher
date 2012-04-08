__author__ = 'monitorius'

import os
from tkinter import *

import config
from skyrim_saves import SkyrimSaves


root = Tk()
listbox = Listbox(root, relief=RAISED, bd=1)
listbox.pack(expand=YES, fill=BOTH)
btn_refresh = Button(root, text='Refresh')
btn_refresh.pack()
saves_work = SkyrimSaves(config.saves_path, config.copy_token)


def on_listbox_double_clicked(event):
	listbox = event.widget
	current_index = listbox.curselection()
	char_name = listbox.get(current_index)
	saves_work.make_char_last_saved(char_name)
	os.system(config.skyrim_launcher_path)	# launch Skyrim


def refresh_list():
	listbox.delete(0, END)
	root.title('Refreshing...')
	saves_work.refresh()
	for char_name in saves_work.get_chars_names():
		listbox.insert(END, char_name)
	root.title('Done')


def on_btn_refresh_clicked(event):
	refresh_list()


listbox.bind('<Double-1>', on_listbox_double_clicked)
btn_refresh.bind('<Button-1>', on_btn_refresh_clicked)

refresh_list()
root.mainloop()
