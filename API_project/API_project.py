import requests
import json
import re
import datetime
import time
from datetime import date
from datetime import timedelta
import matplotlib.pyplot as plt
from matplotlib import style
style.use('ggplot') 

from collections import Counter

def vk_api(method, **kwargs):
    api_request = 'https://api.vk.com/method/'+ method + '?'
    api_request += '&'.join(['{}={}'.format(key, kwargs[key]) for key in kwargs])
    return json.loads(requests.get(api_request).text)

def write_txt(what, where):
    doc = open(where, 'w', encoding='utf-8')
    doc.write(what)
    doc.close()

def get_age(birthday, postday):
    age = postday.year - birthday.year
    if postday.month < birthday.month:
        age -= 1
    elif postday.month == birthday.month and postday.day < birthday.day:
        age -= 1
    return age

def word_count(text):
    text1 = text.replace('.', ' ')
    text1 = text1.replace('!', ' ')
    text1 = text1.replace(',', ' ')
    text1 = text1.replace('?', ' ')
    text1 = text1.replace('+', '')
    text1 = text1.replace(')', ' ')
    text1 = text1.replace('-', '')
    text1 = text1.strip(' ')
    text1 = text1.replace('(', ' ')
    text1 = text1.replace('"', ' ')
    myre = re.compile(u'['u'\U0001F300-\U0001F64F'u'\U0001F680-\U0001F6FF'u'\u2600-\u26FF\u2700-\u27BF]+', re.UNICODE)
    text1 = myre.sub('', text1)
    for smth in range(0,20):
        text1 = text1.replace('  ', ' ')
    textarr = text1.split(' ')
    return len(textarr)
    

def get_posts(group_name, item_count): #даём группу и количество постов, получаем массив
    group_info = vk_api('groups.getById', group_id=group_name, v='5.63')
    group_id = group_info['response'][0]['id']   
    posts = []
    if item_count < 100:
        try:
            result = vk_api('wall.get', owner_id=-group_id, v='5.63', count=item_count)            
        except:
            result = vk_api('wall.get', owner_id=-group_id, v='5.63')
        posts += result["response"]["items"]
    else:
        try:
            result = vk_api('wall.get', owner_id=-group_id, v='5.63', count=100)
        except:
            result = vk_api('wall.get', owner_id=-group_id, v='5.63')
        posts += result["response"]["items"]
        

    while len(posts) < item_count:
        lastlen = len(posts)
        try:
            result = vk_api('wall.get', owner_id=-group_id, v='5.63', count=100, offset=len(posts))
        except:
            result = vk_api('wall.get', owner_id=-group_id, v='5.63', offset=len(posts))
        posts += result['response']["items"]
        if lastlen == len(posts):
            break
    return posts

def addcomments(posts): #даём массив постов и к каждому добавляются комментарии
    wholeposts = []
    for post in posts:
        print('работа идёт, хоть и медленно')
        owner = post["from_id"]
        thepost = post["id"]
        if post['comments']['count'] <= 100:
            postcomments = vk_api('wall.getComments', post_id=thepost, owner_id=owner, count=post['comments']['count'])       
            post.update(postcomments)
        else:
            count = 0
            comments = [0]
            while count < post['comments']['count'] - 100:
                postcomments = vk_api('wall.getComments', post_id=thepost, owner_id=owner, offset=count, count=100)
                comments[0] += 100
                for element in postcomments['response']:
                    if type(element)==dict:
                        comments.append(element)
                count += 100
            postcomments = vk_api('wall.getComments', post_id=thepost, owner_id=owner, offset=count, count=post['comments']['count']-count)
            comments[0] += post['comments']['count'] - count
            for element in postcomments['response']:
                    if type(element)==dict:
                        comments.append(element)
            post['response']=comments
            
        wholeposts.append(post)                     
    return wholeposts

def counting(posts): # функция выдёт список с длинами постов и комментариев, а параллельно записывает в файлы все тексты
    n = 1
    lens = []
    for post in posts:
        file = open('posts/post' + str(n) + '.txt', 'w', encoding='utf-8')
        comentlens = []
        postlens = []
        posttext = post['text']
        if posttext == '':
            textlen = 0
        else:
            textlen = word_count(posttext)
        file.write(posttext + '\n\n-----------\nКОММЕНТАРИИ:\n-----------')
        for element in post['response']:
            if type(element)==dict:
                comenttext = element['text']
                if comenttext != '':
                    comentlens.append(word_count(comenttext))
                else:
                    comentlens.append(0)
                file.write('\n\n' + comenttext)
        postlens = [textlen, comentlens] #(сейчас посты без комментариев не учитываются)
        lens.append(postlens)
        file.close()
        n += 1
    return lens

def sortby1(arr):
    return arr[0]

def lensdic(lens):
    lensdic = {}
    for element in lens:
        if element[0] not in lensdic:
            lensdic[element[0]] = element[1]
        else:
            lensdic[element[0]].extend(element[1])
    sortedarr = []
    for elem in lensdic:
        element = [elem, lensdic[elem]]
        sortedarr.append(element)
    sortedarr.sort(key=sortby1)
    return sortedarr

def average(arr):
    s = 0
    for elem in arr:
        s += elem
    try:
        return s / len(arr)
    except:
        return 0

