import logging
from exchanges.binance import *
from data_collector import collect_all, data_validator
from analysis import *

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

formatter = logging.Formatter("%(asctime)s %(levelname)s :: %(message)s")

stream_handler = logging.StreamHandler()
stream_handler.setFormatter(formatter)
stream_handler.setLevel(logging.INFO)

file_handler = logging.FileHandler("info.log")
file_handler.setFormatter(formatter)
file_handler.setLevel(logging.DEBUG)

logger.addHandler(stream_handler)
logger.addHandler(file_handler)

if __name__ == "__main__":
  while True:
    mode = input("Choost the program mode: data / validator / analysis / backtest: ").lower()
    if mode in ["data", "backtest", "validator", "analysis"]:
      break

  client = BinanceClient(futures=True)

  while True:
    symbol = input("Choose a symbol: ").upper()
    if symbol in client.symbols:
      break


  if mode == "data":
    collect_all(client, "binance", symbol)
  
  if mode == "validator":
    data_validator("binance", symbol)
  
  if mode == "analysis":
    while True:
      tf = input("Choose a timeframe in wich you want to see the data: (1h, 1d, 1M): ")
      if tf in ["1h", "1d", "1M"]:
        break

    day_of_week = None

    if tf == "1h":
      while True:
        day_of_week = input("Choose a day to filter the data, or write 'n' (0: Monday, ..., 6: Sunday): ")
        try:
          if int(day_of_week) in range(7):
            break
        except:
          pass
        if day_of_week == 'n':
          break
    
    while True:
      showfliers = input("Do you want to see the outliers: ")
      if showfliers in ["y", "n"]:
        break

    if day_of_week != None:
      print(day_of_week)
      volatility_analyzer(symbol, tf, day_of_week, showfliers)
    else:
      volatility_analyzer(symbol, tf, showfliers=showfliers)