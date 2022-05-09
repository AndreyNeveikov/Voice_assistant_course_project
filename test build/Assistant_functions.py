import requests
import bs4
import webbrowser
import re
import subprocess
from urllib import request
from urllib.parse import quote
import urllib.request


# Чистит фразу от ключевых слов
def clean_phrase(statement, words_list):
    for x in words_list:
        statement = statement.replace(x, '')
    statement = statement.strip()
    return statement


# Функция дающая случайный анекдот
def anekdot():
    s = requests.get('http://anekdotme.ru/random')
    b = bs4.BeautifulSoup(s.text, "html.parser")
    p = b.select('.anekdot_text')
    s = (p[0].getText().strip())
    reg = re.compile('[^0-9a-zA-Zа-яА-я .,!?-]')
    s = reg.sub('', s)
    return s


# Открыть сайт во внешнем браузере
def open_url(url):
    webbrowser.open(url)


# Запускает внешнюю команду ОС
def os_run(cmd):
    PIPE = subprocess.PIPE
    p = subprocess.Popen(cmd, shell=True, stdin=PIPE, stdout=PIPE, stderr=subprocess.STDOUT)


def start_application(statement):
    answer = 'Такой команды я пока не знаю'
    statement = clean_phrase(statement, ['запусти', 'запустить'])
    if (statement.find("калькулятор") != -1) or (statement.find("calculator") != -1):
        os_run('calc')
        answer = 'Калькулятор запущен'
    if (statement.find("блокнот") != -1) or (statement.find("notepad") != -1):
        os_run('notepad')
        answer = 'Блокнот запущен'
    if (statement.find("paint") != -1) or (statement.find("паинт") != -1):
        os_run('mspaint')
        answer = 'Графический редактор запущен'
    if (statement.find("browser") != -1) or (statement.find("браузер") != -1):
        open_url('http://google.ru')
        answer = 'Запускаю браузер'
    if (statement.find("проводник") != -1) or (statement.find("файловый менеджер") != -1):
        os_run('explorer')
        answer = 'Проводник запущен'
    return answer


# Даёт iframe код ютуб ролика по любому поисковому запросу    
def find_on_tube(phrase):
    phrase = clean_phrase(phrase, ['хочу', 'на ютубе', 'на ютюбе', 'на ютуб', 'ютюб', 'на youtube', 'на you tube', 'на youtub', 'youtube', 'ютуб', 'ютубе', 'посмотреть', 'смотреть'])
    zz = []
    sq = 'http://www.youtube.com/results?search_query='+quote(phrase)
    doc = urllib.request.urlopen(sq).read().decode('cp1251', errors='ignore')
    match = re.findall(r"\?v\=(.+?)\"", doc)
    if not(match is None):
        for ii in match:
            if len(ii) < 25:
                zz.append(ii)
    zz2 = dict(zip(zz, zz)).values()
    zz3 = []
    for qq in zz2:
        zz3.append(qq)
    s = zz3[0]
    s = 'https://www.youtube.com/watch?v='+s+'?autoplay=1'
    return s


def browser_search(z):
    doc = urllib.request.urlopen('http://go.mail.ru/search?fm=1&q='+quote(z)).read().decode('unicode-escape', errors = 'ignore')
    sp = re.compile('title":"(.*?)orig').findall(doc)
    mas1 = []
    mas2 = []
    for x in sp:
        if (x.rfind('wikihow') == -1) and (x.rfind('an.yandex') == -1) and (x.rfind('wikipedia') == -1) and (x.rfind('otvet.mail.ru') == -1) and (x.rfind('youtube')==-1) and(x.rfind('.jpg')==-1) and (x.rfind('.png')==-1) and (x.rfind('.gif')==-1):
            a = x.replace(',', '')
            a = a.replace('"', '')
            a = a.replace('<b>', '')
            a = a.replace('</b>', '')
            a = a.split('url:')
            if len(a) > 1:
                z = a[0].split('}')
                mas1.append(z[0])
                z = a[1].split('}')
                z = z[0].split('title')
                mas2.append(z[0])
    return mas2






