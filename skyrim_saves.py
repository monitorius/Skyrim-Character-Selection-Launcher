__author__ = 'monitorius'
__all__ = ['SkyrimSaves', 'get_char_name']

import os
import shutil


class SAVE_FILE:
	NAME_SIZE_POS = 25 # size of name is in 26th byte
	NAME_POS = 27 # name starts from 28th byte

def get_char_name(save_file_path):
	"""Retrieve a character name from Skyrim savefile. """
	f = open(save_file_path, 'rb')
	b = f.read(300)
	name_size = b[SAVE_FILE.NAME_SIZE_POS]
	name = b[SAVE_FILE.NAME_POS : SAVE_FILE.NAME_POS + name_size]
	return name.decode('UTF8') # name.decode('CP866')


class SkyrimSaves:
	"""
		Scan Skyrim "Saves" directory to get characters and their files.

		Use "make_char_last_saved" method to make a copy of that char last savefile,
		so "Continue" menu item in Skyrim will load selected character.
	"""
	def __init__(self, saves_path, copy_token='___COPIED_SAVEGAME_'):
		self.saves_path = saves_path
		self.copy_token = copy_token
		self.files_by_char_name = {}

	def refresh(self):
		"""Iterate through all saved games to create a dict {charName : {'fileName':fileName, 'timestamp':timestamp}, ...} """
		self.files_by_char_name = {}
		files = [file_name for file_name in os.listdir(self.saves_path) if file_name.endswith('.ess')]
		for file_name in files:
			if not file_name.startswith(self.copy_token): # ignore files created by us
				save_file_path = self.saves_path + file_name
				char_name = get_char_name(save_file_path)
				files = self.files_by_char_name.setdefault(char_name, [])
				timestamp = os.path.getmtime(save_file_path)
				files.append( {'fileName':file_name,'timestamp':timestamp} )
		# sort by time, descending
		for char_name, files in self.files_by_char_name.items():
			print(char_name)
			self.files_by_char_name[char_name] = sorted(files, key=lambda f:f['timestamp'], reverse=True)

	def make_char_last_saved(self, char_name):
		""" Make a copy of last savefile of char - Skyrim will treat that copy as last saved game """
		file_name = self.files_by_char_name[char_name][0]['fileName'] # get latest file for that char
		from_file = self.saves_path + file_name
		to_file = self.saves_path + self.copy_token+char_name+'.ess'
		shutil.copyfile(from_file, to_file)

	def get_chars_names(self):
		return self.files_by_char_name.keys()