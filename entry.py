# -*- coding: utf-8 -*-
#!/bin/python

class Entry:
	def __init__(self, text, pinyin, english=None):
		self.text = text
		self.pinyin = pinyin
		self.english = english
		self.count = len(text)
    
	def __repr__(self):
		return self.text.encode("utf-8")

	def __unicode__(self):
		return self.sc +" " +self.py # this has an error

	def __eq__(self, other):
		return self.text == other.text

	def __hash__(self):
		return hash(self.text)
