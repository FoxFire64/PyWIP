# import win32com.client
import random

import pyowm
import pyttsx3
import speech_recognition as sr
import wikipedia
import wolframalpha
from twilio.rest import Client

'''local imports'''
import keys
import responses
from lookups import Lookups


class PyPIR():
    def __init__(self):
        # print("Initializing Assistant...")
        self._owm_key, self._wa_key, self._twilio_sid, self._twilio_token = (None,) * 4
        self.speech_engine, self.wa_client, self.owm_client, self.sr_client, self.twilio_client = (None,) * 5
        self.setup_keys()
        self.setup_clients()
        self.start_engine()
        self.lookups = Lookups()
        self.speak("Hello")
        self.speak(responses.help_responses[0])
        # print("Hello")
        self.ms_handler()

    def __del__(self):
        self.speak("Goodbye")
        # print("Goodbye")

    @property
    def owm_key(self):
        return self._owm_key

    @property
    def wa_key(self):
        return self._wa_key

    @property
    def twilio_sid(self):
        return self._twilio_sid

    @property
    def twilio_token(self):
        return self._twilio_token

    @owm_key.setter
    def owm_key(self, key):
        self._owm_key = key

    @wa_key.setter
    def wa_key(self, key):
        self._wa_key = key

    @twilio_sid.setter
    def twilio_sid(self, sid):
        self._twilio_sid = sid

    @twilio_token.setter
    def twilio_token(self, token):
        self._twilio_token = token

    def setup_keys(self):
        self._wa_key = keys.wolfram_key
        self._owm_key = keys.owm_key
        self._twilio_sid = keys.twilio_sid
        self._twilio_token = keys.twilio_token

    def setup_clients(self):
        self.wa_client = wolframalpha.Client(self.wa_key)
        self.owm_client = pyowm.OWM(self.owm_key)
        self.sr_client = sr.Recognizer()
        self.twilio_client = Client(self.twilio_sid, self.twilio_token)

    def start_engine(self):
        speech_engine = pyttsx3.init()
        rate = speech_engine.getProperty('rate')
        speech_engine.setProperty('voice', 'com.apple.speech.synthesis.voice.tessa')
        self.speech_engine = speech_engine

    def speak(self, phrase):
        self.speech_engine.say(phrase)
        self.speech_engine.runAndWait()

    def ms_handler(self):
        self.speak('What is your query?')
        # print("What is your query?")
        query = self.get_speech().split()
        while True:
            query[:] = [x for x in query if x not in self.lookups.strike_dict]
            # print(" ".join(query))
            for word in query:
                if word in self.lookups.keep_dict and len(query) > 1:
                    eval(self.lookups.keep_dict[word])(query)
                    break

            self.speak('Anything else?')
            # print('Anything else?')
            query = self.get_speech().split()

    def get_speech(self):
        with sr.Microphone() as source:
            #self.sr_client.adjust_for_ambient_noise(source)
            try:
                audio = self.sr_client.listen(source)
                # return self.sr_client.recognize_google(audio)
                res = self.sr_client.recognize_google(audio)
                # # print("response: {}".format(res))
                return res
            except sr.UnknownValueError:
                self.speak("I didn't understand what you said, could you say that again?")
                # print("I didn't understand what you said, could you say that again?")
                return self.get_speech()

    def call(self, outgoing=None):
        if outgoing is None:
            outgoing = ['call', "7087458760"]
        outgoing[:] = [x for x in outgoing if x not in self.lookups.keep_dict]
        self.speak("Calling {}".format(outgoing[0]))
        # print("Calling {}".format(outgoing[0]))
        call = self.twilio_client.calls.create(
            to="+1" + outgoing[0],
            from_="+17734232950",
            url="http://demo.twilio.com/docs/voice.xml"
        )

    def help(self, words):
        self.speak(random.choice(responses.help_responses))

    def weather(self, location=None):
        if location is None:
            location = ['weather', 'New', 'York']
        location[:] = [x for x in location if x not in self.lookups.keep_dict]
        try:
            if not location[0].isdigit():
                location = ','.join([' '.join(location), 'US'])
                obs = self.owm_client.weather_at_place(location)  # Toponym
            else:
                obs = self.owm_client.weather_at_zip_code(location[0], 'US')

            w = obs.get_weather()
            temp_f = w.get_temperature('fahrenheit')
            if ',' in location:
                self.speak("It is {0} degrees in {1}".format(temp_f['temp'], location[:location.find(',')]))
                # print("It is {0} degrees in {1}".format(temp_f['temp'], location[:location.find(',')]))
            else:
                self.speak("It is {0} degrees in {1}".format(temp_f['temp'], location[0]))
                # print("It is {0} degrees in {1}".format(temp_f['temp'], location[0]))
        except pyowm.exceptions.not_found_error.NotFoundError:
            # print("Sorry, this weather location is invalid.")
            self.speak("Sorry, this weather location is invalid.")

    def wolfram(self, equation=None):
        if equation is None:
            equation = ['1', 'plus', '1']
        math_strike = ['calculate', 'determine']
        equation[:] = [x for x in equation if x not in math_strike]  # only keep what isn't in the strike list
        equation = ' '.join(equation)
        # print(equation)
        try:
            res = self.wa_client.query(equation)
            answer = next(res.results).text
            self.speak("{0} is {1}".format(equation, answer))
            # print("{0} is {1}".format(equation, answer))
        except AttributeError:
            self.speak("Sorry, that\'s an invalid equation")
            # print("Sorry, that\'s an invalid equation")

    def wiki(self, topic=None):
        if topic is None:
            topic = ["search", "Alexander", "Hamilton"]
        topic[:] = [x for x in topic if x not in self.lookups.keep_dict]  # only keep what isn't in the striking list
        topic = " ".join(topic)
        try:
            # print(wikipedia.summary(topic, sentences=2))
            self.speak(wikipedia.summary(topic, sentences=2))
        except wikipedia.exceptions.DisambiguationError as dis_err:
            # print("Looks like there's more than one option for this query, pulling the first result")
            self.speak("Looks like there's more than one option for this query, pulling the first result")
            self.speak(wikipedia.summary(dis_err.options[0], sentences=1))
            # print(wikipedia.summary(dis_err.options[0], sentences=2))
        except wikipedia.exceptions.PageError:
            self.speak("Please form your question using keywords only")
            # print("Please form your question using keywords only")
        # except ValueError:
        #     self.speak("That value is not sufficient enough for a search")
        #     # print("That value is not sufficient enough for a search")

    def quit_pypir(self, words):  # do not remove 'words', unless you like IndexErrors
        self.__del__()


def main():
    PyPIR()
    # pypir.ms_handler()
    # pypir.call(['call',"7087458760"])
    # pypir.weather(['weather', 'Kansas City'])
    # pypir.wolfram(['1', 'divided by', '2'])
    # pypir.wiki(["search", "Alexander", "Hamilton"])


if __name__ == '__main__':
    main()
