import os
import urllib.request
import re

def write_txt(what, where):
    doc = open(where, 'w', encoding='utf-8')
    doc.write(what)
    doc.close()

def get_html(site): # html страницы текстом
    req = urllib.request.Request(site)
    with urllib.request.urlopen(req) as response:
        html = response.read().decode('utf-8')
    write_txt(html, 'first_html.txt')
    return html
    
def make_folds(subroot): #создаёт папки длягодов и месяцов
    n = 2014
    while n < 2017:
        for a in range (12):
            dirpath = 'rassvet/' + subroot + '/' + str(n) + '/' + str(a+1).rjust(2, '0')
            if not os.path.exists(dirpath):
                os.makedirs(dirpath)
        n += 1
        
def del_empty(theroot): #удаляет пустые папки
    for root, dirs, files in os.walk(theroot):
        try:
            os.rmdir(root)
        except:
            pass

    
def get_articles_from_homepage(site):
    info1 = re.findall('((?:<div class="allmode-item">|<div class="allmode-details">).*?)(?:<div class="allmode-item">|<.div><.div><.div>)', get_html(site), re.DOTALL)
    info2 = re.findall('<li class="allmode_item">.*?</li>.', get_html(site), re.DOTALL)
    info = info1 + info2  #info - массив с кусками кода. в каждом куске информация про одну статью

    months = {'Янв': '01', 'Фев': '02', 'Мар': '03', 'Апр': '04', 'Мая': '05', 'Июн': '06','Июл': '07','Авг': '08','Сен': '09','Окт': '10','Ноя': '11','Дек': '12'}
    articles = []
    for elem in info:
        try: # извлекаем и приводим к нужному виду даты
            res = re.search('<span class="allmode-date">(.*)</span>', elem)
            i3 = res.group(1)
            reg = '(...) (\d\d), (\d{4})'
            an = months[i3[0:3]]
            i31 = re.sub(reg, r'\2.xx.\3', i3)
            i32 = i31.replace('xx', an)
            i3 = i32
        except:
            res = re.search('<span class="allmode_date">(.*)</span>', elem)
            i3 = res.group(1)
            an = months[i3[3:6]]
            reg = '(\d\d) ([^ ]*) (-?\d{4})'
            i31 = re.sub(reg, r'\1.xx.\3', i3)
            i32 = i31.replace('xx', an)
            i33 = i32.replace('-0001', '2014')
            i3 = i33
        
        try: # извлекаем названия рубрик
            res = re.search('<span class="allmode_category">(.*)</span>', elem)
            i4 = res.group(1)
        except:
            i4 = 'Новости'

        try: # получаем заголовки и ссылки на статьи
            res = re.search('<h4 class="allmode-title"><a href="/.*/(.*?)-.*">(.*)</a></h4>', elem)
            i2 = res.group(2)
            i5 = res.group(1)
        except:
            res = re.search('<h4 class="allmode_title"><a href="/.*/(.*?)-.*">(.*)</a></h4>', elem)
            i2 = res.group(2)
            i5 = res.group(1)
        i5 = 'http://xn-----6kcgcpd5bzbmfhaqr3fud1bj.xn--p1ai/' + i5
        art = [i2, i3, i4, i5]
        articles.append(art)
    return articles # для каждой статьи массив [Заголовок Дата Рубрика Ссылка]

def art_nums(articles): #из массива с информацией про статьи получаем массив номеров статей и разбираемся
    art_numms = []
    for elem in articles:
        a = elem[3][-3:]
        a = a.strip('/')
        art_numms.append(a)
        
    nums = []
    for n in range (1,240):
        nums.append(str(n))
        
    not_numms = []
    for element in nums:
        if element not in art_numms:
            not_numms.append(element)

    return not_numms

def news_no_date(nums):
    news = []
    for elem in nums:
        site = 'http://xn-----6kcgcpd5bzbmfhaqr3fud1bj.xn--p1ai/' + elem
        try:
            req = urllib.request.Request(site)
            with urllib.request.urlopen(req) as response:
                html = response.read().decode('utf-8')
            news.append(site)
        except:
            pass
    news_info = []
    for element in news:
        a = ['no_title', 'no date', 'Новости', element]
        news_info.append(a)
    return news_info

def get_articles(all_arts):
    for element in all_arts:
        req = urllib.request.Request(element[3])
        with urllib.request.urlopen(req) as response:
            html = response.read().decode('utf-8')
            
                   

def main():
    val = get_articles_from_homepage('http://xn-----6kcgcpd5bzbmfhaqr3fud1bj.xn--p1ai/')
    make_folds('plain')
    make_folds('mystem_plain')
    make_folds('mystem_xml')
    val1 = news_no_date(art_nums(val))
    all_articles = val + val1  #массив информации о всех статьях в формате [Заголовок Дата Рубрика Ссылка] только некоторых заголовков не хватает
    val2 = get_articles(all_articles)

    
#    del_empty('./rassvet')

if __name__ ==  '__main__':
    main()
