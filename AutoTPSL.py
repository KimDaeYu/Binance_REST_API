from calendar import c
from binance import Client
import config
import pandas as pd
import time

api_key = config.api_key
api_secret = config.api_secret

bot = Client(api_key=config.api_key, api_secret=config.api_secret)

GetCoinInfo = bot.futures_exchange_info()
CoinInfo = pd.DataFrame(GetCoinInfo['symbols'])

GetPosition = bot.futures_position_information()
PosList = pd.DataFrame(GetPosition)
PosList.positionAmt = PosList.positionAmt.astype(float)
LastPos = PosList[PosList.positionAmt != 0]
CurrPos = PosList[PosList.positionAmt != 0]

while(1):
    time.sleep(5)
    LastPos = CurrPos
    GetPosition = bot.futures_position_information()
    PosList = pd.DataFrame(GetPosition)
    PosList.positionAmt = PosList.positionAmt.astype(float)
    CurrPos = PosList[PosList.positionAmt != 0]
    print("----------------------------------------------------")
    print("Current Position:" + str(len(CurrPos)))
    if(len(CurrPos) != 0):
        _usdt = abs(CurrPos.positionAmt.sum()) * float(CurrPos.entryPrice.sum()) / float(CurrPos.leverage.sum())
        if(CurrPos.positionAmt.sum() > 0):
            print("    Long Position: USDT " + f"{_usdt:.2f}$")
        else:
            print("    Short Position: USDT " + f"{_usdt:.2f}$")
    print("----------------------------------------------------")
    if((len(CurrPos) != len(LastPos) and len(CurrPos) != 0) or CurrPos.positionAmt.sum() * LastPos.positionAmt.sum() <= 0):
        # Close all Open Orders
        if(len(CurrPos) != 0):
            _symbol = CurrPos["symbol"].values[0]
            bot.futures_cancel_all_open_orders(symbol=_symbol)
        else:
            if(len(LastPos) == 0):
                # print("no")
                continue
            _symbol = LastPos["symbol"].values[0]
            bot.futures_cancel_all_open_orders(symbol=_symbol)
            print("position closed")
            continue
        
        print("Position changed")
        _quantity = abs(CurrPos["positionAmt"].values[0])
        if(CurrPos["positionAmt"].values[0] > 0):
            # Long Position / _side = "SELL"
            _side = "SELL"
            # stop loss 
            SLPrice = float(CurrPos["entryPrice"].values[0]) * 0.993
            SLPrice = round(SLPrice,CoinInfo[CoinInfo.symbol == _symbol].pricePrecision.values[0])
            order = bot.futures_create_order(
                symbol=_symbol, side="SELL", type="STOP_MARKET", stopPrice=SLPrice, closePosition=True, priceProtect=True
            )
            # take profit
            TPPrice = float(CurrPos["entryPrice"].values[0]) * 1.02
            TPPrice = round(TPPrice,CoinInfo[CoinInfo.symbol == _symbol].pricePrecision.values[0])  
            order = bot.futures_create_order(
                symbol=_symbol, side="SELL", type="TRAILING_STOP_MARKET", timeInForce='GTC', quantity=_quantity, activationPrice=TPPrice, callbackRate=0.4, reduceOnly=True
            )
        else:
            # Short Position / _side = "BUY"
            _side = "BUY"
            # stop loss
            SLPrice = float(CurrPos["entryPrice"].values[0]) * 1.007
            SLPrice = round(SLPrice,CoinInfo[CoinInfo.symbol == _symbol].pricePrecision.values[0])
            order = bot.futures_create_order(
                symbol=_symbol, side="BUY", type="STOP_MARKET", stopPrice=SLPrice, closePosition=True, priceProtect=True
            )
            # take profit
            TPPrice = float(CurrPos["entryPrice"].values[0]) * 0.98
            TPPrice = round(TPPrice,CoinInfo[CoinInfo.symbol == _symbol].pricePrecision.values[0])
            order = bot.futures_create_order(
                symbol=_symbol, side="BUY", type="TRAILING_STOP_MARKET", timeInForce='GTC', quantity=_quantity, activationPrice=TPPrice, callbackRate=0.4, reduceOnly=True
            )