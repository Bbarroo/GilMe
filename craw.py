import requests
import codecs
import csv

f = codecs.open('data.csv', 'w', encoding='euc_kr')

wr = csv.writer(f)

for k in range(10000,24150):
    url = "http://youthlabor.co.kr/alba/sub/consult_view.php"
    data = {"c_no":k}
    check = False;

    a = requests.post(url,data).text.split('<')
    print(a)

    if 'strong>한국공인노무사회' in a:
        c_1 = a.index('span class="icon question">Q :')
        if a[c_1+1] == '/span>\n            ':
            c_1 +=1
        c_1 += 1
        c_2 = a.index('strong>한국공인노무사회')
        c_3 = a.index('!-- 목록/글쓰기 버튼 -->\n        ')

        question = a[c_1]
        answer = a[c_2+5]

        question = question.replace('p>','')
        question = question.replace('/span>\n            ','')
        question = question.replace('\n            ','')

        answer = answer.replace('/p>br','')
        answer = answer.replace('/>','')
        answer = answer.replace('p>','')
        answer = answer.replace('br','')
        answer = answer.replace('\r','')
        answer = answer.replace('\n','')
        answer = answer.replace('&nbsp;','')
        answer = answer.replace("p class='contents'>", '')

        try:
            if answer != "":
                wr.writerow([question,answer])
                check = True
        except UnicodeEncodeError:
            pass

    if check:
        print(k,"is finished. it is written correctly.")
    else:
        print(k,"is finished. it is non-written.")
f.close()
print('Finish!')



