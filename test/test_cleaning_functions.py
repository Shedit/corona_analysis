from cleaning_functions import *
from API.call_functions import *
import pandas as pd
import unittest 

class test_generate_plot_data(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        self.calls_object = calls()
        print('setUpClass called')
    
    def setUp(self): 
        self.data = self.calls_object.historical()
        self.data_ca = self.calls_object.historical('canada')

        self.data = pd.read_json(self.data)
        self.data_ca = pd.read_json(self.data_ca)
        print("setUp called")

    def test_output_historical_is_cleaned(self): 

        data = generate_plot_data(self.data)

        self.assertIn(['variable', 'value'], list(data.columns))
    
    def test_output_historical_with_selected_country_is_cleaned(self):

        data = generate_plot_data(self.data_ca)

        self.assertIn(['variable', 'value'], list(data.columns))
    
    def test_dependent_function_column_merge_country_province(self):

        data = column_merge_country_province(self.data)

        self.assertEqual(2, len(list(data.columns)))
        self.assertIn("countryANDprovince", list(data.columns))
        self.assertGreaterEqual(len(data.index), 2)
    
    def test_dependent_function_convert_timeline_to_dataframe_ALL(self):
    
        data = column_merge_country_province(self.data)

        data = convert_timeline_to_dataframes_ALL(data)
        
        self.assertEqual(type(data['timeline'][0]), type(pd.DataFrame()))

    def test_dependent_function_convert_timeline_to_dataframe_SINGLE(self):
        
        data_ca = convert_timeline_to_dataframes_SINGLE(self.data_ca)
        
        self.assertEqual(['cases', 'deaths'], list(data_ca['index']))
        self.assertEqual([0,1], list(data_ca.index))

    def test_dependent_function_melt_country_province(self):

        data = column_merge_country_province(self.data)
        data = convert_timeline_to_dataframes_ALL(data)
        data = melt_country_province(data)

        self.assertIn(['variable, value, countrySegment'], list(data.columns))

if __name__ == '__main__':
    unittest.main()