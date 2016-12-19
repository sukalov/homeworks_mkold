import re
import os

def write_txt(what, where):
    doc = open(where, 'w', encoding='utf-8')
    for elem in what:
        doc.write(elem + '\n')
    doc.close()
def write_txt2(what, where):
    doc = open(where, 'w', encoding='utf-8')
    for elem in what:
        doc.write(elem)
    doc.close()

def reading_list(text1):
    text1 = text1.lower()
    text1 = text1.replace('\n', ' ')
    text1 = text1.replace('\t', ' ')
    for smth in range(0,50):
        text1 = text1.replace('  ', ' ')
    text_list = text1.split(' ')
    i = 0
    for sym in text_list:
        text_list[i] = sym.strip('!.,?;:{}[]()<>:+_-–=*/\"#\a«”»,—“')
        i += 1
    return text_list

def wordset():
    wordset = set()
    file = open('adyghe-unparsed-words.txt', 'r', encoding='utf-8')
    for line in file:
        line = line.strip(' \n')
        wordset.add(line)
    file.close()
    return wordset

def wordlist():
    complete_wl = set()
    words = wordset()
    page = open('politicer.html', 'r', encoding='utf-8')
    pagetxt = page.read()
    res = re.search('<body class="archive category category-politics category-3">(.*)</div><!-- #site-info -->', pagetxt, re.DOTALL)
    page_txt = res.group(1)

    regTag = re.compile('<.*?>', flags=re.U | re.DOTALL)
    regScript = re.compile('<script>.*?</script>', flags=re.U | re.DOTALL)
    regComment = re.compile('<!--.*?-->', flags=re.U | re.DOTALL)
    clean_t = regScript.sub('', page_txt)
    clean_t = regComment.sub('', clean_t)
    clean_t = regTag.sub(' ', clean_t)
    clean_t = clean_t.replace('&nbsp;', ' ')
    clean_t = clean_t.replace('&quot;', '"')
    clean_t = re.sub('&.*?;', '', clean_t)
    text = reading_list(clean_t)

    textset = set(text)

    for elem in textset:
        if elem in words:
            complete_wl.add(elem)

    write_txt(complete_wl, 'wordlist.txt')
    return complete_wl

def mysteming():
    command = './mystem -cdi adyghe-unparsed-words.txt mystemed.txt'
    os.system(command)

def rus_nouns():
    nouns = []
    mystemed = open('mystemed.txt', 'r', encoding='utf-8')
    for line in mystemed:
        if '?' not in line and not line.startswith('ӏ') and '}-' not in line and '}ӏ' not in line:
            #ТИМОФЕЙ АЛЕКСАНДРОВИЧ РАЗРЕШИЛ УДАЛИТЬ ВСЕ СЛОВА С ДЕФИСАМИ И ПАЛКАМИ ВНАЧАЛЕ
            res = re.search('=S[^|]*=им', line)
            if res:
                nouns.append(line)

    write_txt2(nouns, 'rus_nouns.txt')
    return set(nouns)

def sql_make():
    commands = set()
    for element in rus_nouns():
        res = re.search('(.*)\{([^|]*)=S', element)
        command = 'INSERT INTO my_table (wordform, lemma) values ("' + res.group(1) + '", "' + res.group(2) +'")'
        commands.add(command)
    write_txt(commands, 'sql.txt')
    
def main():
    wordlist()
    mysteming()
    rus_nouns()
    sql_make()
    
if __name__ == '__main__':
    main()
