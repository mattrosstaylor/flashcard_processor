# -*- coding: utf-8 -*-
#!/bin/python

from unicode_csv import *
from entry import *
from flashcard_context import *

def read_entries_from_csv(path, text_index=0, pinyin_index=1, english_index=2):

	lines = UnicodeReader(open(path))

	entries = []

	for r in lines:
		if r:
			
			
			if len(r) >= 3:
				entry = Entry(r[text_index], r[pinyin_index], r[english_index])
				entries.append(entry)
			else:
				entry = Entry(r[text_index], r[pinyin_index])
				entries.append(entry)

	return entries

def load_word_file(path):
	return read_entries_from_csv(path)

def load_export_file(path, text_index=0, pinyin_index=1, english_index=2):
	return read_entries_from_csv(path, text_index, pinyin_index, english_index)