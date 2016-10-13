# -*- coding: utf-8 -*-
#!/bin/python

from unicode_csv import UnicodeReader 
from export_loader import *
import operator
import random

minimum_desired_count = 3
maximum_card_count = 10000
(words, sentences, unknown) = load_export_file("export.txt")

sentences = list(set(sentences))
random.shuffle(sentences)

known_word_counts = dict()

for s in sentences:
	example = s.text

	for w in words:
		if w.text in example:
			example = example.replace(w.text,"")
			increment_word(known_word_counts, w)
		
			s.related.add(w)
			w.related.add(s)

covering = []
added_word_counts = dict()
added_sentences = set()

for w in known_word_counts:
	added_word_counts[w] = 0

looping = True

while looping:
	if not len(covering) < maximum_card_count:
		looping = False
		break

	it = sorted(added_word_counts.items(), key=operator.itemgetter(1))

	maximum_prevalence = added_word_counts[it[len(it)-1][0]]

	for w in it:
		smallest_word = w[0]

		if known_word_counts[smallest_word] == added_word_counts[smallest_word]:
			continue

		if not added_word_counts[smallest_word] < minimum_desired_count:
			looping = False
			break

		
		sentence = None
		cost = 0

		for s in smallest_word.related:
			if s not in added_sentences:
				
				total = 0
				for ww in s.related:
					total += 1 + maximum_prevalence - added_word_counts[ww]
				
				if total > cost:
					sentence = s
					cost = total

		if not sentence:
			continue

		covering.append(sentence)
		added_sentences.add(sentence)

		for ww in sentence.related:
			increment_word(added_word_counts, ww)
		
		break

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

#it = sorted(known_word_counts.items(), key=operator.itemgetter(1))
#for sc in it:
#	oc = known_word_counts[sc[0]]
#	ao = added_word_counts[sc[0]]
#	print (sc[0].text +" " +str(ao) +"/" +str(oc)).encode('utf-8')
