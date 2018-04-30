"""PyPIR: Personal Inquiry Resolver Source

    Author : Armani Akines\n
    Purpose : Concordia University Chicago Capstone\n
    Date : 04/29/18\n
"""

import random
import time

import pyowm
import pyttsx3
import speech_recognition as sr
import wikipedia
import wolframalpha
# import tweepy
from twilio.rest import Client

"""Local Imports"""
import gmaps_directions
import keys
import responses
from lookups import Lookups


class PyPIR():
    """Initializes PyPIR Assistant


    Attributes:

    _owm_key : str
        OpenWeatherMap API Key
    _wa_key : str
        WolframAlpha API Key
    _twilio_sid : str
        Twilio API SID
    _twilio_token : str
        Twilio API Token

    speech_engine : object
        PyTTSX3 Speech Engine
    wa_client : object
        WolframAlpha Client Object
    owm_client : object
        PyOpenWeatherMap Client Object
    sr_client : object
        SpeechRecognition Client Object
    twilio_client : object
        Twilio Client Object

    lookups : object
        Trigger Word Lookup Object
    \n\n
    """

    def __init__(self):
        """PyPIR Constructor.

        Sets up class attributes, API Keys, API Clients, Speech Engines (speech output), and
        the Microphone (speech input)
        """
        self._owm_key, self._wa_key, self._twilio_sid, self._twilio_token = (
            None,) * 4
        self.speech_engine, self.wa_client, self.owm_client, self.sr_client, self.twilio_client, = (
            None,) * 5
        self.setup_keys()
        self.setup_clients()
        self.start_engines()
        self.lookups = Lookups()
        with sr.Microphone() as self.source:
            self.speak("Hello! " + responses.help_responses[0])
            self.ms_handler()

    def __del__(self):
        """PyPIR Destructor"""
        self.speak("Goodbye")

    @property
    def owm_key(self):
        """OpenWeatherMap API Key"""
        return self._owm_key

    @property
    def wa_key(self):
        """WolframAlpha API Key"""
        return self._wa_key

    @property
    def twilio_sid(self):
        """Twilio SID"""
        return self._twilio_sid

    @property
    def twilio_token(self):
        """Twilio Token"""
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

    def timeit(self):
        """[DEV-ONLY] Timing testing decorator."""

        def timed(*args, **kw):
            """[DEV-ONLY] Determine time taken for each method"""
            ts = time.time()
            result = self(*args, **kw)
            te = time.time()

            # Print time taken, name of method, and args
            print(
                "{0!r} ({1!r}, {2!r}) {3:2.4f} sec".format(
                    self.__name__, args, kw, te - ts))
            return result

        return timed

    # @timeit
    def setup_keys(self):
        """Initializes API keys from keys.py helper module"""
        self._wa_key = keys.wolfram_key
        self._owm_key = keys.owm_key
        self._twilio_sid = keys.twilio_sid
        self._twilio_token = keys.twilio_token

    # @timeit
    def setup_clients(self):
        """Initializes API clients using initialized keys"""
        self.wa_client = wolframalpha.Client(self._wa_key)
        self.owm_client = pyowm.OWM(self._owm_key)
        self.sr_client = sr.Recognizer()
        self.twilio_client = Client(self._twilio_sid, self._twilio_token)

    # @timeit
    def start_engines(self):
        """Initializes PyTextToSpeech3 Engine for speech output"""

        # Initialize pyttsx3 engine
        speech_engine = pyttsx3.init()
        # Set voice to Tessa (slow, clear annunciation of Female Voice)
        speech_engine.setProperty(
            'voice', 'com.apple.speech.synthesis.voice.tessa')
        # Set class member for ease of access
        self.speech_engine = speech_engine

    # @timeit
    def speak(self, phrase):
        """Blocks thread to allow for phrase to be spoken.

        phrase : str, default=N/A
            Phrase to be spoken
        """

        # Queue phrase in engine
        self.speech_engine.say(phrase)
        # Block thread and output phrase
        self.speech_engine.runAndWait()

    # @timeit
    def ms_handler(self):
        """Pick which class method to execute query with, sentinel = quit

        Prompt user for query, get user input, strip input of non-meaningful
        or non-trigger words, and determine which class method to use for
        query execution
        """

        # Trigger word found
        istriggered = bool

        # Gather input, strip input, determine method
        self.speak('What is your query?')
        while True:
            query = self.get_speech().split()
            # Remove non-meaningful words
            query[:] = [x for x in query if x not in self.lookups.strike_dict]

            for word in query:
                if word in self.lookups.get_quit_lookup():
                    return None
                if word in self.lookups.get_help_lookup():
                    self.help(query)
                    istriggered = True
                    break
                if word in self.lookups.keep_dict and len(query) > 1:
                    istriggered = True
                    eval(self.lookups.keep_dict[word])(query)
                    break
                else:
                    istriggered = False
            # If query lacked triggers/meaning, ask for more information
            self.speak(
                'Anything else?' if istriggered else 'I\'ll need a little more information')

    # @timeit
    def get_speech(self):
        """Get speech from user, return result"""

        while True:
            # Enable the below line for ambient noise reduction. Slows function down
            # But allows PyPIR to hear better in loud rooms.
            # self.sr_client.adjust_for_ambient_noise()
            try:
                audio = self.sr_client.listen(self.source)
                res = self.sr_client.recognize_google(audio)
            except sr.UnknownValueError:
                self.speak(
                    "I didn't understand what you said, could you say that again?")
                continue
            return res

    # @timeit
    def call(self, outgoing=None):
        """Place call using Twilio API to phone number.

        Sets Twilio client up to make outgoing call from Twilio Number to
        outgoing number. Currently set up for Domestic US Numbers.


        outgoing : list(string), default=None
            The outgoing phone number Twilio will use.
        """

        if outgoing is None:
            outgoing = ['call', "7087458760"]
        outgoing[:] = [x for x in outgoing if x not in self.lookups.keep_dict]
        self.speak("Calling {}".format(outgoing[0]))
        call = self.twilio_client.calls.create(
            to="+1" + outgoing[0],
            from_="+17734232950",
            url="http://demo.twilio.com/docs/voice.xml"
        )

    # @timeit
    def directions(self, finish=None):
        """Get directions to finish location. Output answers incrementally.

        Prompts for user location, and utilizes GoogleMaps API to get
        directions. PyPIR then speaks each direction one-by-one until user
        stops her.


        finish : list(string), default=None
            The finish location; the destination
        """

        if finish is None:
            finish = ['directions', 'to', 'Wheaton', 'Metra', 'Station']

        self.speak("What is your current location?")
        curr_loc = self.get_speech()

        # Access gmaps_directions for routing results
        gmaps_dirs = gmaps_directions.Directions(curr_loc, finish)
        dirs_list = gmaps_dirs.get_directions()

        # List each direction, ask for user continuation
        for direction in dirs_list:
            self.speak(direction)
            self.speak("Should I continue?")
            if self.get_speech() in [
                'yes',
                'Yes',
                'sure',
                'Sure',
                'Okay',
                'okay',
                'ok',
                    'Ok']:
                continue
            else:
                return None

    # @timeit
    def help(self, words):
        """Speak help commands to user

        words : list(string), default=None
            [unused]
        """

        self.speak(random.choice(responses.help_responses))

    # @timeit
    def weather(self, location=None):
        """Say weather in specific location.

        Queries location in PyOpenWeatherMap, then pulls in first reliable
        Toponym and speaks weather in that area

        location : list(string), default=None
            US-Based location for weather lookup
        """

        if location is None:
            location = ['weather', 'New', 'York']

        # Strip trigger words, concatenate location to US toponym, speak
        # Result if there is one.
        location[:] = [x for x in location if x not in self.lookups.keep_dict]
        try:
            if location[0].isdigit():
                obs = self.owm_client.weather_at_zip_code(location[0], 'US')
            else:
                location = ','.join([' '.join(location), 'US'])
                obs = self.owm_client.weather_at_place(location)  # Toponym

            w = obs.get_weather()
            temp_f = w.get_temperature('fahrenheit')
            if ',' in location:
                self.speak("It is {0} degrees in {1}".format(
                    temp_f['temp'], location[:location.find(',')]))
            else:
                self.speak(
                    "It is {0} degrees in {1}".format(
                        temp_f['temp'], location[0]))
        # This exception both does and does not exist, according to source
        except pyowm.exceptions.not_found_error.NotFoundError:
            self.speak("Sorry, this weather location is invalid.")

    # @timeit
    def wolfram(self, equation=None):
        """Say result of math equation.

        Takes in user input, processes through WolframAlpha API, and speaks
        the result.

        equation : list(str), default=None
            Equation to process
        """

        if equation is None:
            equation = ['1', 'plus', '1']
        math_strike = ['calculate', 'determine']
        # Only keep what isn't in the math strike list
        equation[:] = [x for x in equation if x not in math_strike]
        equation = ' '.join(equation)
        try:
            res = self.wa_client.query(equation)
            answer = next(res.results).text
            self.speak("{0} is {1}".format(equation, answer))
        except AttributeError:
            self.speak("Sorry, that\'s an invalid equation")

    # @timeit
    def wiki(self, topic=None):
        """Speak result of Wikipedia topic search.

        Processes topic through Wikipedia API to return results. If more than one possible
        result, processes the first result. If search is insufficient, returns handled
        exception.

        topic : list(str)
            Keyword topic to search
        """

        if topic is None:
            topic = ["search", "Alexander", "Hamilton"]
        # only keep what isn't in the striking list
        topic[:] = [x for x in topic if x not in self.lookups.keep_dict]
        topic = " ".join(topic)
        try:
            self.speak(wikipedia.summary(topic, sentences=2))
        except wikipedia.exceptions.DisambiguationError as dis_err:
            self.speak(
                "Looks like there's more than one option for this query, pulling the first result")
            self.speak(wikipedia.summary(dis_err.options[0], sentences=1))
        except wikipedia.exceptions.PageError:
            self.speak("Please form your question using keywords only")
        except ValueError:
            self.speak("That value is not sufficient enough for a search")

    # @timeit
    def quit_pypir(self, words):  # do not remove 'words', unless you like IndexErrors
        """Processes exit functionality for PyPIR Assistant

        words : list(str)
            [unused]
        """

        # Call destructor
        self.__del__()


def main():
    """PyPIR Driver Line

    Instantiates PyPIR Object
    """
    PyPIR()


if __name__ == '__main__':
    main()
