from API.call_functions import * 
import datetime as dt
import time

class updater(object):

    def __init__(self):
        self.call = calls() 
        self.hist = self.call.historical()
        self.jhop = self.call.jhopkins()
        self.lastupdated = dt.datetime.today()

    def __call__(self): 
        if (dt.datetime.today() - self.lastupdated  >= dt.timedelta(days=1)):
            print('Updater updated! Difference is {}'.format(dt.datetime.today() - self.lastupdated))
            self.hist = self.call.historical()
            self.jhop = self.call.jhopkins()
            self.lastupdated = dt.datetime.today()
        else:
            print('Updater not updated! Difference is only {}'.format(dt.datetime.today() - self.lastupdated))
            pass
    
update = updater()

while True:
    time.sleep(5)
    update()

    
