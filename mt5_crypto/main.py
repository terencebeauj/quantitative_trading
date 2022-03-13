import MetaTrader5 as mt5
import dotenv
import os

if not mt5.initialize():
  print(f"Initialization failed, error: {mt5.last_error()}")
  quit()

print(mt5.terminal_info())
