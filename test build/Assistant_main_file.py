# Interface
from PyQt5.QtWidgets import QLabel, QApplication, QMainWindow
from PyQt5.QtWebEngineWidgets import *
from PyQt5 import QtCore, QtGui

# Functional
import speech_recognition as sr
import threading
import pyttsx3
import signal
import apiai
import json
import sys
import os

# Files
import Assistant_functions


engine = pyttsx3.init()    # Initialize SAPI5
voices = engine.getProperty('voices')    # Get a list of available votes
engine.setProperty('voice', 'ru')    # Set the Russian language
engine.setProperty('rate', 200)    # Set voice speed

for voice in voices:    # Select the desired voice
    if voice.name == 'Elena':
        engine.setProperty('voice', voice.id)

# Get the html page for messages in the chat window
html_code = '<div class="robot">Чем я могу помочь?</div>'
file = open('chat.html', 'r', encoding='UTF-8')
html_template = file.read()
file.close()

# Get the html page feature_list
file = open('feature_list.html', 'r', encoding='UTF-8')
html_code_2 = file.read()
file.close()


def ai_message(phrase):
    """
    A function that calls Dialogflow and receives a response

    :param phrase: user phrase
    :return: issue an assistant's answer or a blank that the message is not understood
    """
    # API token to Dialogflow
    request_to_api = apiai.ApiAI('7f01246612e64e3f89264a85a965ddd3').text_request()

    request_to_api.lang = 'ru'   # Request language
    request_to_api.session_id = 'voice_assistant'   # Dialog session ID
    request_to_api.query = phrase   # Sending a request with a message from the user

    # Getting a response
    response_json = json.loads(request_to_api.getresponse().read().decode('utf-8'))
    response = response_json['result']['fulfillment']['speech']  # Parse JSON and get response
    if response:    # If there is a response from the assistant - issue it
        return response
    else:   # if there is no answer, we display a stub about an incomprehensible question
        return 'Я Вас не поняла :/'


r = sr.Recognizer()     # Variable for speech recognition from Google


def thread(my_func):
    """
    Function that creates a separate thread
    (used as decorator)

    :param my_func: a function to run on a new thread
    :return: wrapper
    """
    def wrapper(*args, **kwargs):
        my_thread = threading.Thread(target=my_func, args=args, kwargs=kwargs)
        my_thread.start()
    return wrapper


global interrupted_thread


def signal_handler(thread_signal, frame):
    """
    Function for signals between threads

    :param thread_signal: thread signal
    :param frame: signal handler
    :return: nothing, just changes the state of the thread
    """
    global interrupted_thread
    interrupted_thread = True


def interrupt_callback():
    """
    A function that accesses an interrupted thread

    :return: a thread interrupted by another thread
    """
    global interrupted_thread
    return interrupted_thread


@thread
def listen_command():
    """
    Activates Speech Recognition to recognize commands

    :return: recognized phrase or handled error
    """
    global listen
    global request
    global not_listen

    listen.emit([1])    # Monitoring the state of the assistant (listens or speaks)
    with sr.Microphone() as source:     # Listen to the microphone
        audio = r.listen(source)
    try:
        # Send the record to Google, get the recognized phrase
        voice_record = r.recognize_google(audio, language="ru-RU").lower()
        listen.emit([2])    # Change the assistant's state from listening to answering
        # Send the recognized phrase for processing to the response_to_user_request function
        request.emit([voice_record])
    # In case of an error, change the state of the assistant to "didn't hear"
    except sr.UnknownValueError:
        print("Ассистент не расслышал фразу")
        not_listen.emit(['00'])
    except sr.RequestError as error:
        print("Ошибка сервиса; {0}".format(error))


signal.signal(signal.SIGINT, signal_handler)    # Thread signal processing

global p_urls
global p_cmd


# Blanks for the state of threads
answer = ''
listen = ''
request = ''
not_listen = ''
speaking = ''


