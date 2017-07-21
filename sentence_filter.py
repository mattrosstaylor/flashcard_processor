# -*- coding: utf-8 -*-
#!/bin/python

from entry import *
from flashcard_context import *
import operator

minimum_desired_count = 1
maximum_card_count = 30000

class Sentence_Filter:

	def get_filtered_sentences(self, context):
		
		# null initialise added_word_count dictionary
		added_word_counts = dict()

		for w in context.known_word_counts:
			added_word_counts[w] = 0

		output = []
		added_sentences = set()

		looping = True

		while looping:
			if len(output) >= maximum_card_count or len(output) >= len(context.sentences):
				looping = False
				break

			# sort already added words incrementally by prevalence
			it = sorted(added_word_counts.items(), key=operator.itemgetter(1)) #shuffle this list somehow...

			# find the most common word's prevalence (i.e. the last word on this list)
			maximum_prevalence = added_word_counts[it[len(it)-1][0]]

			for w in it:
				smallest_word = w[0]

				# if you have already added all the examples from this word - continue
				if context.known_word_counts[smallest_word] == added_word_counts[smallest_word]:
					continue

				# if the least common word has reached the desired count - we're done!
				if not added_word_counts[smallest_word] < minimum_desired_count:
					looping = False
					break

				# find the best unadded sentence for this word - see below
				best_sentence = None
				best_sentence_score = 0

				# loop through sentences containing this word
				for sentence in context.get_related_entries(smallest_word):
					if sentence in added_sentences:
						continue
						
					# base score is number of unique words
					sentence_score = len(context.get_related_entries(sentence)) 
					
					# score bonus points for how rare each word is
					for ww in context.get_related_entries(sentence):
						sentence_score += maximum_prevalence - added_word_counts[ww]

					# check if best sentence for this word
					if sentence_score > best_sentence_score:
						best_sentence = sentence
						best_sentence_score = sentence_score

				# if no suitable sentences found - go to next smallest word
				if not sentence:
					continue

				# add this sentence - register as "added"
				output.append(best_sentence)
				added_sentences.add(best_sentence)

				# update added_word_counts to include new sentence
				for ww in context.get_related_entries(best_sentence):
					increment_word(added_word_counts, ww)
				
				break # back to main loop
		return output
