# -*- coding: utf-8 -*-

#!/bin/python

import csv, codecs, cStringIO
import operator
import re

class UTF8Recoder:

    def __init__(self, f, encoding):
        self.reader = codecs.getreader(encoding)(f)

    def __iter__(self):
        return self

    def next(self):
        return self.reader.next().encode("utf-8")

class UnicodeReader:

    def __init__(self, f, dialect=csv.excel, encoding="utf-8", **kwds):
        f = UTF8Recoder(f, encoding)
        self.reader = csv.reader(f, dialect=dialect, delimiter='\t', **kwds)

    def next(self):
        row = self.reader.next()
        return [unicode(s, "utf-8") for s in row]

    def __iter__(self):
        return self

class UnicodeWriter:

    def __init__(self, f, dialect=csv.excel, encoding="utf-8", **kwds):
        self.queue = cStringIO.StringIO()
        self.writer = csv.writer(self.queue, dialect=dialect, **kwds)
        self.stream = f
        self.encoder = codecs.getincrementalencoder(encoding)()

    def writerow(self, row):
        self.writer.writerow([s.encode("utf-8") for s in row])
        data = self.queue.getvalue()
        data = data.decode("utf-8")
        data = self.encoder.encode(data)
        self.stream.write(data)
        self.queue.truncate(0)

    def writerows(self, rows):
        for row in rows:
            self.writerow(row)

class Entry:
    def __init__(self, cat, sc, py, en=None):
        self.sc = sc
        self.py = py
        self.en = en
        self.cat = cat

        self.pypy = py.encode("ascii", "replace").replace("?", "v")
        self.count = len(sc)
    
    def __str__(self):
        return self.pypy

    def __unicode__(self):
    	return self.sc +" " +self.py +" " +self.cat

lines = UnicodeReader(open("flashcard.txt"))

entries = []
category_name = None

for r in lines:
	if r:
		if "// " in r[0]:
			category_name = r[0]
		else:
			if u'\u2026' in r[0]: # search for elipsis
				sctokens = r[0].split(u'\u2026')
				pytokens = r[1].split(u'\u2026')

				for i, t in enumerate(sctokens):
					if t:
						entry = Entry(category_name, t, pytokens[i])
						entries.append(entry)
			else:
				if len(r) == 3:
					entry = Entry(category_name, r[0], r[1], r[2])
					entries.append(entry)
				else:
					entry = Entry(category_name, r[0], r[1])
					entries.append(entry)

words = []
sentences = []

for entry in entries:
	if "Example" in entry.cat:
		sentences.append(entry)
	elif not "Learning" in entry.cat:
		words.append(entry)

words.sort(key=operator.attrgetter('count'), reverse=True)

bad_chars = [
	u"、" , 
	u"。" , 
	u"；" ,
	u"—" ,
	u"？" ,
	u"（" ,
	u"）" ,
	u"→" , 
	u"”" , 
	u"“" ,
	u"！" ,
	"(" ,
	")" ,
	"/" ,
	"," , 
	"!" ,
	";" ,
	":" ,
	"?" ,
	" "
]

unknown = dict()
passed = []

for s in sentences:
	sc = s.sc
	sc_printable = s.sc

	for w in words:
		if w.sc in sc:
			sc = sc.replace(w.sc,"")
			sc_printable = sc_printable.replace(w.sc,u' '*w.count)
			# print unicode(w)

	for bc in bad_chars:
		sc = sc.replace(bc,"")
		sc_printable = sc_printable.replace(bc,"*")
	
	sc_printable = re.sub(r'(.)\1+', r'\1', sc_printable) 
	sc_printable = sc_printable.replace("*", " ").strip()


	if sc:
		#print unicode(s.sc)
		#print sc_printable
		#print ""

		junk = sc_printable.split(' ')
		for j in junk:
			if j in unknown:
				unknown[j] += 1
			else:
				unknown[j] = 1
	else:
		passed.append(s)	

#it = sorted(unknown.items(), key=operator.itemgetter(1))

#for sc in it:
#	print sc[0] +" " +str(unknown[sc[0]])

print "// Learning".encode('utf-8')
for s in passed:
	if s.sc and s.py and s.en:
		print (s.sc +"\t" +s.py +"\t" +s.en).encode('utf-8')
