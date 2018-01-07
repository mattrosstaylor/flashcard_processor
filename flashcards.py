# -*- coding: utf-8 -*-
#!/bin/python

from export_loader import *
from entry import *
from flashcard_context import *
from sentence_filter import *
import codecs

import operator	

def process_audio_sentences(words):
	sentences = load_export_file("SpoonFedChinese.txt", 2, 1, 0)

	context = Flashcard_Context(sentences, words)

	# FILTER SENTENCE
	sf = Sentence_Filter(context)
	sf.filter_sentences()

	#print ("// Learning " +str(len(sf.output))).encode('utf-8')
	
	for s in sf.output:
		print (s.english +"\t" "learning").encode('utf-8')

def process_text_sentences(words):
	sentences = load_export_file("examples.txt")
	context = Flashcard_Context(sentences, words)

	with codecs.open("results_unknown_counts.txt", "w", "utf-8") as f:
		# output unknown words
		it = sorted(context.unknown_word_counts.items(), key=operator.itemgetter(1))

		for w in it:
			f.write(w[0] +"\t" +str(w[1]) +"\n")

	with codecs.open("results_failed.txt", "w", "utf-8") as f:
		it = sorted(context.failed_sentence_map.items(), key=operator.itemgetter(1))
		for sc in it:
			s = sc[0]
			oc = context.failed_sentence_map[s]
			if s.text and s.pinyin and s.english and oc:
				f.write(s.text +"\t" +s.pinyin +"\t" +s.english +"\t" +oc +"\n")

	# FILTER SENTENCE
	sf = Sentence_Filter(context, 3, 999999)
	existing_sentences = load_export_file("examples_already_existing.txt")
	sf.add_existing_sentences(existing_sentences)
	sf.filter_sentences()

	#print ("// Learning " +str(len(sf.output))).encode('utf-8')
	
	with codecs.open("results.txt", "w", "utf-8") as f:
		for s in sf.output:
			if s.text and s.pinyin and s.english:
				f.write(s.text +"\t" +s.pinyin +"\t" +s.english +"\n")
	
	with codecs.open("results_counts.txt", "w", "utf-8") as f:
		# words that are missing
		for w in context.words:
			if not w in context.known_word_counts:
				f.write(w.text +" 0\n")

		# Lists the number of cards for each word
		it = sorted(context.known_word_counts.items(), key=operator.itemgetter(1))
		for sc in it:
			oc = context.known_word_counts[sc[0]]
			f.write(sc[0].text +" " +str(oc) +"\n")


# load stuff
words = load_word_file("vocab.txt") + load_word_file("vocab_extras.txt")

#process_audio_sentences(words)
process_text_sentences(words)

#output_sentence_list(context.sentences)
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
