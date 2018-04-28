class Lookups():
    def __init__(self):
        self.keep_dict = dict.fromkeys(self.get_quit_lookup(), 'self.quit')
        self.keep_dict.update(dict.fromkeys(self.get_weather_lookup(), 'self.weather'))
        self.keep_dict.update(dict.fromkeys(self.get_math_lookup(), 'self.wolfram'))
        self.keep_dict.update(dict.fromkeys(self.get_twitter_lookup(), 'self.tweet'))
        self.keep_dict.update(dict.fromkeys(self.get_calendar_lookup(), 'self.calendar'))
        self.keep_dict.update(dict.fromkeys(self.get_search_lookup(), 'self.wiki'))
        self.keep_dict.update(dict.fromkeys(self.get_call_lookup(), 'self.call'))

        self.strike_dict = self.get_strike_lookup()

    def get_quit_lookup(self):
        quit_lookup = ['quit', 'exit', 'terminate', 'go home', 'end']
        return quit_lookup

    def get_weather_lookup(self):
        weather_lookup = ['weather', 'temperature', 'climate']
        return weather_lookup

    def get_math_lookup(self):
        math_lookup = ['calculate', 'plus', 'minus', 'divided', 'multiply', 'multiplied', 'times', '+', '-', '*', '/', 'of', 'determine']
        return math_lookup

    def get_twitter_lookup(self):
        tweet_lookup = ['tweet', 'tweets', 'twitter', 'handle', 'send a tweet']
        return tweet_lookup

    def get_calendar_lookup(self):
        calendar_lookup = ['date', 'calendar']
        return calendar_lookup

    def get_search_lookup(self):
        search_lookup = ['search', 'find', 'tell me', 'look up', 'who', 'when', 'where']
        return search_lookup

    def get_call_lookup(self):
        call_lookup = ['call', 'phone', 'call up', 'ring']
        return call_lookup

    def get_strike_lookup(self):
        strike_lookup = ['what', 'what\'s', 'is', 'the', 'in', 'a', 'an', 'like', 'yes', 'no', 'can', 'now']
        return strike_lookup