from gensim.models import Word2Vec
import codecs
import csv

model = Word2Vec.load('lawme.model')
print(model.most_similar(positive=["시급"], topn=20))
