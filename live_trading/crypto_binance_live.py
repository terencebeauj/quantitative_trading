import ccxt
import pandas as pd
import time
from ta.trend import IchimokuIndicator
from ta.volatility import BollingerBands
pd.set_option('display.expand_frame_repr', False)

class Organizer():
    def __init__(self, binance, pair, timeframe, window):
        self.binance = binance
        self.pair = pair
        self.timeframe = timeframe
        self.window = window
        self.candles_snap = None

    def OnInit(self):
        candles_snap = self.get_candles()
        candles_snap = pd.DataFrame(candles_snap, columns=["timestamp", "Open", "High", "Low", "Close", "Volume"])
        ichimoku = IchimokuIndicator(high=candles_snap.High, low=candles_snap.Low)
        bollinger_bands = BollingerBands(close=candles_snap.Close)
        candles_snap["ssa"] = ichimoku.ichimoku_a()
        candles_snap["ssb"] = ichimoku.ichimoku_b()
        candles_snap["kijun"] = ichimoku.ichimoku_base_line()
        candles_snap["tenkan"] = ichimoku.ichimoku_conversion_line()
        candles_snap["low_bb"] = bollinger_bands.bollinger_lband()
        candles_snap["high_bb"] = bollinger_bands.bollinger_hband()
        candles_snap["width_bb"] = bollinger_bands.bollinger_wband()
        candles_snap["datetime"] = pd.to_datetime(candles_snap.timestamp, errors="ignore", unit="ms")
        self.candles_snap = candles_snap.copy()
        candles_snap.dropna(inplace=True)
        print(candles_snap.tail())
        print("")

    def OnTick(self):
        candles = self.get_candles()
        if len(candles) == self.window:
            candles = pd.DataFrame(candles, columns=["timestamp", "Open", "High", "Low", "Close", "Volume"])
            ichimoku = IchimokuIndicator(high=candles.High, low=candles.Low)
            bollinger_bands = BollingerBands(close=candles.Close)
            candles["ssa"] = ichimoku.ichimoku_a()
            candles["ssb"] = ichimoku.ichimoku_b()
            candles["kijun"] = ichimoku.ichimoku_base_line()
            candles["tenkan"] = ichimoku.ichimoku_conversion_line()
            candles["low_bb"] = bollinger_bands.bollinger_lband()
            candles["high_bb"] = bollinger_bands.bollinger_hband()
            candles["width_bb"] = bollinger_bands.bollinger_wband()
            candles["datetime"] = pd.to_datetime(candles.timestamp, errors="ignore", unit="ms")

            same_candle = self.candles_snap.iloc[-1, 0] == candles.iloc[-1, 0]
            if same_candle:
                candles.dropna(inplace=True)
                print("Same candle")
                print(candles.iloc[-1,-1])
                print(candles.tail())
                print("")
            else:
                print("New candle")
                self.candles_snap = candles.copy()

                candles.dropna(inplace=True)
                print(candles.iloc[-1,-1])
                print(candles.tail())
                print("")

            time.sleep(0.25)

    def get_candles(self):
        candles = self.binance.fetch_ohlcv(self.pair, self.timeframe,  limit=self.window)
        return candles

def main():
    binance = ccxt.binance({"enableRateLimit": True})

    organizer = Organizer(binance=binance, pair="ETH/BUSD", timeframe="1m", window=100)
    organizer.OnInit()
    while True:
        organizer.OnTick()


if __name__ == '__main__':
    main()