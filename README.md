Konlpy-examples
==============
Example codes for Konlpy package

All codes are modified from konlpy examples

Original code: https://github.com/konlpy

test/test.py
-------
Test code for Konlpy taggers.

Modiffied to run in Python 3


*Okt and Twitter on results(morph*.csv) are same but duplicated due to name change(Twitter->Okt).
```
python3 test.py
```

chunk.py
------
Chunk an input sentece and draw a tree.
```
python3 chunk.py setence
```

cloud.py
---
Draw a wordcloud of a Wikipedia page.
```
python3 cloud.py keyword
```

collocation.py
---
Find collocations among tagged words, words and tags from NSMC test data.
```
python3 collocation.py
```

data/ratings_test.txt
-----
From Naver sentiment movie corpus v1.0

https://github.com/e9t/nsmc
