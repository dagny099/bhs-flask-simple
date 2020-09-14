from pandas_datareader import data, wb
import pandas as pd
import numpy as np
import datetime

startDate = "Jan, 1, 2006"
endDate = "Jan, 1, 2016"
 
BAC = data.DataReader("BAC.US",'stooq',start= startDate,end= endDate)
print(BAC)


