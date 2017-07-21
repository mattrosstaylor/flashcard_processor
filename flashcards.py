# -*- coding: utf-8 -*-
#!/bin/python

from export_loader import *
from entry import *
from flashcard_context import *
from sentence_filter import *

words = load_word_file("vocab.txt") + load_word_file("vocab_extras.txt")

(sentences, unknown) = load_export_file("spoonfed_sample.txt", words)

#for w in unknown:
#	print w

# eliminate duplicates in sentence list (crudely)
sentences = list(set(sentences))

context = Flashcard_Context(sentences, words)

# Output list of words with no matching sentences
#for w in words:
#	if not w.text in known_word_counts:
#		print w.text


# FILTER SENTENCE
sf = Sentence_Filter()
filtered_sentences = sf.get_filtered_sentences(context)

# output sentence list
print ("// Learning " +str(len(filtered_sentences))).encode('utf-8')
for s in filtered_sentences:
	if s.text and s.pinyin and s.english:
		#print (s.text +"\t" +s.pinyin +"\t" +s.english).encode('utf-8')
		#print (s.english +"\t" +s.pinyin +"\t" +s.text).encode('utf-8')
		print (s.english +"\t" "learning").encode('utf-8')

#output_word_list(known_word_counts)

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

#it = sorted(known_word_counts.items(), key=operator.itemgetter(1))
#for sc in it:
#	oc = known_word_counts[sc[0]]
#	ao = added_word_counts[sc[0]]
#	print (sc[0].text +" " +str(ao) +"/" +str(oc)).encode('utf-8')
