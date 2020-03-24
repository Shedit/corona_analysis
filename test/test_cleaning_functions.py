from cleaning_functions import *
from API.call_functions import *
import unittest 

class test_get_timelines_as_list(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        self.calls_object = calls()

    def test_output_is_list(self): 
        data = self.calls_object.historical()
        
        
    
if __name__ == '__main__':
    unittest.main()