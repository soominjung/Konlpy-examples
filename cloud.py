#! /usr/bin/python3.7
# -*- coding: utf-8 -*-

from collections import Counter
import urllib
import random
import webbrowser

from konlpy.tag import Mecab
import pytagcloud # requires Korean font support
import sys
import webbrowser
import csv
import re
import wikipediaapi
import argparse

r = lambda: random.randint(0,255)
color = lambda: (r(), r(), r())

parser = argparse.ArgumentParser(description='Draw a wordcloud of a Wikipedia page.')
parser.add_argument('keyword', type=str, help='Keyword to search on Wikipedia')
arg=parser.parse_args()

def read_wiki(keyword):
    wiki = wikipediaapi.Wikipedia(language='ko', extract_format=wikipediaapi.ExtractFormat.WIKI)
    
    wiki_page = wiki.page(keyword)
    if not wiki_page.exists():
        print("The page for the keyword doesn't exist")

    return wiki_page.text

def get_tags(wiki_text, ntags=50, multiplier=5):
    len_text = len(wiki_text)
    if len_text>5000:
        multiplier=1
    elif len_text>3000:
        multiplier=3
    elif len_text>1000:
        multiplier=5
    else:
        multiplier=10
    
    nouns = Mecab().nouns(wiki_text)
    count = Counter(nouns)
    return [{ 'color': color(), 'tag': n, 'size': c*multiplier }\
                for n, c in count.most_common(ntags)]

def draw_cloud(tags, filename, fontname='Noto Sans CJK', size=(800, 600)):
    pytagcloud.create_tag_image(tags, filename, fontname=fontname, size=size)
    webbrowser.open(filename)

wiki_text = read_wiki(arg.keyword)
if len(wiki_text)>0:
    tags = get_tags(wiki_text)
    print(tags)
    draw_cloud(tags, 'wordcloud.png')
