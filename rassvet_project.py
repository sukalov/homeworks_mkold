import os
import urllib.request

def get_html(site):
    req = urllib.request.Request(site)
    with urllib.request.urlopen(req) as response:
        html = response.read().decode('utf-8')
    return html

def write_txt(what, where):
    doc = open(where, 'w', encoding='utf-8')
    doc.write(what)
    doc.close()
    
    
def main():
    val = get_html('http://xn-----6kcgcpd5bzbmfhaqr3fud1bj.xn--p1ai/')
    val1 = write_txt(val, 'first_html.txt')

if __name__ ==  '__main__':
    main()
