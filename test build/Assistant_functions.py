# Functional
from urllib.parse import quote
from urllib import request
import urllib.request
import subprocess
import webbrowser
import requests
import bs4
import re
import os


def clean_phrase(statement, words_list):
    """
    Cleans keywords in a phrase

    :param statement: phrase
    :param words_list: keywords
    :return: clean phrase
    """
    for word in words_list:
        statement = statement.replace(word, '')
    statement = statement.strip()
    return statement


def tell_joke():
    """
    A function that gives a random joke (anecdote)

    :return: joke from site
    """
    joke = requests.get('http://anekdotme.ru/random')
    joke_parser = bs4.BeautifulSoup(joke.text, "html.parser")
    parsed_joke = joke_parser.select('.anekdot_text')
    joke = (parsed_joke[0].getText().strip())
    reg_ex = re.compile('[^0-9a-zA-Zа-яА-я .,!?-]')
    joke = reg_ex.sub('', joke)
    return joke


def assistant_answering_dialogue_phrase(phrase):
    """
    Answers user questions

    :param phrase: user question
    :return: prepared answer
    """
    answer = 'Пожалуйста, повторите фразу!'
    phrase = clean_phrase(phrase,
                          ['ответь', 'скажи'])

    if (phrase.find("кто"
                    "") != -1) and (phrase.find("тебя") != -1) and (phrase.find("создал") != -1):
        answer = 'Меня создал Невейков Андрей'

    elif (phrase.find("как") != -1) and (phrase.find("тебя") != -1)\
            and (phrase.find("зовут") != -1):
        answer = 'Можете обращаться просто ассистент.'

    elif ((phrase.find("сколько") != -1) and (phrase.find("тебе") != -1)
          and (phrase.find("лет") != -1)) or ((phrase.find("твой") != -1)
                                              and (phrase.find("возраст") != -1)):
        answer = 'Можете обращаться просто ассистент.'

    elif (phrase.find("какие") != -1) and (phrase.find("библиотеки") != -1)\
            and (phrase.find("ты") != -1) and (phrase.find("используешь") != -1):
        answer = '''Извините за акцент: urllib, subprocess, webbrowser,
        requests, bs4, re, os, sqlite3, PyQt5, speech recognition,
        threading, pyttsx3, signal, sys'''

    elif (phrase.find("такое") != -1) and ((phrase.find("ооп") != -1)
                                           or (phrase.find("офп") != -1)
                                           or (phrase.find("о о п") != -1)
                                           or (phrase.find("о п") != -1)):
        answer = '''
        Объектно-ориентированное программирование — методология программирования,
        основанная на представлении программы в виде совокупности объектов, 
        каждый из которых является экземпляром определённого класса, 
        а классы образуют иерархию наследования.
        '''

    elif (phrase.find("такое") != -1) and (phrase.find("паттерн") != -1) \
            and (phrase.find("проектирования") != -1):
        answer = '''
        Паттерн проектирования - это повторяемая архитектурная конструкция,
        представляющая собой решение проблемы проектирования в рамках
        некоторого часто возникающего контекста.
        '''

    return answer


def open_url(url):
    """
    Function that opens the site in a browser

    :param url: link to site
    :return: nothing, just open site
    """
    webbrowser.open(url)


def os_run(cmd):
    """
    Runs an external OS command to
    run a standard application as a subprocess

    :param cmd: Abbreviated notation for command line
    :return: nothing, just create a subprocess and runs an application
    """
    pipe = subprocess.PIPE
    p = subprocess.Popen(cmd, shell=True, stdin=pipe, stdout=pipe, stderr=subprocess.STDOUT)


