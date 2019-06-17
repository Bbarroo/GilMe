from flask import Flask, request, jsonify
import sys
import requests
import json
import ast
from konlpy.tag import Mecab
import pickle
from gensim.models import Word2Vec
import math
with open('./answer.pkl', 'rb') as f:
        answer = pickle.load(f) # answer = [Question, Answer, List of token]
lst_a = []
for i in answer:
    lst_a.append(i[2])
    
model = Word2Vec.load("lawme.model")
app = Flask(__name__)
mecab = Mecab()
@app.route('/order', methods=['POST'])
def order():

    storys = request.get_json()
    story = storys["action"]["detailParams"]["알바"]["origin"]

    score = []

    tokens = []
    for i in range(0, len(answer)):
        score.append(0)

    temp = mecab.pos(story, flatten=True)
    
    for k in temp:
        if k[1][0] != 'S' and k[1][0] != 'E' and k[1][0] != 'J':
            tokens.append(k[0])
    tokens = set(tokens)
    print(tokens)        
    for i in range(0, len(lst_a)):
        try:
            score[i] = model.n_similarity(tokens,lst_a[i])
        except(KeyError,ZeroDivisionError):
            pass
    res_print = "질문: " + answer[score.index(max(score))][0] +"\n\n답변: " +answer[score.index(max(score))][1] + "\n\n질문이 도움이 되셨나요?"

    res = {"version": "2.0",
           "template": {
               "outputs": [
                   {
                   "simpleText": {
                       "text": res_print
                   }
                }
            ]
        }
    }

    print(res)

    return jsonify(res)

if __name__ == '__main__':
    app.run(host ='0.0.0.0', threaded = True)