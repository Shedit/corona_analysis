from API.call_functions import *
from graph_functions import *
from cleaning_functions import *
import pandas as pd
import numpy as np



API = calls()

data_hist_json = API.historical()

df_hist = pd.read_json(data_hist_json)

df_hist = tidy_historical(data)



