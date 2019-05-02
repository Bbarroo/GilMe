from flask import Flask, request, jsonify
import sys
import requests
import json
import ast

app = Flask(__name__)


@app.route('/order', methods=['post'])
def order():

    start = ""
    arrival = ""

    req = request.get_json()
    print(req)

    talk_data = req["action"]["detailParams"]["장소"]["origin"]
    user_data = req["userRequest"]["user"]["id"]

    talk_lst = talk_data.split('/')

    url_kakao = "https://dapi.kakao.com/v2/local/search/keyword.json"
    headers = {'Authorization': 'KakaoAK 76129b4755674eabb8122486664765ab'}
    params = {"query": talk_lst[0]}
    print(talk_lst[0])
    result = requests.get(url_kakao, headers = headers, params = params)


    start_x = result.json()['documents'][0]['x']
    start_y = result.json()['documents'][0]['y']
    start = start_x[0:10] + "," + start_y[0:10] + "," + talk_lst[0]

    params = {"query": talk_lst[1]}

    result = requests.get(url_kakao, headers = headers, params = params)

    arrival_x = result.json()['documents'][0]['x']
    arrival_y = result.json()['documents'][0]['y']
    arrival =  arrival_x[0:10] + "," + arrival_y[0:10] + "," + talk_lst[1]
    
    url = "https://map.naver.com/findroute2/findWalkRoute.nhn"
    print(start,"/",arrival)
    params = {'call':'route2', 'output':'json', 'coord_type':'naver', 'search':'0', 'start':start, 'destination':arrival}
    headers = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86     Safari/537.36","Referer":"https://map.naver.com/"}
    response = requests.get(url, params=params,headers=headers)
    res = response.text
    a = json.loads(res)
 
    res_print = ""
    for i in range(0,len(a['result']['route'][0]['point'])):
        res_print += i
        res_print +=". "
        res_print += a['result']['route'][0]['point'][i]['guide']['name']
        res_print += "\n\n"
    res_out = res_print.replace("<b>","")
    res_print = res_out.replace("</b>","")
        
    

    res = {"version": "2.0",
           "template": {
               "outputs": [{
                   "simpleText": {
                       "text": res_print
                   }
               }]
           }}
    
    return jsonify(res)

if __name__ == '__main__':
    app.run('0.0.0.0', threaded = True)
