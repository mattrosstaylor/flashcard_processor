# -*- coding: utf-8 -*-
#!/bin/python

from entry import *
from bad_chars import *
import operator
import re

def increment_word(words, character):
	if character in words:
		words[character] += 1
	else:
		words[character] = 1

def output_word_list(words):
	it = sorted(words.items(), key=operator.itemgetter(1))
	for sc in it:
		print sc[0].text +" " +str(words[sc[0]])

class Flashcard_Context:

	def __init__(self, raw_sentences, words):
		
		self.words = words
		(self.sentences, self.failed_sentence_map, self.unknown_word_counts) =  self.process_raw_sentence_list(raw_sentences)
		
		# eliminate duplicates in sentence list (crudely)
		self.sentences = list(set(self.sentences))

		self.related_words = dict()
		self.related_sentences = dict()

		for s in self.sentences:
			self.related_words[s] = set()
		for w in self.words:
			self.related_sentences[w] = set()

		self.known_word_counts = dict()
		
		for s in self.sentences:
			example = s.text

			for w in self.words:
				if w.text in example:
					example = example.replace(w.text,"")
					increment_word(self.known_word_counts, w)
				
					self.related_words[s].add(w)
					self.related_sentences[w].add(s)
	
	
	def process_raw_sentence_list(self, sentences):
		
		self.words.sort(key=operator.attrgetter('count'), reverse=True)

		# examples without unknown characters
		passed = []

		# unknown words mapped to number of entries with that word
		unknown_word_counts = dict()

		# failed sentences mapped to string of remaining characters
		failed = dict()

		for s in sentences:
			example = s.text
			example_printable = s.text

			# remove bad characters
			for bc in bad_chars:
				example = example.replace(bc,"")
				example_printable = example_printable.replace(bc,"*")

			# remove known words
			for w in self.words:
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

				failed[s] = example_printable

				junk = example_printable.split(' ')
				for j in junk:
					increment_word(unknown_word_counts, j)
			else:
				passed.append(s)

		return (passed, failed, unknown_word_counts)

	def get_related_words(self, sentence):
		return self.related_words[sentence]

	def get_related_sentences(self, word):
		return self.related_sentences[word]