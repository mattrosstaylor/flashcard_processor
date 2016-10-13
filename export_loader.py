# -*- coding: utf-8 -*-
#!/bin/python

from unicode_csv import UnicodeReader 
import operator
import re

class Entry:
	def __init__(self, category, text, pinyin, english=None):
		self.text = text
		self.pinyin = pinyin
		self.english = english
		self.category = category
		self.count = len(text)
		self.related = set()
    
	def __repr__(self):
		return self.text.encode("utf-8")

	def __unicode__(self):
		return self.sc +" " +self.py +" " +self.category

def read_entries_from_csv(path):

	lines = UnicodeReader(open(path))

	entries = []
	category_name = None

	for r in lines:
		if r:
			if "// " in r[0]:
				category_name = r[0]
			else:
				if u'…' in r[0]: # search for ellipsis
					text_tokens = r[0].split(u'…')
					pinyin_tokens = r[1].split(u'…')

					for i, t in enumerate(text_tokens):
						if t:
							entry = Entry(category_name, t, pinyin_tokens[i])
							entries.append(entry)
				else:
					if len(r) == 3:
						entry = Entry(category_name, r[0], r[1], r[2])
						entries.append(entry)
					else:
						entry = Entry(category_name, r[0], r[1])
						entries.append(entry)

	return entries

def increment_word(words, character):
	if character in words:
		words[character] += 1
	else:
		words[character] = 1

def output_word_list(words):
	it = sorted(words.items(), key=operator.itemgetter(1))
	for sc in it:
		print sc[0].text +" " +str(words[sc[0]])

def load_export_file(path):
	entries = read_entries_from_csv(path)

	words = []
	sentences = []

	for entry in entries:
		if "Example" in entry.category:
			sentences.append(entry)
		elif not "Learning" in entry.category:
			words.append(entry)

	words.sort(key=operator.attrgetter('count'), reverse=True)

	bad_chars = [
		u"、" , 
		u"。" , 
		u"；" ,
		u"—" ,
		u"？" ,
		u"（" ,
		u"）" ,
		u"→" , 
		u"”" , 
		u"“" ,
		u"！" ,
		"(" ,
		")" ,
		"/" ,
		"," , 
		"!" ,
		";" ,
		":" ,
		"?" ,
		" "
	]

	unknown_word_counts = dict()
	passed = []

	for s in sentences:
		example = s.text
		example_printable = s.text

		for w in words:
			if w.text in example:
				example = example.replace(w.text,"")
				example_printable = example_printable.replace(w.text, u' '*w.count)

		for bc in bad_chars:
			example = example.replace(bc,"")
			example_printable = example_printable.replace(bc,"*")
		
		if example:
			example_printable = re.sub(r'(\*)\1+', r'\1', example_printable) 
			example_printable = example_printable.replace("*", " ").strip()

			junk = example_printable.split(' ')
			for j in junk:
				increment_word(unknown_word_counts, j)
		else:
			passed.append(s)

	return (words, passed, unknown_word_counts)
