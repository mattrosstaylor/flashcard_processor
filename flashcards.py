# -*- coding: utf-8 -*-
#!/bin/python

from unicode_csv import UnicodeReader 
import operator
import re
import random

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
				if u'\u2026' in r[0]: # search for elipsis
					text_tokens = r[0].split(u'\u2026')
					pinyin_tokens = r[1].split(u'\u2026')

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

entries = read_entries_from_csv("export.txt")

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

def increment_word(words, character):
	if character in words:
		words[character] += 1
	else:
		words[character] = 1

def output_word_list(words):
	it = sorted(words.items(), key=operator.itemgetter(1))
	for sc in it:
		print sc[0] +" " +str(words[sc[0]])

unknown = dict()
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
			increment_word(unknown, j)
	else:
		passed.append(s)

known = dict()

for s in passed:
	example = s.text

	for w in words:
		if w.text in example:
			example = example.replace(w.text,"")
			increment_word(known, w.text)
			s.related.add(w)
			w.related.add(s)
"""
	contains = "\t"
	for x in s.related:
		contains = contains +" " +x.text

	print s.text + " " +str(len(s.related))
"""

covering = []

while passed:
	passed.sort(key=lambda x: x.count, reverse=False)
	#passed.sort(key=lambda x: len(x.related))

	#top = passed.pop()
	top = passed[random.randint(0,len(passed)-1)]
	passed.remove(top)

	for s in passed:
		for chars in top.related:
			if chars in s.related:
				s.related.remove(chars)

		if not len(s.related):
			passed.remove(s)

	covering.append(top)


print len(covering)

#for w in words:
#	if not w.text in known:
#		print w.text

#output_word_list(known)

print "// Learning".encode('utf-8')
for s in covering:
	if s.text and s.pinyin and s.english:
		print (s.text +"\t" +s.pinyin +"\t" +s.english).encode('utf-8')
