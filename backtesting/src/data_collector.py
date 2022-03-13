from typing import *
from exchanges.binance import *
from utils import *
import time
import logging

logger = logging.getLogger()

def collect_all(client: BinanceClient, exchange: str, symbol: str):

  oldest_ts, most_recent_ts = None, None

  # Initial request
  if oldest_ts is None:
    data = client.get_historical(symbol=symbol, end_time=int(time.time() * 1000) - 60000)

    if len(data) == 0:
      logger.warning(f"{exchange}, {symbol}: No initial data found")
      return
    else:
      logger.info(f"{exchange}, {symbol}: Collected {len(data)} initial data from {ms_to_dt(data[0][0])} to {ms_to_dt(data[-1][0])}")
    
    oldest_ts = data[0][0]
    most_recent_ts = data[-1][0]
  

  # Most recent data
  while True:
    data = client.get_historical(symbol, start_time=int(most_recent_ts + 60000))

    if data is None:
      time.sleep(4) # Pause in case an error occurs during the request
      continue

    if len(data) < 2:
      break

    data = data[:-1]

    if data[-1][0] > most_recent_ts:
      most_recent_ts = data[-1][0]
    
    logger.info(f"{exchange} {symbol}: Collected {len(data)} recent data from {ms_to_dt(data[0][0])} to {ms_to_dt(data[-1][0])}")

    time.sleep(1)


  # Older data
  while True:
    data = client.get_historical(symbol, end_time=int(oldest_ts - 60000))

    if data is None:
      time.sleep(4) # Pause in case an error occurs during the request
      continue

    if len(data) == 0:
      logger.info(f"{exchange} {symbol}: Stopped older data collection because no data was found before {ms_to_dt(oldest_ts)}")
      break

    if data[0][0] < oldest_ts:
      oldest_ts = data[0][0]
    
    logger.info(f"{exchange} {symbol}: Collected {len(data)} older data from {ms_to_dt(data[0][0])} to {ms_to_dt(data[-1][0])}")

    time.sleep(1.1)