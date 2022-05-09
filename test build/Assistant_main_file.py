from PyQt5 import QtCore, QtGui
from PyQt5.QtWidgets import QLabel, QApplication, QMainWindow
from PyQt5.QtWebEngineWidgets import *
import sys
import os
import threading
import speech_recognition as sr
import signal
import pyttsx3
import json
import apiai
import Assistant_functions


# Инициализируем SAPI5
engine = pyttsx3.init()
# Получаем список голосов
voices = engine.getProperty('voices')
# Устанавливаем русский язык
engine.setProperty('voice', 'ru')

# Скорость чтения
engine.setProperty('rate', 200)

# Получаем html шаблон для сообщений в окне чата
html_code = '<div class="robot">Чем я могу помочь?</div>'
file = open('chat.html', 'r', encoding='UTF-8')
html_template = file.read()
file.close()

# Получаем html шаблон help
file = open('help.html', 'r', encoding='UTF-8')
html_code_2 = file.read()
file.close()


# Функция, которая обращается к Dialogflow и получает ответ
def ai_message(s):
    # Токен API к Dialogflow (оставьте этот или натренируйте свою модель)
    request_to_api = apiai.ApiAI('7f01246612e64e3f89264a85a965ddd3').text_request()
    # На каком языке будет послан запрос
    request_to_api.lang = 'ru'
    # ID Сессии диалога (нужно, чтобы потом учить бота)
    request_to_api.session_id = 'voice_assistant'
    # Посылаем запрос к ИИ с сообщением от юзера
    request_to_api.query = s
    response_json = json.loads(request_to_api.getresponse().read().decode('utf-8'))
    # Разбираем JSON и вытаскиваем ответ
    response = response_json['result']['fulfillment']['speech']
    # Если есть ответ от бота - выдаём его,
    # если нет - бот его не понял
    if response:
        return response
    else:
        return 'Я Вас не поняла :/'


answer = ''
listen = ''
request = ''
not_listen = ''
speaking = ''

# Объявляем распознавание речи от Google
r = sr.Recognizer()


def thread(my_func):    # Отдельный поток
    def wrapper(*args, **kwargs):
        my_thread = threading.Thread(target=my_func, args=args, kwargs=kwargs)
        my_thread.start()
    return wrapper


global interrupted_thread


# Функции для сигналов между потоками
def signal_handler(thread_signal, frame):
    global interrupted_thread
    interrupted_thread = True


def interrupt_callback():
    global interrupted_thread
    return interrupted_thread


# Функция активизирует Google Speech Recognition для распознавания команд
@thread
def listen_command():
    global listen
    global request
    global not_listen
    # Следим за состоянием ассистента - слушает она или говорит
    listen.emit([1])
    # Слушаем микрофон
    with sr.Microphone() as source:
        audio = r.listen(source)
    try:
        # Отправляем запись с микрофона гуглу, получаем распознанную фразу
        voice_record = r.recognize_google(audio, language="ru-RU").lower()
        # Меняем состояние ассистента со слушания на ответ
        listen.emit([2])
        # Отправляем распознанную фразу на обработку в функцию response_to_user_request
        request.emit([voice_record])
    # В случае ошибки меняем состояние ассистента на "не расслышал"
    except sr.UnknownValueError:
        print("Робот не расслышал фразу")
        not_listen.emit(['00'])
    except sr.RequestError as e:
        print("Ошибка сервиса; {0}".format(e))


signal.signal(signal.SIGINT, signal_handler)

global pr_urls
global pr_cmd


