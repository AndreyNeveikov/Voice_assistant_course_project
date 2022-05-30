# Interface
from PyQt5.QtWidgets import QLabel, QApplication, QMainWindow
from PyQt5.QtWebEngineWidgets import *
from PyQt5 import QtCore, QtGui
from PyQt5.QtGui import QIcon

# Functional
import speech_recognition as sr
import threading
import signal
import sys
import os

# Files
import Assistant_voice_output_settings
import Assistant_functions
import Assistant_database


# Get the html page for messages in the chat window
html_code = '<div class="robot">Чем я могу помочь?</div>'
file = open('chat.html', 'r', encoding='UTF-8')
html_chat = file.read()
file.close()

# Get the html page feature_list
file = open('feature_list.html', 'r', encoding='UTF-8')
feature_list_html = file.read()
file.close()


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
        self.setWindowIcon(QIcon("img\\app_icon.png"))
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
        self.label.setStyleSheet("QLabel { \n"
                                 "color: white;\n"
                                 "background-color: #6c0503;\n"
                                 "border: 1px solid #000000;\n"
                                 "border-radius: 0;\n"
                                 "}\n"
                                 "\n")
        # Declare the QWebEngineView element to display the html page with the chat
        self.browser = QWebEngineView(self.centralwidget)
        # Declaring the QWebEngineView element to display YouTube videos, texts and web pages
        self.browser2 = QWebEngineView(self.centralwidget)
        # Position the QWebEngineView inside the window
        self.browser.setGeometry(QtCore.QRect(2, 305, 400, 300))
        self.browser2.setGeometry(QtCore.QRect(405, 2, 930, 603))

        # Load the html page with the chat into QWebEngineView
        global html_chat
        global html_code
        global feature_list_html

        html_result = html_chat.replace('%code%', html_code)
        self.browser.setHtml(html_result, QtCore.QUrl("file://"))
        self.browser.show()
        self.browser2.setHtml(feature_list_html, QtCore.QUrl("file://"))
        self.browser2.show()
        self.label.setText("<center><img src='file:///"+os.getcwd() +
                           "/img/img_greetings.jpg'></center>")

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
        Function that handles clicks on an image

        :param obj: the object on which the action is performed
        :param event: type of event
        :return: changed object
        """
        if event.type() == 2:
            mouse_button = event.button()
            if mouse_button == 1:
                listen_command()

            elif mouse_button == 2:
                self.label.setText("<center><img src='file:///"+os.getcwd()+"/img/img_greetings.jpg'></center>")
                return_menu_html = open('feature_list.html', 'r', encoding='UTF-8')
                returned_feature_list_html = return_menu_html.read()
                self.browser2.setHtml(returned_feature_list_html, QtCore.QUrl("feature_list"))
                return_menu_html.close()

        return super(QMainWindow, self).eventFilter(obj, event)

    def picture_change(self, data):
        """
        Function of changing the picture depending on
        whether the assistant is listening or talking

        :param data: assistant mode
        :return: nothing, just change an image of the assistant's mode
        """
        if data[0] == 1:
            # Assistant listens
            self.label.setText("<center><img src='file:///" + os.getcwd() +
                               "/img/img_listen.jpg'></center>")
        if data[0] == 2:
            # Assistant speaks
            self.label.setText("<center><img src='file:///" + os.getcwd() +
                               "/img/img_greetings.jpg'></center>")

    def adding_response_to_chat_by_assistant(self, phrase):
        """
        Adding an assistant's phrase to the html chat

        :param phrase: assistant answer
        :return: nothing, writes assistant answer in the html chat
        """
        global html_chat
        global html_code
        html_code = '<div class="robot">' + phrase + '</div>' + html_code
        html_result = html_chat.replace('%code%', html_code)
        self.browser.setHtml(html_result, QtCore.QUrl("file://"))
        self.browser.show()

    def adding_query_to_chat_by_user(self, phrase):
        """
        Adding a user phrase to the html chat

        :param phrase: assistant request
        :return: nothing, writes user request in the html chat
        """
        global html_chat
        global html_code
        html_code = '<div class="you">' + phrase + '</div>' + html_code
        html_result = html_chat.replace('%code%', html_code)
        self.browser.setHtml(html_result, QtCore.QUrl("file://"))
        self.browser.show()

    @staticmethod
    def pronounce_assistant_answer(phrase):
        """
        Redirects a phrase to the voiceover function

        :param phrase: written phrase
        :return: nothing
        """
        speaker_list = ['aidar', 'baya', 'kseniya', 'xenia', 'random']

        Assistant_voice_output_settings.Speaker(speaker_list[3]).pronounce_assistant_answer(phrase)

    def response_to_user_request(self, data):
        """
        Answer by selection function

        :param data: list of keywords
        :return: assistant answer
        """
        global p_urls
        global p_cmd

        phrase = data[0].lower()    # Get phrase from user
        self.adding_response_to_chat_by_assistant(phrase)   # Display the user's phrases in the chat
        assistant_answer = 'Я не поняла запрос'    # Default response

        try:
            # Perform an action depending on the presence of keywords in the phrase
            if 'ответь' in phrase:
                assistant_answer = Assistant_functions.assistant_answering_dialogue_phrase(phrase)

            elif ((phrase.find("база") != -1) and (phrase.find("данных") != -1)) \
                    or (((phrase.find("пароль") != -1) or (phrase.find("логин") != -1))
                        or ((phrase.find("добавить") != -1) and (phrase.find("данные") != -1))
                        or ((phrase.find("записать") != -1) and (phrase.find("данные") != -1)
                            and (phrase.find("сайта") != -1))):
                assistant_answer = Assistant_database.DatabaseFunctionSelector().selecting_database_function(phrase)

            elif (phrase.find("запустить") != -1) or (phrase.find("запусти") != -1):
                assistant_answer = Assistant_functions.start_application(phrase)

            elif ((phrase.find("youtube") != -1) or (phrase.find("ютюб") != -1) or
                  (phrase.find("ютуб") != -1) or (phrase.find("you tube") != -1))\
                    and (phrase.find("смотреть") != -1):
                self.browser2.load(QtCore.QUrl(Assistant_functions.find_on_you_tube(phrase)))
                assistant_answer = 'Вот видео.'

            elif ((phrase.find("анекдот") != -1) or (phrase.find("шутка") != -1) or
                  (phrase.find("анек") != -1) or (phrase.find("прикол") != -1))\
                    or (phrase.find("смешной") != -1):
                assistant_answer = Assistant_functions.tell_joke()

            elif (phrase.find("слушать") != -1) and ((phrase.find("песн") != -1) or (phrase.find("песню") != -1)):
                self.browser2.load(QtCore.QUrl(Assistant_functions.find_on_you_tube(phrase)))
                assistant_answer = 'Вот песня.'

            elif ((phrase.find("найти") != -1) or (phrase.find("найди") != -1)) \
                    and not(phrase.find("статью") != -1):
                user_request = Assistant_functions.clean_phrase(phrase,
                                                                ['найти', 'найди', 'про', 'про то', 'о том'])
                question = Assistant_functions.browser_search(user_request)
                self.browser2.load(QtCore.QUrl(question[0]))
                assistant_answer = 'Ответ найден'

            elif phrase == 'пока' or phrase == 'выход' or phrase == 'выйти' or phrase == 'до свидания':
                assistant_answer = 'Ещё увидимся!'
                self.adding_query_to_chat_by_user(assistant_answer)
                self.pronounce_assistant_answer(assistant_answer)
                sys.exit(app.exec_())

        except():
            assistant_answer = 'Я не поняла запрос'    # Default response

        self.adding_query_to_chat_by_user(assistant_answer)    # Add response to the chat
        self.pronounce_assistant_answer(assistant_answer)    # Speak out the answer

    def response_to_unrecognized_speech(self, *args):
        """
        Function that changes the picture if the assistant did not hear you

        :param args: QtCore.Qt.QueuedConnection
        :return: nothing, just change the picture
        """
        self.label.setText("<center><img src='file:///"+os.getcwd() +
                           "/img/img_response_to_unrecognized_speech.jpg'></center>")


# Run the program
app = QApplication([])
window = ProgramWindow()

window.resize(1340, 615)    # Window size
window.show()
app.exec_()
