# -*- coding: utf-8 -*-
from konlpy.tag import Mecab
import pickle
from gensim.models import Word2Vec
import csv
import codecs

kw = codecs.open('test_result.csv', 'w', encoding='euc_kr')
kr = open('realtest.csv','r',encoding='euc_kr')
rdr = csv.reader(kr)
wr = csv.writer(kw)
i = 0;
for line in rdr:
    print(str(i),"/100\n")
    i+=1
    story = line[0]
    with open('./answer.pkl','rb') as f:
        answer = pickle.load(f) # answer = [Question,Answer,List of token]

    model = Word2Vec.load("lawme.model")

    score = []

    mecab = Mecab()

    tokens = []
    for i in range(0,len(answer)):
        score.append(0)

    temp = mecab.pos(story,flatten=True)
    for k in temp:
        if k[1][0] != 'S' and k[1][0] != 'E' and k[1][0] != 'J':
            tokens.append(k[0])

    lst_a = []
    for i in answer:
        lst_a.append(i[2])

    for i in range(0,len(lst_a)):
        try:
            score[i] = model.n_similarity(tokens,lst_a[i])
        except(KeyError,ZeroDivisionError):
            pass
    wr.writerow([story,answer[score.index(max(score))][0]])

