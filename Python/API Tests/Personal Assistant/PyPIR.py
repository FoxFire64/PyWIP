import keys, wolframalpha, wikipedia, pyowm
from twilio.rest import Client
from lookups import Lookups
import win32com.client
import speech_recognition as sr


class PyPIR():
    def __init__(self):
        # print("Initializing Assistant...")
        self.dispatch, self.wa_client, self.owm, self.r, self.twilio_client = self.setup()
        self.lookups = Lookups()
        # self.dispatch.Speak("Hello")

    def setup(self):
        dispatch = win32com.client.Dispatch("SAPI.SpVoice")
        owm = pyowm.OWM(keys.OWM_key)
        wa_client = wolframalpha.Client(keys.wolfram_key)
        r = sr.Recognizer()
        twilio_client = Client(keys.twilio_sid, keys.twilio_token)
        return dispatch, wa_client, owm, r, twilio_client

    def ms_handler(self):
        self.dispatch.Speak('What is your query?')
        query = self.get_speech().split()
        # query = "weather 60302".split()
        # query = 'call 7087458760'.split()
        while 'quit' not in query:
            query[:] = [x for x in query if x not in self.lookups.strike_dict]
            print(" ".join(query))
            for word in query:
                if word in self.lookups.keep_dict:
                    eval(self.lookups.keep_dict[word])(query)
                    break
            self.dispatch.Speak('Anything else?')
            query = self.get_speech().split()
            # query = ['quit']

    def __del__(self):
        self.dispatch.Speak("Goodbye")

    def get_speech(self):
        with sr.Microphone() as source:
            # self.r.adjust_for_ambient_noise(source)
            try:
                audio = self.r.listen(source)
                # return self.r.recognize_google(audio)
                res = self.r.recognize_google(audio)
                # print("response: {}".format(res))
                return res
            except sr.UnknownValueError:
                self.dispatch.Speak("I didn't understand what you said, could you say that again?")
                return self.get_speech()

    def call(self, outgoing):
        outgoing[:] = [x for x in outgoing if x not in self.lookups.keep_dict]
        # self.dispatch.Speak("Calling {}".format(outgoing[0]))
        call = self.twilio_client.calls.create(
            to="+1" + outgoing,
            from_="+13124677861",
            url="http://demo.twilio.com/docs/voice.xml"
        )
        import time
        time.sleep(10)

    def weather(self, location='New York'):
        '''
        search = ZipcodeSearchEngine()
        possible_locations = search.by_city(location)
        zipcode = possible_locations[0].Zipcode
        del possible_locations
        #print(zipcode)
        '''
        location[:] = [x for x in location if x not in self.lookups.keep_dict]
        if not location[0][0].isdigit():
            location = ','.join([' '.join(location), 'US'])
            obs = self.owm.weather_at_place(location)  # Toponym
        else:
            obs = self.owm.weather_at_zip_code(location[0], 'US')

        w = obs.get_weather()

        try:
            temp_f = w.get_temperature('fahrenheit')
            self.dispatch.Speak("It is {0} degrees in {1}".format(temp_f['temp'], location[:location.find(',')]))
        except pyowm.not_found_error.NotFoundError:
            self.dispatch.Speak("Sorry, this weather location is invalid.")
        '''
        reg = self.owm.city_id_registry()
        if len(reg.locations_for(location[:location.find(',')])) > 1:
            self.dispatch.Speak("Please select one of the locations from the list below:")
            for location in reg.locations_for(location[:location.find(',')]):
                print(location)
        '''

    def wolfram(self, equation="1 + 1"):
        math_strike = ['calculate', 'determine']
        equation[:] = [x for x in equation if x not in math_strike]  # only keep what isn't in the strike list
        print(equation)
        equation = ' '.join(equation)
        try:
            res = self.wa_client.query(equation)
            answer = next(res.results).text
            self.dispatch.Speak("{0} is {1}".format(equation, answer))
        except AttributeError:
            self.dispatch.Speak("Sorry, that\'s an invalid equation")

    def wiki(self, topic="Macho Man Randy Savage"):
        topic[:] = [x for x in topic if x not in self.lookups.keep_dict]  # only keep what isn't in the striking list

        try:
            self.dispatch.Speak(wikipedia.summary(topic, sentences=2))
        except wikipedia.exceptions.DisambiguationError as dis_err:
            self.dispatch.Speak("Looks like there's more than one option for this query, pulling the first result")
            '''
            for option in dis_err.options:
                print(option)
            spec_res = str(input("Specific Query: "))
            '''
            self.dispatch.Speak(wikipedia.summary(dis_err.options[0], sentences=1))
        except wikipedia.exceptions.PageError:
            self.dispatch.Speak("Please form your question using keywords only")
            print("Please form your question using keywords only")
            # except ValueError:
            #     self.dispatch.Speak("That value is not sufficient enough for a search")
            #     topic = self.get_speech()
            #     continue


def main():
    pypir = PyPIR()
    #pypir.ms_handler()
    # pypir.call(['call',"test"])
    # pypir.run()
    # pypir.weather('Salt Lake City')
    # pypir.wolfram(['1', 'divided by', 'divided by', '2'])
    # pypir.wiki("French Revolution")


if __name__ == '__main__':
    main()