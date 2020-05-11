#! /usr/bin/python3.7
# -*- coding: utf-8 -*-

from time import time

from konlpy import tag
from konlpy.corpus import kolaw
from konlpy.utils import pprint
import csv


def tagging(tagger, text):
    r = []
    try:
        r = getattr(tag, tagger)().pos(text)
    except Exception as e:
        print("Uhoh,", e)
    return r


def measure_time(taggers, mult=6):
    doc = kolaw.open('constitution.txt').read()*6
    data = [['n'] + taggers]
    for i in range(mult):
        doclen = 10**i
        times = [time()]
        diffs = [doclen]
        for tagger in taggers:
            r = tagging(tagger, doc[:doclen])
            times.append(time())
            diffs.append(times[-1] - times[-2])
            print('%s\t%s\t%s' % (tagger[:5], doclen, diffs[-1]))
            pprint(r[:5])
        data.append(diffs)
        print()
    return data


def measure_accuracy(taggers, text):
    print('\n%s' % text)
    result = []
    for tagger in taggers:
        print(tagger)
        r = tagging(tagger, text)
        pprint(r)
        result.append([tagger] + list(map(lambda s: ' / '.join(s), r)))
    return result


def plot(result):

    from matplotlib import pylab as pl
    import scipy as sp

    if not result:
        result = sp.loadtxt('morph.csv', delimiter=',', skiprows=1).T

    x, y = result[0], result[1:]

    for i in y:
        pl.plot(x, i)

    pl.xlabel('Number of characters')
    pl.ylabel('Time (sec)')
    pl.xscale('log')
    pl.grid(True)
    pl.savefig("images/time.png")
    pl.show()


if __name__=='__main__':

    PLOT = False
    MULT = 6

    examples = [u'나오늘학교에서밥먹었어',  # 띄어쓰기
            u'나는 밥을 먹는다', u'허리가 가는 사람', # 중의성 해소
            u'인정 ㄹㅇ 일반고 진짜 ㅠㅠ 정시는 개뿔 내신도 제대로 못가르침 ㅜㅜㅋㅋㅋ'] # 속어

    taggers = [t for t in dir(tag) if t[0].isupper()]

    # Time
    data = measure_time(taggers, mult=MULT)
    with open('morph.csv', 'w') as f:
        wr = csv.writer(f)
        wr.writerows(data)

    # Accuracy
    for i, example in enumerate(examples):
        result = measure_accuracy(taggers, example)
        with open('morph-%s.csv' % i, 'w') as f:
            wr = csv.writer(f)
            wr.writerows(result)

    # Plot
    if PLOT:
        plot(list(result))
