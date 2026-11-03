import pandas as pd 

def readCSV(self, location):
  try:
    CSV = pd.read_csv(location)
    return CSV
  except:
    return