def pc_plot(lens): #по массиву из counting() построит график
    X = []
    Y = []
    for elem in lens:
        if len(elem[1]) != 0: #НАДО УБРАТЬ ЭТО УСЛОВИЕ ЕСЛИ МЫ СЧИТАЕМ, ЧТО У ПОСТОВ БЕЗ КОММЕНТАРИЕВ СРЕДНЯЯ ДЛИНА КОММЕНТОВ 0.
            X.append(elem[0])
            Y.append(average(elem[1]))

    plt.plot(X,Y)
    plt.ylabel('средняя длина комментария')
    plt.xlabel('длина поста (в словах)')
    plt.show()
    return 0


def cityname(cityid):
    cityinfo = vk_api('database.getCitiesById', city_ids=cityid)
    cityname = cityinfo['response'][0]['name']
    return cityname
    
def user_api(uid, timearr):
    user = vk_api('users.get', user_ids=uid, fields='bdate, city')
    try:
        date = str(user['response'][0]['bdate']).split('.')
        if len(date)==3:
            birthtime = datetime.datetime(int(date[2]), int(date[1]), int(date[0]))
            posttime = datetime.datetime(int(timearr[2]), int(timearr[1]), int(timearr[0]))       
            uage = get_age(birthtime, posttime)
        else:
            uage = ''
    except:
        uage = ''
    try:
        city = user['response'][0]['city']
        cname = cityname(city)
    except:
        cname = ''   
    cityage = [cname, uage]
    return cityage


def userinfo(wholeposts, lens):
    n = 0
    citiesp = {}
    citiesc = {}
    agesp = {}
    agesc = {}

    nn=0
    for element in wholeposts:
        print('тише едешь – дальше будешь')
        print(str(nn) + ' постов из ' + str(len(wholeposts)) + ' обработано')
        nn+=1
        if not element['from_id']<0:
            uid = element['from_id']
        else:
            try: 
                uid = element['signer_id']
            except:
                uid = None
        if uid != None:
            timestr = time.strftime("%d.%m.%Y ", time.localtime(element['date']))
            timearr = timestr.split('.')
            ucap = user_api(uid, timearr)
            
            if ucap[0]!= '':
                if ucap[0] not in citiesp.keys():
                    citiesp[ucap[0]] = []
                    citiesp[ucap[0]].append(lens[n][0])
                   
                else:
                    citiesp[ucap[0]].append(lens[n][0])
            
            if ucap[1] != '':
                if ucap[1] not in agesp.keys():
                    agesp[ucap[1]] = []
                    agesp[ucap[1]].append(lens[n][0])
                   
                else:
                    agesp[ucap[1]].append(lens[n][0])

        k = 0
        for comment in element['response']:
            print('ещё один коммент обработан')
            if type(comment)==dict:
                if not comment['from_id'] < 0:
                    timestr = time.strftime("%d.%m.%Y ", time.localtime(comment['date']))
                    timearr = timestr.split('.')                    
                    ucac = user_api(comment['from_id'], timearr)
                    
                    if ucac[1] != '':
                        if ucac[1] not in agesc.keys():
                            agesc[ucac[1]] = []
                            agesc[ucac[1]].append(lens[n][1][k])
                        else:
                            agesc[ucac[1]].append(lens[n][1][k])
                            
                    if ucac[0] != '':
                        if ucac[0] not in citiesc.keys():
                            citiesc[ucac[0]] = []
                            citiesc[ucac[0]].append(lens[n][1][k])
                        else:
                            citiesc[ucac[0]].append(lens[n][1][k])
                k += 1
                       
        n += 1

    X1 = []
    Y1 = []
    X2 = []
    Y2 = []
    
    for elm in agesp:
        X1.append(elm)
        Y1.append(average(agesp[elm]))
    for eleme in agesc:
        X2.append(eleme)
        Y2.append(average(agesc[eleme]))

    plt.scatter(X1, Y1, c='r', label='длина поста')
    plt.scatter(X2, Y2, c='g', label='длина комментария')

    plt.xlabel('возраст автора')
    plt.ylabel('количество слов')
    plt.legend()
    plt.show()

    cities = [citiesp, citiesc]
    return cities

def citiesplot(cities):
    citiesc = []
    citiesp = []
    for eleme in cities[1]:
        city = []
        city.append(eleme)
        city.append(average(cities[1][eleme]))
        citiesc.append(city)

    for elem in cities[0]:
        city2 = []
        city2.append(elem)
        city2.append(average(cities[0][elem]))
        citiesp.append(city2)
        
    citydic = {}

    n = -1
    for element in citiesp:
        n += 1
        citydic[n] = element[0]
        element[0] = n
        
    for el in citiesc:
        if el[0] not in citydic.values():
            n += 1
            citydic[n] = el[0]
            el[0] = n
        else:
            for key in citydic:
                if citydic[key]==el[0]:
                    el[0] = key
    
           
    plt.scatter([a[0] for a in citiesp], [i[1] for i in citiesp], c='r', label='длина поста')
    plt.scatter([a[0] for a in citiesc], [i[1] for i in citiesc], c='b', label='длина комментария')
    plt.xticks(range(len(citydic)), [citydic[n] for n in citydic], rotation='vertical')   
    plt.legend()
    plt.show()

def main():
    posts = addcomments(get_posts('baneks', 300))
    pc_plot(lensdic(counting(posts)))
    a = userinfo(posts, counting(posts))
    citiesplot(a)
   
if __name__ == '__main__':
              main()
    
