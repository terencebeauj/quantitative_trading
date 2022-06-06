import imp
from database import *
from utils import *
import logging
import time
import matplotlib.pyplot as plt
import seaborn as sns
from typing import Optional

sns.set_style("darkgrid")

logger = logging.getLogger()

def analyzer(symbol):
  db = Hdf5Client()
  if symbol not in db.hf.keys():
    logger.warning(f"No data to perform analysis for: {symbol}")
    return
  
  df = db.get_data(symbol, 0, time.time() * 1000)
  df = resample_timeframe(df, "15m")
  print(f"Number of duplicated lines: {df.duplicated().sum()}")
  
  returns = pd.DataFrame(df.close.pct_change(1))
  returns.set_index(df.index, inplace=True)
  returns = returns[3000:]*100
  monthly = returns.groupby([returns.index.dayofweek.rename("day"), returns.index.hour.rename("hour")]).mean()
  print(monthly)
  monthly.boxplot(column="close", by="hour")
  plt.show()

def volatility_analyzer(symbol, tf, day_of_week: Optional[str] = None, showfliers = True):
  db = Hdf5Client()
  if symbol not in db.hf.keys():
    logger.warning(f"No data to performs analysis for: {symbol}")
    return

  df = db.get_data(symbol, 0, time.time() * 1000)
  df = df[500:]
  df = resample_timeframe(df, tf)
  print(f"Number of duplicated lines: {df.duplicated().sum()}")
  df["returns"] = 100 * (df.close - df.open) / df.open
  if tf == "1h":
    if day_of_week != 'n':
      df = df[df.index.dayofweek == int(day_of_week)]
    sns.boxplot(data=df, x=df.index.hour, y="returns", showfliers= True if showfliers == "y" else False)
  if tf == "1d":
    sns.boxplot(data=df, x=df.index.dayofweek, y="returns", showfliers= True if showfliers == "y" else False)
  if tf == "1M":
    sns.boxplot(data=df, x=df.index.month, y="returns", showfliers= True if showfliers == "y" else False)
  else:
    print("Choose a correct timeframe (1h, 1d, 1M)")
  if day_of_week not in ["n", None]:
    days = {
      "0": "Monday",
      "1": "Tuesday",
      "2": "Wednesday",
      "3": "Thursday",
      "4": "Friday",
      "5": "Saturday",
      "6": "Sunday"
    }
    plt.title(f"Distribution of volatility by {tf}, on {days[day_of_week]}")
  else:
    plt.title(f"Distribution of volatility by {tf}")
  plt.show()