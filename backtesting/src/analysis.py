import imp
from database import *
from utils import *
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
  
  returns = pd.DataFrame(df.close.pct_change(1))
  returns.set_index(df.index, inplace=True)
  returns = returns[3000:]
  monthly = returns.groupby([returns.index.year.rename("year"), returns.index.month.rename("month")]).mean()
  monthly.boxplot(column="close", by="month")
  plt.show()

