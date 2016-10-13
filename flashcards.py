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
		print sc[0].text +" " +str(words[sc[0]])

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

passed = list(set(passed))

known_word_counts = dict()
original_known_word_counts = dict()

for s in passed:
	example = s.text

	for w in words:
		if w.text in example:
			example = example.replace(w.text,"")
			increment_word(known_word_counts, w)
			increment_word(original_known_word_counts, w)
			s.related.add(w)
			w.related.add(s)

covering = []
added_word_counts = dict()
added_sentences = set()
looping = True

for w in known_word_counts:
	added_word_counts[w] = 0

while len(covering) < 1000:

	it = sorted(added_word_counts.items(), key=operator.itemgetter(1))
	
	looping = False

	for w in it:
		smallest_word = w[0]

		if added_word_counts[smallest_word] < 100:
			
			sentence = None
			float cost = 999999

			for s in smallest_word.related:
				if s not in added_sentences:
					
					float total = 0
					for ww in s.related:
						total += float(added_word_counts[ww]*added_word_counts[ww])
					
					total = total / float(len(s.related))

					if total < cost:
						sentence = s
						cost = total

			if not sentence:
				continue

			covering.append(sentence)
			added_sentences.add(sentence)

			for ww in sentence.related:
				increment_word(added_word_counts, ww)
			
			break
		else:
			continue

#for w in words:
#	if not w.text in known_word_counts:
#		print w.text

#output_word_list(known_word_counts)

print ("// Learning " +str(len(covering))).encode('utf-8')
for s in covering:
	if s.text and s.pinyin and s.english:
		print (s.text +"\t" +s.pinyin +"\t" +s.english).encode('utf-8')
		#print (s.text).encode('utf-8')

#print len(covering)

#known_word_counts = dict()

#for s in covering:
#	example = s.text
#
#	for w in words:
#		if w.text in example:
#			example = example.replace(w.text,"")
#			increment_word(known_word_counts, w.text)
#			s.related.add(w)
#			w.related.add(s)

it = sorted(original_known_word_counts.items(), key=operator.itemgetter(1))
for sc in it:
	oc = original_known_word_counts[sc[0]]
	ao = added_word_counts[sc[0]]
	print (sc[0].text +" " +str(ao) +"/" +str(oc)).encode('utf-8')
