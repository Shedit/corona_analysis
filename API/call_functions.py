import requests 
import os


class calls():

    def __init__(self):
        self.URL = "https://corona.lmao.ninja/v2"
        self.URL_v1 = "https://corona.lmao.ninja"

    def historical(self, country = '', lastdays = 'all'):
        URL = os.path.join(self.URL, "historical")
        
        if country == '':  
            r = requests.get(url = URL, params = {'lastdays': str(lastdays)})
            return r.text

        else:
            # Because params in r.get delimit with '?' instead and REST api does not accept '?' only '/'
            PATH = os.path.join (URL, country)
            r = requests.get(url = PATH, params={'lastdays': str(lastdays)})
            print('historical:' + r.url)
            return r.text

    def all(self):

        URL = self.URL_v1 + "/all"
        r = requests.get(url = URL)
        return r.json()

    def countries(self):

        URL = self.URL + "/countries"
        r = requests.get(url = URL)
        return r.text

    def jhopkins(self): 

        URL = self.URL + "/jhucsse"
        r = requests.get( url = URL)
        return r.text
