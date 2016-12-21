from flask import Flask
from flask import render_template, request, url_for, redirect
import os
import re

def write_txt(what, where):
    doc = open(where, 'w', encoding='utf-8')
    doc.write(what)
    doc.close()

def mysteming(from_where, to_where):
    command = './mystem -nd ' + from_where + ' ' + to_where
    os.system(command)

def first_table(where_sql):
    file = open('lemmes.txt', 'r', encoding='utf-8')
    wordsarr = []
    for line in file:
        line = line.lower()
        line = line.strip('}\n')
        word = line.split('{')
        wordsarr.append(tuple(word))
       
    wordsset = set(wordsarr)
    n = 0
    words = {}
    for wordpair in wordsset:
        words[wordpair[0]] = [n, wordpair[1]]
        n += 1
        
    filesql = open(where_sql, 'w', encoding='utf-8')
    for element in words:
        string = 'INSERT INTO analyses (id, wordform, lemma) VALUES ("' + str(list(words[element])[0]) + '", "' + element + '", "' + list(words[element])[1]  +'")\n'
        filesql.write(string)
    filesql.write('\n\n')
    filesql.close()

    return words

def second_table1():
    text = open('text.txt', 'r', encoding='utf-8')
    text0 = text.read()
    text.close()
    text1 = re.sub('( +\n*)+', ' ', text0)
    textarr = re.split(' |\n', text1)
    regex = '(\W*)?(\w+(?:\W\w+)*)(\W*)?'
    
    n = 0
    tokens = []
    for element in textarr:
        res = re.search(regex, element)
        if res.group(1) == None:
            punc1 = ''
        else:
            punc1 = res.group(1)

        if res.group(3) == None:
            punc2 = ''
        else:
            punc2 = res.group(3)

        arr = [n, punc1, res.group(2), punc2]
        n += 1
        tokens.append(arr)


    return tokens

def second_table2(tokens, lemmes, where_sql):
    file = open(where_sql, 'a', encoding='utf-8')
    for element in tokens:
        wordform = element[2].lower()
        lex_id = lemmes[wordform][0]
        sqlstring = 'INSERT INTO tokens (id, analyses_id, token, punctuation_before, punctuation_after) VALUES ("' + str(element[0]) + ', ' + str(lex_id) + ', ' + element[2] + ', ' + element[1] + ', ' + element[3] + '")\n'
        file.write(sqlstring)
    file.close()



def main(filename):
    mysteming('text.txt', 'lemmes.txt')
    val = first_table(filename)
    second_table2(second_table1(), val, filename)

app = Flask(__name__)
@app.route('/')
def index():
    if request.args:
        try:
            name = request.args['sql_name']
            if name != '' and name != ' ':
                filename = name + '.txt'
            else:
                filename = 'sql.txt'
        except:
            filename = 'sql.txt'

        text = request.args['text']
        res = re.search('\w', text)
        if res:
            file = open('text.txt', 'w', encoding='utf-8')
            file.write(text)
            file.close()
        else:
            pass
        main(filename)
        return redirect(url_for('end'))
    return render_template ('home.html')

@app.route('/end')
def end():
    return render_template('end.html', url=url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
