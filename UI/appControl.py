import time
import os
import subprocess
from pynput.keyboard import Key, Controller




class WindowOpt:
	def __init__(self):
		self.keyboard = Controller()

	def openWindow(self):
		self.maximizeWindow()
	
	def closeWindow(self):
		self.keyboard.press(Key.alt_l)
		self.keyboard.press(Key.f4)
		self.keyboard.release(Key.f4)
		self.keyboard.release(Key.alt_l)
	# TODO: Optional functions if need include
	# def minimizeWindow(self):
	# 	for i in range(2):
	# 		self.keyboard.press(Key.cmd)
	# 		self.keyboard.press(Key.down)
	# 		self.keyboard.release(Key.down)
	# 		self.keyboard.release(Key.cmd)
	# 		time.sleep(0.05)
	
	# def maximizeWindow(self):
	# 	self.keyboard.press(Key.cmd)
	# 	self.keyboard.press(Key.up)
	# 	self.keyboard.release(Key.up)
	# 	self.keyboard.release(Key.cmd)

	# def moveWindow(self, operation):
	# 	self.keyboard.press(Key.cmd)
	#
	# 	if "left" in operation:
	# 		self.keyboard.press(Key.left)
	# 		self.keyboard.release(Key.left)
	# 	elif "right" in operation:
	# 		self.keyboard.press(Key.right)
	# 		self.keyboard.release(Key.right)
	# 	elif "down" in operation:
	# 		self.keyboard.press(Key.down)
	# 		self.keyboard.release(Key.down)
	# 	elif "up" in operation:
	# 		self.keyboard.press(Key.up)
	# 		self.keyboard.release(Key.up)
	# 	self.keyboard.release(Key.cmd)

	# def switchWindow(self):
	# 	self.keyboard.press(Key.alt_l)
	# 	self.keyboard.press(Key.tab)
	# 	self.keyboard.release(Key.tab)
	# 	self.keyboard.release(Key.alt_l)


def isContain(text, lst):
	for word in lst:
		if word in text:
			return True
	return False

def Win_Opt(operation):
	w = WindowOpt()
	if isContain(operation, ['open']):
		w.openWindow()
	elif isContain(operation, ['close']):
		w.closeWindow()
	# elif isContain(operation, ['mini']):
	# 	w.minimizeWindow()
	# elif isContain(operation, ['maxi']):
	# 	w.maximizeWindow()
	# elif isContain(operation, ['move', 'slide']):
	# 	w.moveWindow(operation)
	# elif isContain(operation, ['switch','which']):
	# 	w.switchWindow()
	return


from difflib import get_close_matches
import json
from random import choice
import webbrowser

data = json.load(open('extrafiles/websites.json', encoding='utf-8'))

def open_website(query):
	query = query.replace('open','')
	if query in data:
		response = data[query]
	else:
		query = get_close_matches(query, data.keys(), n=2, cutoff=0.5)
		if len(query)==0: return "None"
		response = choice(data[query[0]])
	webbrowser.open(response)