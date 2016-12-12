import json
import re
from flask import Flask
from flask import url_for, render_template, request, redirect

def write_txt(what, where):
    doc = open(where, 'w', encoding='utf-8')
    doc.write(what)
    doc.close()

def readit(name):
    lexemes = open(name, 'r', encoding='utf-8')
    regexp = 'lex: (.*)\n'
    regexp1 = 'gramm: (.*)\n'
    regexp2 = 'trans_ru: (.*)\n'
    dic = {}
    arr = []
    for line in lexemes:
        if len(arr) == 3:
            dic[arr[0]] = [arr[1], arr[2]]
            arr = []
        else:
            if 'lex' in line:
                res = re.search(regexp, line)
                if res:
                    lex = res.group(1)
                    arr.append(lex)
            if 'gramm' in line:
                res1 = re.search(regexp1, line)
                if res1:
                    gramm = res1.group(1)
                    arr.append(gramm)
            if 'trans_ru' in line:
                res2 = re.search(regexp2, line)
                if res2:
                    trans = res2.group(1)
                    arr.append(trans)
    return dic

def make_dic():
    N = readit('udm_lexemes_N.txt')
    ADJ = readit('udm_lexemes_ADJ.txt')
    IMIT = readit('udm_lexemes_IMIT.txt')
    Np = readit('udm_lexemes_N_persn.txt')
    Nrel = readit('udm_lexemes_NRel.txt')
    PRO = readit('udm_lexemes_PRO.txt')
    UN = readit('udm_lexemes_unchangeable.txt')
    V = readit('udm_lexemes_V.txt')
    dic = N
    dic.update(ADJ)
    dic.update(IMIT)
    dic.update(Np)
    dic.update(Nrel)
    dic.update(PRO)
    dic.update(UN)
    dic.update(V)
    return dic

def write_words(what, where):
    doc = open(where, 'w', encoding='utf-8')
    for word in what:
        doc.write(word + '\t' + str(what[word]) + '\n')
    doc.close()

def json1(dic):
    json_string = json.dumps(dic, ensure_ascii=False)
    write_txt(json_string, 'json1.txt')

def json2(dic):
    dic2 = {}
    for elem in dic:
        arr = []
        arr.append(dic[elem][0])
        arr.append(elem)
        dic2[dic[elem][1]] = arr
        
    dic3 = {}
    for word in dic2:
        if word == "":
            pass
        else:
            res = re.search('[1-9]\.', word)
            if res:
                wordarr = re.split('[1-9]\.', word)
                for elem in wordarr:
                    elem = elem.strip(' ')
                    if elem != "":
                        dic3[elem] = dic2[word]
            else:
                dic3[word] = dic2[word]

    json_string = json.dumps(dic3, ensure_ascii=False)
    write_txt(json_string, 'json2.txt')
    


def main():
    write_words(make_dic(), 'results.txt')
    json1(make_dic())
    json2(make_dic())

    
search_request = ''

app = Flask(__name__)
@app.route('/')
def index():
    if request.args:
        udm_word = request.args['udm_word']

        global search_request                                                                                                         
        search_request = udm_word
        
        return redirect(url_for('results'))
    return render_template('search.html')

@app.route('/results')
def results():
    global search_request
    for elem in make_dic():
        if elem == search_request:
            trans_ru = make_dic()[elem][1]

    try: 
        trans_ru
    except NameError: 
        trans_ru = 'нет перевода'

    return render_template('results.html', trans_ru=trans_ru)

if __name__ == '__main__':
    main()
    app.run(debug='true')
            
    
    
