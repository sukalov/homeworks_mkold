import os
import urllib.request
import re

def info_from_part1():
    all_arts = []
    os.chdir('.')
    doc = open('result_of_part_1.txt', 'r', encoding='utf-8')
    for line in doc:
        art = line.split(';;')
        all_arts.append(art)
    return all_arts
  
'''

#ЗАКИДЫВАЕТ ХТМЛИ СТАТЕЙ В ЕКЗЕМ

def get_articles_htmls():
    all_arts = info_from_part1()
    try:
        os.makedirs('./rassvet/exem')
    except:
        os.chdir('./rassvet/exem')
    n = 1
    for elem in all_arts:
        req = urllib.request.Request(elem[3])
        with urllib.request.urlopen(req) as response:
            html = response.read().decode('utf-8')
        doc = open((str(n)+'.html'), 'w', encoding='utf-8')
        doc.write(html)
        doc.close()
        n+=1
'''

def clean_arts():
    all_arts = info_from_part1()
    try:
        os.makedirs('./rassvet/exem')
    except:
        os.chdir('./rassvet/exem')
    n = 0
    for elem in all_arts:         
        req = urllib.request.Request(elem[3])
        with urllib.request.urlopen(req) as response:
            html = response.read().decode('utf-8')
        res = re.search('(<div class="art-article">.*article><.div>)', html, re.DOTALL)
        text = res.group(1)
        regTag = re.compile('<.*?>', flags=re.U | re.DOTALL)
        regScript = re.compile('<script>.*?</script>', flags=re.U | re.DOTALL)
        regComment = re.compile('<!--.*?-->', flags=re.U | re.DOTALL)
        clean_t = regScript.sub('', text)
        clean_t = regComment.sub('', clean_t)
        clean_t = regTag.sub('', clean_t)
        clean_t = clean_t.replace('&quot;', '"')
        clean_t = re.sub('&.*?;', '', clean_t)
        if elem[0] == 'no_title':
            elem.remove('no_title')
            res1 = re.search('<article class="art-post"><h2 class="art-postheader">(.*?)<', html)
            thetitle = res1.group(1)
            elem.insert(0, thetitle)
        print(elem)
            
        n+=1
        docc = open('i'+ str(n) + '.txt', 'w', encoding='utf-8')
        docc.write(clean_t)
        docc.close()
    aa = open('complete_aa_utf.csv', 'w', encoding='utf-8')
    for eleme in all_arts:
        elemet = ';'.join(eleme)
        aa.write(elemet)
    aa.close()

def making_aa_win():
    os.chdir('./rassvet/exem')
    aa = open('complete_aa_utf.csv', 'r', encoding='utf-8')
    table = aa.read()
    aa_win = open('complete_aa_win.csv', 'w', encoding='utf-16')
    table = table.replace('&quot;', '"')
    table = table.replace(';', '\t')
    aa_win.write(table)
    aa.close()
    aa_win.close()

def lets_mystem_it():
    os.chdir('./rassvet/exem')
    ttable = []
    table = open('complete_aa_win.csv', 'r', encoding='utf-16')
    for line in table:
        lline = line.split('\t')
        ttable.append(lline)
    
    for root, dirs, files in os.walk('.'):
        n = 0
        for file in files:
            if file[0] == 'i':
                art = ttable[n]
                if art[1] != 'no date':
                    date = art[1].split('.')
                    thelink = art[3].split('/')
                    thenum = thelink[-1]
                    thenum = thenum.replace('\n', '')
                   n+=1
                    command = './mystem -cdi ' + file + ' /Users/Matvey/Desktop/homeworks_mkold/project/rassvet/mystem_plain/' + date[2] + '/' + date[1] + '/'+ thenum + '.txt'
                    os.system(command)
                else:
                    thelink = art[3].split('/')
                    thenum = thelink[-1]
                    n += 1
                    thenum = thenum.replace('\n', '')
                    command = './mystem -cdi ' + file + ' /Users/Matvey/Desktop/homeworks_mkold/project/rassvet/mystem_plain/2014-2016/'+ thenum + '.txt'
                    os.system(command)

