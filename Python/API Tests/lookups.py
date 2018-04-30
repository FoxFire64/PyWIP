"""Trigger Dictionary for PyPIR

    Author : Armani Akines\n
    Purpose : Concordia University Chicago Capstone\n
    Date : 04/29/18\n
"""

class Lookups():
    """Trigger Dictionary Class.

    Creates and iterates through lookup dictionaries to find trigger words

    keep_dict : dict
        Dictionary of trigger words and their mappings of PyPIR functions
    strike_dict : dict
        Dictionary of meaningless words to be taken out of a general query
    """

    def __init__(self):
        """Lookups Constructor

        Initializes and concatenates lookup tables"""
        self.keep_dict = dict.fromkeys(
            self.get_weather_lookup(), 'self.weather')
        self.keep_dict.update(
            dict.fromkeys(
                self.get_math_lookup(),
                'self.wolfram'))
        self.keep_dict.update(
            dict.fromkeys(
                self.get_directions_lookup(),
                'self.directions'))
        self.keep_dict.update(
            dict.fromkeys(
                self.get_search_lookup(),
                'self.wiki'))
        self.keep_dict.update(
            dict.fromkeys(
                self.get_call_lookup(),
                'self.call'))

        self.strike_dict = self.get_strike_lookup()

    def get_quit_lookup(self):
        quit_lookup = ['quit', 'exit', 'terminate', 'end']
        return quit_lookup

    def get_weather_lookup(self):
        weather_lookup = ['weather', 'temperature', 'climate']
        return weather_lookup

    def get_math_lookup(self):
        math_lookup = [
            'calculate',
            'plus',
            'minus',
            'divided',
            'multiply',
            'multiplied',
            'times',
            '+',
            '-',
            '*',
            '/',
            'of',
            'determine']
        return math_lookup

    def get_directions_lookup(self):
        directions_lookup = ['direction', 'directions', 'map', 'guide']
        return directions_lookup

    def get_search_lookup(self):
        search_lookup = ['search', 'find', 'lookup', 'who', 'when', 'where']
        return search_lookup

    def get_call_lookup(self):
        call_lookup = ['call', 'phone', 'ring']
        return call_lookup

    def get_strike_lookup(self):
        strike_lookup = [
            'what',
            'what\'s',
            'is',
            'the',
            'in',
            'a',
            'an',
            'like',
            'yes',
            'no',
            'can',
            'now',
            'to']
        return strike_lookup

    def get_help_lookup(self):
        help_lookup = ['help', 'tutorial', 'walkthrough']
        return help_lookup