# Графический интерфейс PyQt 
class Program_window(QMainWindow):
    # Объявляем сигналы, которые приходят от асинхронных функций
    thread_signal = QtCore.pyqtSignal(list, name='thread_signal')
    assistant_listen = QtCore.pyqtSignal(list, name='assistant_listen')
    user_request = QtCore.pyqtSignal(list, name='user_request')
    unrecognized_speech = QtCore.pyqtSignal(list, name='unrecognized_speech')

    def __init__(self, *args):
        super().__init__()
        self.setAnimated(False)
        self.flag = True
        self.centralwidget = QMainWindow()
        self.centralwidget.setObjectName("centralwidget")
        self.setCentralWidget(self.centralwidget)
        # Label в который мы загрузим картинку с девушкой
        self.label = QLabel(self.centralwidget)
        # Прикрепляем к Label функцию обработки клика
        self.label.installEventFilter(self)
        # Настраиваем вид курсора на картинке
        self.label.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        # Позиционируем Label внутри окна
        self.label.setGeometry(QtCore.QRect(2, 2, 400, 300))
        # Объявляем элемент QWebEngineView для отображения html странички с чатом
        self.browser = QWebEngineView(self.centralwidget)
        # Объявляем элемент QWebEngineView для отображения видео с ютуба, текстов и веб страниц
        self.browser2 = QWebEngineView(self.centralwidget)
        # Позиционируем QWebEngineView внутри окна
        self.browser.setGeometry(QtCore.QRect(2, 305, 400, 300))
        self.browser2.setGeometry(QtCore.QRect(405, 2, 930, 603))

        # Загружаем в QWebEngineView html документ с чатом
        global html_template
        global html_code
        global html_code_2
        html_result = html_template.replace('%code%', html_code)
        self.browser.setHtml(html_result, QtCore.QUrl("file://"))
        self.browser.show()
        self.browser2.setHtml(html_code_2, QtCore.QUrl("file://"))
        self.browser2.show()  
        self.label.setText("<center><img src='file:///"+os.getcwd()+"/img/img_greetings.jpg'></center>")
        # Соединяем сигналы и функции класса
        global answer
        answer = self.thread_signal
        global listen
        listen = self.assistant_listen
        global not_listen
        not_listen = self.unrecognized_speech
        global request
        request = self.user_request
        self.assistant_listen.connect(self.picture_change, QtCore.Qt.QueuedConnection)
        self.user_request.connect(self.response_to_user_request, QtCore.Qt.QueuedConnection)
        self.unrecognized_speech.connect(self.response_to_unrecognized_speech, QtCore.Qt.QueuedConnection)

    # Обработка клика по картинке
    def eventFilter(self, obj, event):
        if event.type() == 2:
            btn = event.button()
            if btn == 1:
                listen_command()
            elif btn == 2:
                self.label.setText("<center><img src='file:///"+os.getcwd()+"/img/img_greetings.jpg'></center>")
        return super(QMainWindow, self).eventFilter(obj, event)

    # Смена картинки в зависимости от того слушает она или говорит
    def picture_change(self, data):
        if data[0] == 1:
            # Ассистент слушает
            self.label.setText("<center><img src='file:///"+os.getcwd()+"/img/img_listen.jpg'></center>")
        if data[0] == 2:
            # Ассистент говорит
            self.label.setText("<center><img src='file:///"+os.getcwd()+"/img/img_greetings.jpg'></center>")

    # Добавление в html чат фразы ассистента
    def adding_response_to_chat_by_assistant(self, phrase):
        global html_template
        global html_code
        html_code = '<div class="robot">' + phrase + '</div>' + html_code
        html_result = html_template.replace('%code%', html_code)
        self.browser.setHtml(html_result, QtCore.QUrl("file://"))
        self.browser.show()

    # Добавление в html чат фразы пользователя
    def adding_query_to_chat_by_user(self, phrase):
        global html_template
        global html_code
        html_code = '<div class="you">' + phrase + '</div>' + html_code
        html_result = html_template.replace('%code%', html_code)
        self.browser.setHtml(html_result, QtCore.QUrl("file://"))
        self.browser.show()

    # Произносим ответ вслух синтезом речи
    @staticmethod
    def pronounce_assistant_answer(phrase):
        global engine
        engine.say(phrase)
        engine.runAndWait()
        engine.stop()
 
    # Функция в которой решаем что отвечать на фразы пользователя    
    def response_to_user_request(self, data):
        global pr_urls
        global pr_cmd
        # Получаем фразу от пользователя
        vp = data[0].lower()
        # Отображаем её в чате
        self.adding_response_to_chat_by_assistant(vp)
        # Ответ по умолчанию
        assistant_answer = 'Я не поняла запрос'
        try:
            # Выполняем разные действия в зависимости от наличия ключевых слов фо фразе
            if vp == 'пока' or vp == 'выход' or vp == 'выйти' or vp == 'до свидания':
                assistant_answer = 'Ещё увидимся!'
                self.adding_query_to_chat_by_user(assistant_answer)
                self.pronounce_assistant_answer(assistant_answer)
                sys.exit(app.exec_())
            elif 'анекдот' in vp:
                assistant_answer = Assistant_functions.anekdot()
            elif 'запусти' in vp:
                assistant_answer = Assistant_functions.start_application(vp)
            elif ((vp.find("youtube") != -1) or (vp.find("ютюб") != -1) or
                  (vp.find("ютуб") != -1) or (vp.find("you tube") != -1))\
                    and (vp.find("смотреть") != -1):
                self.browser2.load(QtCore.QUrl(Assistant_functions.find_on_tube(vp)))
                assistant_answer = 'Вот видео.'
            elif (vp.find("слушать") != -1) and (vp.find("песн") != -1):
                self.browser2.load(QtCore.QUrl(Assistant_functions.find_on_tube(vp)))
                assistant_answer = 'Вот песня.'
            elif ((vp.find("найти") != -1) or (vp.find("найди") != -1)) \
                    and not(vp.find("статью") != -1):
                user_request = Assistant_functions.clean_phrase(vp, ['найти', 'найди', 'про', 'про то', 'о том'])
                question = Assistant_functions.browser_search(user_request)
                self.browser2.load(QtCore.QUrl(question[0]))
                assistant_answer = 'Ответ найден'
        except():
            # Если ключевых слов не нашли, используем Dialogflow
            assistant_answer = ai_message(vp)
        # Добавляем ответ в чат
        self.adding_query_to_chat_by_user(assistant_answer)
        # Читаем ответ вслух
        self.pronounce_assistant_answer(assistant_answer)
        
    # Функция меняет картинку если ассистент тебя не расслышал
    def response_to_unrecognized_speech(self, data):
        self.label.setText("<center><img src='file:///"+os.getcwd() +
                           "/img/img_response_to_unrecognized_speech.jpg'></center>")


# Запускаем программу на выполнение    
app = QApplication([])
window = Program_window()
window.resize(1340, 615)    # Размер окна
window.show()
app.exec_()
