import requests
import bs4
import webbrowser
import re
import os
import subprocess
from urllib import request
from urllib.parse import quote
import urllib.request


# Чистит фразу от ключевых слов
def clean_phrase(statement, words_list):
    for word in words_list:
        statement = statement.replace(word, '')
    statement = statement.strip()
    return statement


# Функция дающая случайный анекдот
def tell_joke():
    joke = requests.get('http://anekdotme.ru/random')
    joke_parser = bs4.BeautifulSoup(joke.text, "html.parser")
    parsed_joke = joke_parser.select('.anekdot_text')
    joke = (parsed_joke[0].getText().strip())
    reg_ex = re.compile('[^0-9a-zA-Zа-яА-я .,!?-]')
    joke = reg_ex.sub('', joke) 
    return joke


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
    if (statement.find("гитхаб") != -1) or (statement.find("github") != -1):
        subprocess.run(['C:\\Users\\User\\AppData\\Local\\GitHubDesktop\\GitHubDesktop.exe'])
        answer = 'GitHub Desktop запущен'
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
    if (statement.find("телеграм") != -1) or (statement.find("telegram") != -1):
        os.startfile("D:\\Telegram\\Telegram Desktop\\Telegram.exe")
        answer = 'Telegram запущен'
    if (statement.find("гугл") != -1) or (statement.find("гугол") != -1) \
            or (statement.find("google") != -1):
        os.startfile("C:\\Program Files (x86)\\Google\\Chrome\\Application\\chrome.exe")
        answer = 'Google запущен'
    return answer


# Даёт iframe код ютуб ролика по любому поисковому запросу    
def find_on_tube(phrase):
    phrase = clean_phrase(phrase, ['хочу', 'на ютубе', 'на ютюбе', 'на ютуб', 'ютюб', 'на youtube', 'на you tube', 'на youtub', 'youtube', 'ютуб', 'ютубе', 'посмотреть', 'смотреть'])
    tmp_list_for_ends_of_links = []
    compound_query = 'http://www.youtube.com/results?search_query='+quote(phrase)
    doc = urllib.request.urlopen(compound_query).read().decode('cp1251', errors='ignore')
    match = re.findall(r"\?v\=(.+?)\"", doc)
    if not(match is None):
        for link_collector in match:
            if len(link_collector) < 25:
                tmp_list_for_ends_of_links.append(link_collector)

    tmp_dict_for_ends_of_links = dict(zip(tmp_list_for_ends_of_links, tmp_list_for_ends_of_links)).values()
    tmp_list_for_link = []
    for ends_of_links in tmp_dict_for_ends_of_links:
        tmp_list_for_link.append(ends_of_links)
    compound_youtube_link = tmp_list_for_link[0]
    compound_youtube_link = 'https://www.youtube.com/watch?v='+compound_youtube_link+'?autoplay=1'
    return compound_youtube_link


def browser_search(first_result):
    doc = urllib.request.urlopen(
        'http://go.mail.ru/search?fm=1&q=' + quote(first_result)).read().decode(
        'unicode-escape', errors='ignore')
    parsed_page = re.compile('title":"(.*?)orig').findall(doc)
    tmp_search_result = []
    search_result = []
    for elements in parsed_page:
        if (elements.rfind('wikihow') == -1) and (elements.rfind('an.yandex') == -1) and (elements.rfind('wikipedia') == -1) and (elements.rfind('otvet.mail.ru') == -1) and (elements.rfind('youtube') == -1) and (elements.rfind('.jpg') == -1) and (elements.rfind('.png')== -1) and (elements.rfind('.gif') == -1):
            answer = elements.replace(',', '')
            answer = answer.replace('"', '')
            answer = answer.replace('<b>', '')
            answer = answer.replace('</b>', '')
            answer = answer.split('url:')
            if len(answer) > 1:
                first_result = answer[0].split('}')
                tmp_search_result.append(first_result[0])
                first_result = answer[1].split('}')
                first_result = first_result[0].split('title')
                search_result.append(first_result[0])
    return search_result





