# -*- coding: utf-8 -*-
#!/bin/python

from export_loader import *
from entry import *
from flashcard_context import *
from sentence_filter import *

import operator

def output_unknown_words(context):
	# output unknown words
	it = sorted(context.unknown_word_counts.items(), key=operator.itemgetter(1))

	for w in it:
		print w[0] +"\t" +str(w[1])


def output_filtered(context, existing_sentences):

	# FILTER SENTENCE
	sf = Sentence_Filter(context)
	sf.add_existing_sentences(existing_sentences)
	sf.filter_sentences()

	output_sentence_list(sf.output)

def output_sentence_list(sentences):

	# output sentence list
	print ("// Learning " +str(len(sentences))).encode('utf-8')
	for s in sentences:
		if s.text and s.pinyin and s.english:
			print (s.text +"\t" +s.pinyin +"\t" +s.english).encode('utf-8')
			#print (s.english +"\t" +s.pinyin +"\t" +s.text).encode('utf-8')
			#print (s.english +"\t" "learning").encode('utf-8')


# load stuff
words = load_word_file("vocab.txt") + load_word_file("vocab_extras.txt")
#sentences = load_export_file("SpoonFedChinese.txt", 2, 1, 0)

sentences = load_export_file("examples.txt")
existing_sentences = load_export_file("examples_already_existing.txt")

context = Flashcard_Context(sentences, words)

#output_sentence_list(context.sentences)

output_filtered(context, existing_sentences)

#output_unknown_words(context)

#known_word_counts = dict()

#for s in filtered_sentences:
#	example = s.text
#
#	for w in words:
#		if w.text in example:
#			example = example.replace(w.text,"")
#			increment_word(known_word_counts, w.text)
#			s.related.add(w)
#			w.related.add(s)

it = sorted(context.known_word_counts.items(), key=operator.itemgetter(1))
for sc in it:
	oc = context.known_word_counts[sc[0]]
	print (sc[0].text +" " +str(oc)).encode('utf-8')
