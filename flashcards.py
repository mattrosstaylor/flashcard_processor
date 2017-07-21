# -*- coding: utf-8 -*-
#!/bin/python

from unicode_csv import UnicodeReader 
from export_loader import *
import operator
import random

minimum_desired_count = 1000
maximum_card_count = 30000

words = load_word_file("vocab.txt")
extras = load_word_file("vocab_extras.txt")

words = words + extras

(sentences, unknown) = load_export_file("spoonfed_sample.txt", words)

#for w in unknown:
#	print w

# eliminate duplicates in sentence list (crudely)
sentences = list(set(sentences))

known_word_counts = dict()

for s in sentences:
	example = s.text

	for w in words:
		if w.text in example:
			example = example.replace(w.text,"")
			increment_word(known_word_counts, w)
		
			s.related.add(w)
			w.related.add(s)

# Output list of words with no matching sentences
#for w in words:
#	if not w.text in known_word_counts:
#		print w.text

# null initialise added_word_count dictionary
added_word_counts = dict()

for w in known_word_counts:
	added_word_counts[w] = 0

covering = []
added_sentences = set()

looping = True

while looping:
	if len(covering) >= maximum_card_count or len(covering) >= len(sentences):
		looping = False
		break

	# sort already added words incrementally by prevalence
	it = sorted(added_word_counts.items(), key=operator.itemgetter(1)) #shuffle this list somehow...

	# find the most common word's prevalence (i.e. the last word on this list)
	maximum_prevalence = added_word_counts[it[len(it)-1][0]]

	for w in it:
		smallest_word = w[0]

		# if you have already added all the examples from this word - continue
		if known_word_counts[smallest_word] == added_word_counts[smallest_word]:
			continue

		# if the least common word has reached the desired count - we're done!
		if not added_word_counts[smallest_word] < minimum_desired_count:
			looping = False
			break

		# find the best unadded sentence for this word - see below
		best_sentence = None
		best_sentence_score = 0

		# loop through sentences containing this word
		for sentence in smallest_word.related:
			if sentence in added_sentences:
				continue
				
			# base score is number of unique words
			sentence_score = len(sentence.related) 
			
			# score bonus points for how rare each word is
			for ww in sentence.related:
				sentence_score += maximum_prevalence - added_word_counts[ww]

			# check if best sentence for this word
			if sentence_score > best_sentence_score:
				best_sentence = sentence
				best_sentence_score = sentence_score

		# if no suitable sentences found - go to next smallest word
		if not sentence:
			continue

		# add this sentence - register as "added"
		covering.append(best_sentence)
		added_sentences.add(best_sentence)

		# update added_word_counts to include new sentence
		for ww in best_sentence.related:
			increment_word(added_word_counts, ww)
		
		break # back to main loop

# output sentence list
print ("// Learning " +str(len(covering))).encode('utf-8')
for s in covering:
	if s.text and s.pinyin and s.english:
		#print (s.text +"\t" +s.pinyin +"\t" +s.english).encode('utf-8')
		#print (s.english +"\t" +s.pinyin +"\t" +s.text).encode('utf-8')
		print (s.english +"\t" "learning").encode('utf-8')

#output_word_list(known_word_counts)

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
