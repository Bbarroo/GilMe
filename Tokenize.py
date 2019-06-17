import pandas as pd
import pickle
from konlpy.tag import Mecab

data = pd.read_csv("rdl.csv", encoding ="euc_kr")
df = data[["Question","Answer"]] # df: main file

df.to_pickle("./df_data.pkl")

lst = df.values.tolist()

komoran = Mecab()
tokens = []
db_tokens = []
tokens_labeled = []
for i in lst:
    temp = komoran.pos(i[0],flatten=True)
    temp_tokens = []
    for k in temp:
        if k[1][0] != 'S' and k[1][0] != 'E' and k[1][0] != 'J':
            tokens.append(k[0])
            temp_tokens.append(k[0])
    tokens_labeled.append(temp_tokens)
    db_tokens.append([i[0],i[1],set(temp_tokens)])

from gensim.models import Word2Vec
import logging

logging.basicConfig(
    format='%(asctime)s : %(levelname)s : %(message)s',
    level=logging.INFO)

embedding_model = Word2Vec(tokens_labeled, size=100, window=2, min_count = 5, workers=4, iter=100, sg=1)
embedding_model.save("lawme.model")

with open('tokens.pkl','wb') as f:
    pickle.dump(tokens, f)

with open('answer.pkl','wb') as f:
    pickle.dump(db_tokens, f)