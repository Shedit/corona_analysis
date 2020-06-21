from cleaning_functions import *
from API.call_functions import *
import pandas as pd
import unittest 
import pprint as pp
class test_generate_plot_data(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        self.calls_object = calls()
        print('setUpClass called')
   # BUG: Change in historical JSN struct where all provinces are called with province extention. 
    def setUp(self): 
        self.data = self.calls_object.historical()
        #self.data_ca = self.calls_object.historical('canada')
        self.data = pd.DataFrame(self.data)
        #self.data_ca = pd.DataFrame(self.data_ca)
        print("setUp called")
    
    def test_column_merge_country_province(self):

        data = column_merge_country_province(self.data)
        self.assertIn("countryANDprovince", list(data.columns))
        self.assertGreaterEqual(len(data.index), 2)


if __name__ == '__main__':
    unittest.main()