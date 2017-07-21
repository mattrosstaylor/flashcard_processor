# -*- coding: utf-8 -*-
#!/bin/python

from unicode_csv import UnicodeReader 
import operator
import re

class Entry:
	def __init__(self, text, pinyin, english=None):
		self.text = text
		self.pinyin = pinyin
		self.english = english
		self.count = len(text)
		self.related = set()
    
	def __repr__(self):
		return self.text.encode("utf-8")

	def __unicode__(self):
		return self.sc +" " +self.py +" " +self.category

	def __eq__(self, other):
		return self.text == other.text

	def __hash__(self):
		return hash(self.text)

def read_entries_from_csv(path):

	lines = UnicodeReader(open(path))

	entries = []

	for r in lines:
		if r:
			if u'…' in r[0]: # search for ellipsis
				text_tokens = r[0].split(u'…')
				pinyin_tokens = r[1].split(u'…')

				for i, t in enumerate(text_tokens):
					if t:
						entry = Entry(t, pinyin_tokens[i])
						entries.append(entry)
			else:
				if len(r) >= 3:
					entry = Entry(r[0], r[1], r[2])
					entries.append(entry)
				else:
					entry = Entry(r[0], r[1])
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

def load_word_file(path):
	return read_entries_from_csv(path)

def load_export_file(path, words):
	entries = read_entries_from_csv(path)

	sentences = []

	for entry in entries:
		sentences.append(Entry(entry.english, entry.pinyin, entry.text))

	bad_chars = [
		u"，" ,
		u"、" , 
		u"。" , 
		u"；" ,
		u"：" ,
		u"—" ,
		u"？" ,
		u"（" ,
		u"）" ,
		u"《",
		u"》" ,
		u"→" , 
		u"”" , 
		u"“" ,
		u"！" ,
		"(" ,
		")" ,
		"<" ,
		">" ,
		"/" ,
		"," , 
		"." ,
		"!" ,
		";" ,
		":" ,
		"'" ,
		"?" ,
		"%" ,
		"&" ,
		" "
	]

	words.sort(key=operator.attrgetter('count'), reverse=True)

	# examples without unknown characters
	passed = []

	# unknown words mapped to number of entries with that word
	unknown_word_counts = dict()

	for s in sentences:
		example = s.text
		example_printable = s.text

		# remove bad characters
		for bc in bad_chars:
			example = example.replace(bc,"")
			example_printable = example_printable.replace(bc,"*")

		# remove known words
		for w in words:
			if w.text in example:
				example = example.replace(w.text,"")
				example_printable = example_printable.replace(w.text, u' '*w.count)

		# minimise whitespace
		example = re.sub(r'\w', '', example)
		example_printable = re.sub(r'\w', '', example_printable)

		# any example with characters remaining has not passed - records unknown chars
		if example:
			example_printable = re.sub(r'(\*)\1+', r'\1', example_printable)
			example_printable = example_printable.replace("*", " ").strip()

			junk = example_printable.split(' ')
			for j in junk:
				increment_word(unknown_word_counts, j)
		else:
			passed.append(s)

	return (passed, unknown_word_counts)
