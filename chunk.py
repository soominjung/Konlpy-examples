#! /usr/bin/python3.7
# -*- coding: utf-8 -*-

from konlpy.tag import Okt
import nltk
import argparse

parser = argparse.ArgumentParser(description='Chunk an input sentence')
parser.add_argument('sentence', type=str, help='Sentence to chunk')
arg=parser.parse_args()

# POS tag a sentence
words = Okt().pos(arg.sentence)

# Define a chunk grammar, or chunking rules, then chunk
grammar = """
NP: {<N.*>*<Suffix>?}   # Noun phrase
VP: {<V.*>*}            # Verb phrase
AP: {<A.*>*}            # Adjective phrase
"""
regexparser = nltk.RegexpParser(grammar)
chunks = regexparser.parse(words)
print("# Print whole tree")
print(chunks.pprint())

print("\n# Print noun phrases only")
for subtree in chunks.subtrees():
    if subtree.label()=='NP':
        print(' '.join((e[0] for e in list(subtree))))
        print(subtree.pprint())

# Display the chunk tree
chunks.draw()