def start_application(statement):
    """
    The function responsible for selecting the desired application to run

    :param statement: phrase
    :return: reply to a chat with an assistant
    """
    answer = 'Это команде меня не научили'
    statement = clean_phrase(statement, ['запусти', 'запустить'])

    if (statement.find("торент") != -1) or (statement.find("торрент") != -1) \
            or (statement.find("медиагет") != -1) or (statement.find("mediaget") != -1):
        os.startfile('C:\\Users\\User\\MediaGet2\\mediaget.exe')
        answer = 'Торент запущен'

    elif ((statement.find("visual") != -1) or (statement.find("визуал") != -1)
          or (statement.find("вижуал") != -1)) \
            and ((statement.find("studio") != -1) or (statement.find("студио") != -1)):
        os.startfile("E:\\VS\\Common7\\IDE\\devenv.exe")
        answer = 'Вижуал студио запущен'

    elif ((statement.find("sublime") != -1) or (statement.find("саблайм") != -1)) \
            and ((statement.find("text") != -1) or (statement.find("текст") != -1)):
        os.startfile("E:\\Sublime Text 3\\sublime_text.exe")
        answer = 'Саблайм текст запущен'

    elif (statement.find("скайп") != -1) or (statement.find("skype") != -1):
        os.startfile("C:\\Program Files (x86)\\Microsoft\\Skype for Desktop\\Skype.exe")
        answer = 'Скайп запущен'

    elif (statement.find("телеграм") != -1) or (statement.find("telegram") != -1):
        os.startfile("D:\\Telegram\\Telegram Desktop\\Telegram.exe")
        answer = 'Телеграмм запущен'

    elif (statement.find("гугл") != -1) or (statement.find("гугол") != -1) \
            or (statement.find("google") != -1):
        os.startfile("C:\\Program Files (x86)\\Google\\Chrome\\Application\\chrome.exe")
        answer = 'Гугл запущен'

    elif (statement.find("калькулятор") != -1) or (statement.find("calculator") != -1):
        os_run('calc')
        answer = 'Калькулятор запущен'

    elif (statement.find("блокнот") != -1) or (statement.find("notepad") != -1):
        os_run('notepad')
        answer = 'Блокнот запущен'

    elif (statement.find("paint") != -1) or (statement.find("паинт") != -1):
        os_run('mspaint')
        answer = 'Пэинт запущен'

    elif (statement.find("browser") != -1) or (statement.find("браузер") != -1):
        open_url('http://google.ru')
        answer = 'Запускаю браузер'

    elif (statement.find("проводник") != -1) or (statement.find("файловый менеджер") != -1):
        os_run('explorer')
        answer = 'Проводник запущен'

    elif (statement.find("гитхаб") != -1) or (statement.find("github") != -1):
        subprocess.run(['C:\\Users\\User\\AppData\\Local\\GitHubDesktop\\GitHubDesktop.exe'])
        answer = 'Гитхаб запущен'

    return answer


def find_on_you_tube(phrase):
    """
    Gives link on YouTube video code for any search query

    :param phrase: youtube video request
    :return: link to the first video in the issue
    """
    phrase = clean_phrase(phrase,
                          ['хочу', 'на ютубе', 'на ютюбе', 'на ютуб', 'ютюб', 'на youtube',
                           'на you tube', 'на youtub', 'youtube', 'ю туб', 'ютубе',
                           'посмотреть', 'смотреть'])
    tmp_list_for_ends_of_links = []
    compound_query = 'http://www.youtube.com/results?search_query='+quote(phrase)
    doc = urllib.request.urlopen(compound_query).read().decode('cp1251', errors='ignore')
    match = re.findall(r"\?v=(.+?)\"", doc)

    if not(match is None):
        for link_collector in match:
            if len(link_collector) < 25:
                tmp_list_for_ends_of_links.append(link_collector)

    tmp_dict_for_ends_of_links = dict(
        zip(tmp_list_for_ends_of_links, tmp_list_for_ends_of_links)).values()
    tmp_list_for_link = []
    for ends_of_links in tmp_dict_for_ends_of_links:
        tmp_list_for_link.append(ends_of_links)
    compound_youtube_link = tmp_list_for_link[0]
    compound_youtube_link = 'https://www.youtube.com/watch?v=' +\
                            compound_youtube_link+'?autoplay=1'
    return compound_youtube_link


def browser_search(user_request):
    """
    A function that finds links to sites that match the query

    :param user_request: browser search request
    :return: list of several links to suitable sites
    """
    doc = urllib.request.urlopen(
        'http://go.mail.ru/search?fm=1&q=' + quote(user_request)).read().decode(
        'unicode-escape', errors='ignore')
    parsed_page = re.compile('title":"(.*?)orig').findall(doc)
    tmp_search_result = []
    search_result = []

    for elements in parsed_page:
        if (elements.rfind('wikihow') == -1) and (elements.rfind('an.yandex') == -1)\
                and (elements.rfind('wikipedia') == -1) and (elements.rfind('otvet.mail.ru') == -1)\
                and (elements.rfind('youtube') == -1) and (elements.rfind('.jpg') == -1)\
                and (elements.rfind('.png') == -1) and (elements.rfind('.gif') == -1):
            answer = elements.replace(',', '')
            answer = answer.replace('"', '')
            answer = answer.replace('<b>', '')
            answer = answer.replace('</b>', '')
            answer = answer.split('url:')

            if len(answer) > 1:
                user_request = answer[0].split('}')
                tmp_search_result.append(user_request[0])
                user_request = answer[1].split('}')
                user_request = user_request[0].split('title')
                search_result.append(user_request[0])

    return search_result
