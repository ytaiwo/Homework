#!/usr/bin/env python
import sys

import nltk
from nltk.tokenize import word_tokenize
from nltk.tokenize import wordpunct_tokenize
from collections import Counter

cats_file = open("cats_txt.txt", "r")
cats = cats_file.read().replace("\n", " ")
cats_file.close()
#put words in lowercase
lower_words = cats.lower()
#tokenize by words and punctuation
cats_lower = wordpunct_tokenize(lower_words)

#Counter to count the frequency of words
word_counter = Counter(cats_lower)
#order the frequency of words by most common, automatically sorts it by highest frequency at top
print(word_counter.most_common())