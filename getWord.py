import pandas as pd
import pickle

file_name = "tokens.pkl"
with open('./tokens.pkl','rb') as f:
    tokens = pickle.load(f)
import nltk

text = nltk.Text(tokens, name = 'NMSC')
print(len(tokens))
print(len(set(text.tokens)))
a = (text.vocab().most_common(1200))
print(a)