# -*- coding: utf-8 -*-
#!/bin/python

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

	def __init__(self, sentences, words):
		self.sentences = sentences
		self.words = words

		self.related_entries = dict()

		for s in self.sentences:
			self.related_entries[s] = set()
		for w in self.words:
			self.related_entries[w] = set()

		self.known_word_counts = dict()
		
		for s in self.sentences:
			example = s.text

			for w in self.words:
				if w.text in example:
					example = example.replace(w.text,"")
					increment_word(self.known_word_counts, w)
				
					
					self.related_entries[s].add(w)
					self.related_entries[w].add(s)

	def get_related_entries(self, entry):
		return self.related_entries[entry]