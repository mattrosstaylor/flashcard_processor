# -*- coding: utf-8 -*-
#!/bin/python

from entry import *
from flashcard_context import *
import operator

class Sentence_Filter:

	def __init__(self, context, minimum_desired_count = 5, maximum_card_count = 30000):

		self.context = context
		self.minimum_desired_count = minimum_desired_count
		self.maximum_card_count = maximum_card_count
		
		# null initialise added_word_count dictionary
		self.added_word_counts = dict()

		for w in context.known_word_counts:
			self.added_word_counts[w] = 0

		self.output = []
		self.added_sentences = set()

	def add_sentence(self, sentence):
		# add this sentence - register as "added"
		self.output.append(sentence)
		self.added_sentences.add(sentence)

		# update added_word_counts to include new sentence
		for ww in self.context.get_related_words(sentence):
			increment_word(self.added_word_counts, ww)


	def add_existing_sentences(self, existing_sentences):
		# processing exiting sentences first
		for sentence in existing_sentences:
			if sentence in self.context.sentences:
				self.add_sentence(sentence)


	def filter_sentences(self):

		looping = True

		while looping:
			if len(self.output) >= self.maximum_card_count or len(self.output) >= len(self.context.sentences):
				looping = False
				break

			# sort already added words incrementally by prevalence
			it = sorted(self.added_word_counts.items(), key=operator.itemgetter(1)) #shuffle this list somehow...

			# find the most common word's prevalence (i.e. the last word on this list)
			maximum_prevalence = self.added_word_counts[it[len(it)-1][0]]

			for w in it:
				smallest_word = w[0]

				# if you have already added all the examples from this word - continue
				if self.context.known_word_counts[smallest_word] == self.added_word_counts[smallest_word]:
					continue

				# if the least common word has reached the desired count - we're done!
				if not self.added_word_counts[smallest_word] < self.minimum_desired_count:
					looping = False
					break

				# find the best unadded sentence for this word - see below
				best_sentence = None
				best_sentence_score = 0

				# loop through sentences containing this word
				for sentence in self.context.get_related_sentences(smallest_word):
					if sentence in self.added_sentences:
						continue
						
					# base score is number of unique words
					sentence_score = len(self.context.get_related_words(sentence)) 
					
					# score bonus points for how rare each word is
					for ww in self.context.get_related_words(sentence):
						sentence_score += maximum_prevalence - self.added_word_counts[ww]

					# check if best sentence for this word
					if sentence_score > best_sentence_score:
						best_sentence = sentence
						best_sentence_score = sentence_score

				# if no suitable sentences found - go to next smallest word
				if not sentence:
					continue

				self.add_sentence(best_sentence)
				
				break # back to main loop
