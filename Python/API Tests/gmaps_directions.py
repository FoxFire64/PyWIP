"""Google Maps Direction Calculator for PyPIR

    Author : Armani Akines\n
    Purpose : Concordia University Chicago Capstone\n
    Date : 04/29/18\n
"""
import json
import urllib
from html.parser import HTMLParser

import lookups


class Directions():
    """Initializes Directions Calculator


    Attributes:

    curr_loc : str
        Current location
    finish : str
        Destination location
    \n\n
    """

    def __init__(self, curr_loc=None, finish=None):
        """Directions Calculator Constructor

        Initializes Directions attributes
        """
        if curr_loc is None:
            curr_loc = ['Concordia', 'Univeristy', 'Chicago']
        if finish is None:
            finish = ['directions', 'wheaton', 'metra', 'station']
        self.curr_loc = curr_loc
        self.finish = self.get_finish(finish)

    def get_finish(self, finish):
        """Get finish destination from user.

        finish : str
            finish destination
                """
        finish[:] = [x for x in finish if x not in lookups.Lookups().keep_dict]
        return ' '.join(finish)

    def get_directions(self):
        """Get directions to location from Google Maps


        Sends API request to Google Maps, parses response, strips tags,
        and returns results as a list
        """

        # Form API Request
        url = 'http://maps.googleapis.com/maps/api/directions/json?%s' % urllib.parse.urlencode((
            ('origin', self.curr_loc),
            ('destination', self.finish)
        ))

        class MLStripper(HTMLParser):
            """Markup Language Stripper

            Takes in string and removes HTML tags
            """
            def __init__(self):
                """Markup Language Stripper Constructor"""

                # Call HTMLParser Initializer
                super().__init__()
                self.reset()
                self.strict = False
                self.convert_charrefs = True
                self.fed = []

            def handle_data(self, d):
                """Append data d to results"""
                self.fed.append(d)

            def get_data(self):
                """Get/Set data for stripping"""
                return ''.join(self.fed)

        print(url)
        ur = urllib.request.urlopen(url)
        result = json.load(ur)
        directions = []

        # Takes in specific JSON attributes for the directions and strips them
        # Then appends them to the directions dictionary for returning
        for i in range(0, len(result['routes'][0]['legs'][0]['steps'])):
            jres = result['routes'][0]['legs'][0]['steps'][i]['html_instructions']
            s = MLStripper()
            s.feed(jres)
            jres = s.get_data()
            directions.append(jres)
            print(jres)

        return directions


if __name__ == '__main__':
    """Driver"""
    dirs = Directions()
    print(dirs.get_directions())
