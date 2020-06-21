
from API.call_functions import *
import unittest 

class test_calls_class(unittest.TestCase):
    
    @classmethod
    def setUpClass(self):
        self.calls_object = calls()

    def test_calls_is_an_object(self):
        self.assertIsNotNone(self.calls_object)

    def test_calls_history_blank(self):
        # Check if dict contains more multiple countries by checking there exists many country keys in dict
        data = self.calls_object.historical()
        self.assertIs(type(data), type(''))
    
    def test_calls_history_with_arg(self):
        # Check if list contains one country by checking there exists many country keys in dict
        data = self.calls_object.historical(country = 'sweden')
       
        self.assertIs(type(data), type(''))
        self.assertIn('Sweden', data)
    
    def test_calls_all_works(self):
        # Check if the call methodfor all works by checking if the return is an dict object.
        data = self.calls_object.all()

        self.assertIs(type(data), type(''))

    def test_calls_countries_works(self):
        # Check if the call for countires works by check if the return is a list type object.
        data = self.calls_object.countries()

        self.assertIs(type(data), type(''))

    def test_calls_jhopkins(self): 

        data = self.calls_object.jhopkins()
        self.assertIs(type(data), type(''))


if __name__ == '__main__':
    unittest.main()