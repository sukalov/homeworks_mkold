import re
import os
import urllib.request

def reading_list(way):
    text = open('texts/' + way, 'r', encoding = 'utf-8')
    text1 = text.read()
    text1 = text1.lower()
    text1 = text1.replace('\n', ' ')
    for smth in range(0,10):
        text1 = text1.replace('  ', ' ')
    text_list = text1.split(' ')
    text.close()
    i = 0
    for sym in text_list:
        text_list[i] = sym.strip('!.,?;:{}[]()<>:+_-–=*/\"#\a«”»,—“')
        i += 1
    return text_list

def write_txt(what, where):
    doc = open(where, 'w', encoding='utf-8')
    doc.write(what)
    doc.close()

def write_words(what, where):
    doc = open(where, 'w', encoding='utf-8')
    arr = list(what)
    for word in sorted(arr):
        doc.write(word + '\n')
    doc.close()

def folder_and_htmls(url, num):
    try:
        os.makedirs('./htmls')
    except:
        pass
    req = urllib.request.Request(url)
    try:
        with urllib.request.urlopen(req) as response:
            html = response.read().decode('utf-8')
        write_txt(html, 'htmls/article_' + str(num) + '.html')
        num += 1
    except:
        with urllib.request.urlopen(req) as response:
            html = response.read().decode('windows-1251')
        write_txt(html, 'htmls/article_' + str(num) + '.html')
        num += 1
        

def make_htmls(urls):
    num = 1
    for address in urls:
        folder_and_htmls(address, num)
        num += 1


def clean_and_txt():  #матвей не забудь доделать очистку текстов !!!
    for root, dirs, files in os.walk('.'):
        n = 0
        try:
            os.makedirs('./texts')
        except:
            pass
        
        if root == './htmls':
            for file in files:
                n+=1
                html = open('htmls/' + file, 'r', encoding='utf-8')
                html_str = html.read()
                html.close()

                res1 = re.search('<div id="divLetterBranding" class="article_text_wrapper js-mediator-article">(.*?)<p class="b-article__text document_authors">', html_str, re.DOTALL)
                if res1:
                    html_str = res1.group(1)

                res2 = re.search('<article>(.*?)</p></div></article>', html_str, re.DOTALL)
                if res2:
                    html_str = res2.group(1)

                res3 = re.search('<div class="article__text__overview">.*?</div>(.*?)<!-- /52237517/RBCNews_native -->.*?<!--END Medialand -->(.*?)<span class="article__logo">', html_str, re.DOTALL)
                if res3:
                    html_str = res3.group(1) + res3.group(2)

                res4 = re.search('<div class="b-text clearfix js-topic__text" itemprop="articleBody">(.*?)</p></div></div', html_str, re.DOTALL)
                if res4:
                    html_str = res4.group(1)
                    
                res5 = re.search('</script></div></div></div>(.*?)</p></div>', html_str, re.DOTALL)
                if res5:
                    html_str = res5.group(1)
                    
                regTag = re.compile('<.*?>', flags=re.U | re.DOTALL)
                regScript = re.compile('<script>.*?</script>', flags=re.U | re.DOTALL)
                regComment = re.compile('<!--.*?-->', flags=re.U | re.DOTALL)
                clean_t = regScript.sub('', html_str)
                clean_t = regComment.sub('', clean_t)
                clean_t = regTag.sub(' ', clean_t)
                clean_t = clean_t.replace('&nbsp;', ' ')
                clean_t = clean_t.replace('&quot;', '"')
                clean_t = re.sub('&.*?;', '', clean_t)
               
                write_txt(clean_t, 'texts/' + str(n) + '.txt')

def collecting_stuff():

    file1 = set(reading_list('1.txt'))
    file2 = set(reading_list('2.txt'))
    file3 = set(reading_list('3.txt'))
    file4 = set(reading_list('4.txt'))
    file5 = set(reading_list('5.txt'))
    
    common_words = set()
    unique_words = set()
    common_words = file1 & file2 & file3 & file4 & file5
    
    unique1 = file1 - file2 - file3 - file4 - file5
    unique2 = file2 - file1 - file3 - file4 - file5
    unique3 = file3 - file2 - file1 - file4 - file5
    unique4 = file4 - file2 - file3 - file1 - file5
    unique5 = file1 - file2 - file3 - file4 - file1
    unique_words = unique1 | unique2 | unique3 | unique4 | unique5
    
                
    write_words(common_words, 'intersection.txt')
    write_words(unique_words, 'difference.txt')
    return unique_words

def collecting_other(unique):
    file1 = reading_list('1.txt')
    file2 = reading_list('2.txt')
    file3 = reading_list('3.txt')
    file4 = reading_list('4.txt')
    file5 = reading_list('5.txt')
    files = file1 + file2 + file3 + file4 +file5

    files_u = []
    files_u2 = []
    for elem in files:
        if elem in unique:
            if elem in files_u:
                files_u2.append(elem)
            else:
                files_u.append(elem)
    write_words(set(files_u2), 'difference2.txt')
                

def main():
    urls = ['http://www.kommersant.ru/doc/3158422',
     'https://rg.ru/2016/12/01/reg-szfo/sk-ne-nashel-neobosnovannogo-primeneniia-sily-k-osuzhdennomu-dadinu.html',
     'http://www.rbc.ru/society/01/12/2016/58404da29a794703ef0a8a97',
     'https://lenta.ru/news/2016/12/01/dadinvzakone/',
     'https://ria.ru/incidents/20161201/1482653470.html']
    make_htmls(urls)
    clean_and_txt()
    val = collecting_stuff()
    collecting_other(val)


if __name__ == '__main__':
    main()
