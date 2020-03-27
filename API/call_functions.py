import requests 
import os


class calls():

    def __init__(self):
        self.URL = "https://corona.lmao.ninja/v2"

    def historical(self, country = ''):
        URL = os.path.join(self.URL, "historical")
        
        if country == '':  
            r = requests.get(url = URL)
            return r.text

        else:
            # Because params in r.get delimit with '?' instead and REST api does not accept '?' only '/'
            PATH = os.path.join (URL, country)
            r = requests.get(url = PATH)
            return r.text

    def all(self):

        URL = self.URL + "/all"
        r = requests.get(url = URL)
        return r.text

    def countries(self):

        URL = self.URL + "/countries"
        r = requests.get(url = URL)
        return r.text
        
