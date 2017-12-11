"""
    Don't mind me, just overdoing it with the APIs and trying
    to make a personal assistant. So far it speaks (still 
    need to learn how to speed it up), it searches keywords well,
    and can do basic computations. I'm considering adding in
    some default readouts to run the first time the computer is
    restarted after 8:00AM daily.
    
    Maybe I'll have a readout for tasks, calendar events, and
    the weather. Then it'll always be listening (wassup, Big Brother)
    
    I should probably include some real documentation....soon
    
"""
import keys
import wolframalpha, wikipedia
import pyowm
import win32com.client as wincl


class PersonalAssistant():
    def __init__(self):
        # print("Initializing Assistant...")
        self.dispatch, self.wa_client, self.owm = self.setup()
        self.dispatch.Speak('Hello, what can I do for you?')

    def setup(self):
        dispatch = wincl.Dispatch("SAPI.SpVoice")
        owm = pyowm.OWM(keys.OWM_key)
        wa_client = wolframalpha.Client(keys.wolfram_key)
        return dispatch, wa_client, owm

    def process_query(self, query):
        options = \
        {
            'weather': self.weather,
            'math': self.wolfram,
            'keywordsearch': self.wiki,
        }
        while query != 'quit':
            self.dispatch.Speak("Would you like to use Weather, Math, or Keyword Search?")
            try:
                options["".join(input("? ").lower().strip().split())](query)
            except KeyError:
                self.dispatch.Speak("Choice not recognized, defaulting to keyword search")
                self.wiki(query)
            self.dispatch.Speak("Any other questions?")
            query = input("Enter new query: ")

    def __del__(self):
        self.dispatch.Speak("Goodbye")

    def weather(self, location='Chicago,US'):
        while True:
            '''
            reg = self.owm.city_id_registry()
            if len(reg.locations_for(location[:location.find(',')])) > 1:
                self.dispatch.Speak("Please select one of the locations from the list below:")
                for location in reg.locations_for(location[:location.find(',')]):
                    print(location)
            '''
            obs = self.owm.weather_at_place(location)  # Toponym
            w = obs.get_weather()
            try:
                temp_f = w.get_temperature('fahrenheit')
                self.dispatch.Speak("It is {0} degrees in {1}"
                                    .format(temp_f['temp'], location[:location.find(',')]))
                break
            except pyowm.not_found_error.NotFoundError:
                self.dispatch.Speak("Sorry, this weather location is invalid. Please check your formatting")
                location = input("Please enter new weather locale or ID")

    def wolfram(self, equation="1 + 1"):
        res = self.wa_client.query(equation)
        answer = next(res.results).text
        self.dispatch.Speak("{0} is {1}".format(equation, answer))

    def wiki(self, topic="Macho Man Randy Savage"):
        while True:
            try:
                self.dispatch.Speak(wikipedia.summary(topic, sentences=2))
                break
            except wikipedia.exceptions.DisambiguationError as dis_err:
                self.dispatch.Speak("Looks like there's more than one option for this query, pick one from the menu")
                for option in dis_err.options:
                    print(option)
                spec_res = str(input("Specific Query: "))
                self.dispatch.Speak(wikipedia.summary(spec_res, sentences=2))
                break
            except wikipedia.exceptions.PageError as page_err:
                self.dispatch.Speak("Please form your question using keywords only")
                topic = input("Enter new keyword search: ")


def main():
    pa = PersonalAssistant()
    pa.process_query(input("Enter query: "))
    # pa.weather('Chicago,US')
    # pa.wolfram("100^10")
    # pa.wiki("French Revolution")


main()