def lets_mystem_it_xml():
    os.chdir('./rassvet/exem')
    ttable = []
    table = open('complete_aa_win.csv', 'r', encoding='utf-16')
    for line in table:
        lline = line.split('\t')
        ttable.append(lline)
    
    for root, dirs, files in os.walk('.'):
        n = 0
        for file in files:
            if file[0] == 'i':
                art = ttable[n]
                if art[1] != 'no date':
                    print(art[1])
                    n+=1
                    date = art[1].split('.')
                    thelink = art[3].split('/')
                    thenum = thelink[-1]
                    thenum = thenum.replace('\n', '')
                    n += 1
                    command = './mystem -cdi --format xml ' + file + ' /Users/Matvey/Desktop/homeworks_mkold/project/rassvet/mystem_xml/' + date[2] + '/' + date[1] + '/'+ thenum + '.xml'
                    os.system(command)
                else:
                    thelink = art[3].split('/')
                    thenum = thelink[-1]
                    n += 1
                    thenum = thenum.replace('\n', '')
                    command = './mystem -cdi --format xml ' + file + ' /Users/Matvey/Desktop/homeworks_mkold/project/rassvet/mystem_xml/2014-2016/'+ thenum + '.xml'
                    print(command)
                    os.system(command)

def lets_plain():
    os.chdir('./rassvet/exem')
    ttable = []
    table = open('complete_aa_win.csv', 'r', encoding='utf-16')
    for line in table:
        lline = line.split('\t')
        ttable.append(lline)
    for root, dirs, files in os.walk('.'):
        n = 0
        for file in files:
            if file[0] == 'i':
                art = ttable[n]
                if art[1] != 'no date':
                    date = art[1].split('.')
                    thelink = art[3].split('/')
                    thenum = thelink[-1]
                    thenum = thenum.replace('\n', '')
                    n+=1
                    theway = '/Users/Matvey/Desktop/homeworks_mkold/project/rassvet/plain/' + date[2] + '/' + date[1] + '/'+ thenum + '.txt'
                    year = date[2]
                    plain = open(theway, 'w', encoding='utf-8')
                    iplain = open(file, 'r', encoding='utf-8')
                    itext = iplain.read()
                    plain.write('@au Noname\n')
                    plain.write('@ti ' + art[0] + '\n')
                    plain.write('@da ' + art[1] + '\n')
                    plain.write('@topic ' + art[2] + '\n')
                    plain.write('@url ' + art[3] + '\n\n')
                    plain.write(itext)
                    plain.close()
                    iplain.close()
                else:
                    thelink = art[3].split('/')
                    thenum = thelink[-1]
                    n += 1
                    thenum = thenum.replace('\n', '')
                    theway = '/Users/Matvey/Desktop/homeworks_mkold/project/rassvet/plain/2014-2016/'+ thenum + '.txt'
                    plain = open(theway, 'w', encoding='utf-8')
                    iplain = open(file, 'r', encoding='utf-8')
                    itext = iplain.read()
                    plain.write('@au Noname\n')
                    plain.write('@ti ' + art[0] + '\n')
                    plain.write('@da ' + art[1] + '\n')
                    plain.write('@topic ' + art[2] + '\n')
                    plain.write('@url ' + art[3] + '\n\n')
                    plain.write(itext)
                    plain.close()
                    iplain.close()
                art.append(theway)
                try:
                    art.append(year)
                except:
                    art.append('no year')
                
    return ttable

def lets_table(table):
    row = '%s\tNoname\t\t\t%s\t%s\tпублицистика\t\t\t%s\t\tнейтральный\tн-возраст\tн-уровень\tрайонная\t%s\tРАССВЕТ\t\t%s\tгазета\tРоссия\tЯкшур-Бодьинский район Удмуртской Республики\tru\n'
    meta = open('/Users/Matvey/Desktop/homeworks_mkold/project/rassvet/metadata.csv', 'w', encoding='utf-16')
    meta.write('path\tauthor\tsex\tbirthday\theader\tcreated\tsphere\tgenre_fi\ttype\ttopic\tchronotop\tstyle\taudience_age\taudience_level\taudience_size\tsource\tpublication\tpublisher\tpubl_year\tmedium\tcountry\tregion\tlanguage\n')
    for elem in table:
        theurl = elem[3].replace('\n', '')
        meta.write(row % (elem[4], elem[0], elem[1], elem[2], theurl, elem[5]))
      
def del_empty(theroot): #удаляет пустые папки
    for root, dirs, files in os.walk(theroot):
        try:
            os.rmdir(root)
        except:
            pass
            
def main():
#    val = get_articles_htmls()
    val1 = clean_arts()
    val2 = making_aa_win()
    val3 = lets_mystem_it()
    val4 = lets_mystem_it_xml()
    val5 = lets_plain()
    val6 = lets_table(val5)
    del_empty('./rassvet')

if __name__ ==  '__main__':
    main()