class ProgramWindow(QMainWindow):
    """
    Create a PyQt interface
    """
    # Declare signals that come from asynchronous functions
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
        # Label in which we will load pictures
        self.label = QLabel(self.centralwidget)
        # Attach a click handling function to the Label
        self.label.installEventFilter(self)
        # Customize the appearance of the cursor on the picture
        self.label.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        # Position the Label inside the window
        self.label.setGeometry(QtCore.QRect(2, 2, 400, 300))
        # Declare the QWebEngineView element to display the html page with the chat
        self.browser = QWebEngineView(self.centralwidget)
        # Declaring the QWebEngineView element to display YouTube videos, texts and web pages
        self.browser2 = QWebEngineView(self.centralwidget)
        # Position the QWebEngineView inside the window
        self.browser.setGeometry(QtCore.QRect(2, 305, 400, 300))
        self.browser2.setGeometry(QtCore.QRect(405, 2, 930, 603))

        # Load the html page with the chat into QWebEngineView
        global html_template
        global html_code
        global html_code_2

        html_result = html_template.replace('%code%', html_code)
        self.browser.setHtml(html_result, QtCore.QUrl("file://"))
        self.browser.show()
        self.browser2.setHtml(html_code_2, QtCore.QUrl("file://"))
        self.browser2.show()  
        self.label.setText("<center><img src='file:///"+os.getcwd()+"/img/img_greetings.jpg'></center>")

        # Connect signals and class functions
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

    # Handling a click on the image
    def eventFilter(self, obj, event):
        """

        :param obj:
        :param event:
        :return:
        """
        if event.type() == 2:
            btn = event.button()
            if btn == 1:
                listen_command()
            elif btn == 2:
                self.label.setText("<center><img src='file:///"+os.getcwd()+"/img/img_greetings.jpg'></center>")
        return super(QMainWindow, self).eventFilter(obj, event)

    # Смена картинки в зависимости от того слушает она или говорит
    def picture_change(self, data):
        """

        :param data:
        :return:
        """
        if data[0] == 1:
            # Ассистент слушает
            self.label.setText("<center><img src='file:///"+os.getcwd()+"/img/img_listen.jpg'></center>")
        if data[0] == 2:
            # Ассистент говорит
            self.label.setText("<center><img src='file:///"+os.getcwd()+"/img/img_greetings.jpg'></center>")

    # Добавление в html чат фразы ассистента
    def adding_response_to_chat_by_assistant(self, phrase):
        """

        :param phrase:
        :return:
        """
        global html_template
        global html_code
        html_code = '<div class="robot">' + phrase + '</div>' + html_code
        html_result = html_template.replace('%code%', html_code)
        self.browser.setHtml(html_result, QtCore.QUrl("file://"))
        self.browser.show()

    # Добавление в html чат фразы пользователя
    def adding_query_to_chat_by_user(self, phrase):
        """

        :param phrase:
        :return:
        """
        global html_template
        global html_code
        html_code = '<div class="you">' + phrase + '</div>' + html_code
        html_result = html_template.replace('%code%', html_code)
        self.browser.setHtml(html_result, QtCore.QUrl("file://"))
        self.browser.show()

    # Произносим ответ вслух синтезом речи
    @staticmethod
    def pronounce_assistant_answer(phrase):
        """

        :param phrase:
        :return:
        """
        global engine
        engine.say(phrase)
        engine.runAndWait()
        engine.stop()
 
    # Функция в которой решаем что отвечать на фразы пользователя    
    def response_to_user_request(self, data):
        """

        :param data:
        :return:
        """
        global p_urls
        global p_cmd
        # Получаем фразу от пользователя
        phrase = data[0].lower()
        # Отображаем её в чате
        self.adding_response_to_chat_by_assistant(phrase)
        # Ответ по умолчанию
        assistant_answer = 'Я не поняла запрос'
        try:
            # Выполняем разные действия в зависимости от наличия ключевых слов фо фразе
            if phrase == 'пока' or phrase == 'выход' or phrase == 'выйти' or phrase == 'до свидания':
                assistant_answer = 'Ещё увидимся!'
                self.adding_query_to_chat_by_user(assistant_answer)
                self.pronounce_assistant_answer(assistant_answer)
                sys.exit(app.exec_())
            elif 'анекдот' in phrase:
                assistant_answer = Assistant_functions.tell_joke()
            elif 'запусти' in phrase:
                assistant_answer = Assistant_functions.start_application(phrase)
            elif ((phrase.find("youtube") != -1) or (phrase.find("ютюб") != -1) or
                  (phrase.find("ютуб") != -1) or (phrase.find("you tube") != -1))\
                    and (phrase.find("смотреть") != -1):
                self.browser2.load(QtCore.QUrl(Assistant_functions.find_on_tube(phrase)))
                assistant_answer = 'Вот видео.'
            elif (phrase.find("слушать") != -1) and (phrase.find("песн") != -1):
                self.browser2.load(QtCore.QUrl(Assistant_functions.find_on_tube(phrase)))
                assistant_answer = 'Вот песня.'
            elif ((phrase.find("найти") != -1) or (phrase.find("найди") != -1)) \
                    and not(phrase.find("статью") != -1):
                user_request = Assistant_functions.clean_phrase(phrase, ['найти', 'найди', 'про', 'про то', 'о том'])
                question = Assistant_functions.browser_search(user_request)
                self.browser2.load(QtCore.QUrl(question[0]))
                assistant_answer = 'Ответ найден'
        except():
            # Если ключевых слов не нашли, используем Dialogflow
            assistant_answer = ai_message(phrase)
        # Добавляем ответ в чат
        self.adding_query_to_chat_by_user(assistant_answer)
        # Читаем ответ вслух
        self.pronounce_assistant_answer(assistant_answer)
        
    # Функция меняет картинку если ассистент тебя не расслышал
    def response_to_unrecognized_speech(self, data):
        """

        :param data:
        :return:
        """
        self.label.setText("<center><img src='file:///"+os.getcwd() +
                           "/img/img_response_to_unrecognized_speech.jpg'></center>")


# Запускаем программу на выполнение    
app = QApplication([])
window = ProgramWindow()
window.resize(1340, 615)    # Размер окна
window.show()
app.exec_()
