#! /usr/bin/python3.7
# -*- coding: utf-8 -*-

from time import time

from konlpy.tag import Okt
from konlpy.utils import pprint
from nltk import collocations

import csv
import re

measures = collocations.BigramAssocMeasures()

def read_data(csvfile):
    with open(csvfile, 'r') as f:
        reader = csv.reader(f, delimiter='\t')
        sentences = []
        for line in reader:
            line[1] = re.sub('[^(가-힣ㄱ-ㅎㅏ-ㅣa-zA-Z0-9 )]', '', line[1])
            sentences.append(line[1])
    return sentences

def tag_words(sentences):
    tagged_set = []
    for sentence in sentences:
        tagged_words = Okt().pos(sentence)
        tagged_set.extend(tagged_words)
    return tagged_set
    
def collocations_tagged_words(tagged_set):
    print('\nCollocations among tagged words:')
    finder = collocations.BigramCollocationFinder.from_words(tagged_set)
    pprint(finder.nbest(measures.pmi, 10)) # top 5 n-grams with highest PMI
    
def collocations_words(tagged_set):
    print('\nCollocations among words:')
    words = [w for w, t in tagged_set]
    ignored_words = [u'안녕']
    finder = collocations.BigramCollocationFinder.from_words(words)
    finder.apply_word_filter(lambda w: len(w) < 2 or w in ignored_words)
    finder.apply_freq_filter(3) # only bigrams that appear 3+ times
    pprint(finder.nbest(measures.pmi, 10))
    
def collocations_tags(tagged_set):
    print('\nCollocations among tags:')
    tags = [t for w, t in tagged_set]
    finder = collocations.BigramCollocationFinder.from_words(tags)
    pprint(finder.nbest(measures.pmi, 5))

if __name__=='__main__':
    sentences = read_data('data/ratings_test.txt')
    
    tagged_set = tag_words(sentences)
    collocations_tagged_words(tagged_set)
    collocations_words(tagged_set)
    collocations_tags(tagged_set)
    
    
    
