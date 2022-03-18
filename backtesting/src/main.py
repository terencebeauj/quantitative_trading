import logging
from exchanges.binance import *
from data_collector import *

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
    mode = input("Choost the program mode: data / backtest: ").lower()
    if mode in ["data", "backtest"]:
      break

  client = BinanceClient(futures=True)

  while True:
    symbol = input("Choose a symbol: ").upper()
    if symbol in client.symbols:
      break

  if mode == "data":
    collect_all(client, "binance", symbol)