from pymystem3 import Mystem
import pymorphy2
from pymorphy2 import MorphAnalyzer
import random
import re

textik = input('Сюда вводить фразу для бота:\t')

def write_txt(what, where):
    doc = open(where, 'a', encoding='utf-8')
    doc.write(what + '\n')
    doc.close()

def lems_spread(la):
    ld = {}
    for element in la:
        if element != '':
            el = element.split(' ')
            if el[1] in ld:
                ld[el[1]].append(el[0])
            else:
                ld[el[1]] = []
                ld[el[1]].append(el[0])

    return ld

def mysteming(text):
    morph = MorphAnalyzer()
    m = Mystem()
    lemmas = m.lemmatize(text)
    ana = m.analyze(text)
    lemmas = open('lemmas.txt', 'r', encoding='utf-8')
    lemmasstr = lemmas.read()
    lemmas.close()
    lemmasarr = lemmasstr.split('\n')
    
    
    ldic = lems_spread(lemmasarr)

    reply = []
    
    for word in ana:
        if 'analysis' in word and word['analysis'] != []:
            gr = word['analysis'][0]['gr']
            pos = gr.split('=')[0].split(',')[0]
            gr2 = ''
            while gr2 != gr:
                newword = random.choice(ldic[pos])
                morph.parse(newword)
                prog = morph.parse(newword)[0]
                forms = prog.lexeme
                for eleme in forms:
                    res = re.search("word='(.*?)'", str(eleme))
                    wana = m.analyze(str(res.group(1)))                   
                    gr2 = wana[0]['analysis'][0]['gr']
                    if gr2 == gr:
                        newword = str(res.group(1))
                        break
            reply.append(newword)
            lex = word['analysis'][0]['lex']
    return ' '.join(reply)

def main():
    rl = mysteming(textik)
    print(rl)

if __name__ == '__main__':
    main()
