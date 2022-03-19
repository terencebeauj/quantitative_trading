from database import *
import logging
import time
import matplotlib.pyplot as plt

logger = logging.getLogger()

def analyzer(symbol):
  db = Hdf5Client()
  if symbol not in db.hf.keys():
    logger.warning(f"No data to perform analysis for: {symbol}")
    return
  
  df = db.get_data(symbol, 0, time.time() * 1000)
  print(f"Number of duplicated lines: {df.duplicated().sum()}")