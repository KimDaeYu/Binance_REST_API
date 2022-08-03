from binance import Client
import os

def get_position_amt(bot, symbol):
    get_position = bot.futures_position_information(symbol=symbol)
    amt = float(get_position[0]['positionAmt'])
    
    return amt
    

def close_all_position(bot, symbol):
    print('close_all_position')
    amt = get_position_amt(bot, symbol)
    if amt > 0:
        close_order = bot.futures_create_order(
            symbol=symbol, side="SELL", type="MARKET", quantity=amt
            )
        print(close_order)
    elif amt < 0:
        close_order = bot.futures_create_order(
            symbol=symbol, side="BUY", type="MARKET", quantity=abs(amt)
            )
        print(close_order)
    else:
        print("no position : amt is zero")
        

def lambda_handler(event, context):
    
    bot = Client(api_key=os.environ.get('api_key'), api_secret=os.environ.get('api_sc'))
    
    data = eval(event['body'])
	
    side=data.get('side')
    symbol=data.get('market')
    amt = get_position_amt(bot, symbol)
    if side == "BUY":
        if amt < 0:
            close_all_position(bot, symbol)
    elif side == "SELL":
        if amt > 0:
            close_all_position(bot, symbol)

    ord_type = data.get('ord_type')
    if ord_type == 'limit':
        order = bot.futures_create_order(
        symbol=data.get('market'), side=data.get('side'), type="LIMIT", timeInForce='GTC', quantity=float(data.get('volume')), price=float(data.get('price'))
        )
        print(order)
    elif ord_type == 'market':
        order = bot.futures_create_order(
        symbol=data.get('market'), side=data.get('side'), type="MARKET", quantity=float(data.get('volume'))
        )
        print(order)
    elif ord_type == 'close':
        close_all_position(bot, data.get('market'))
    else:
        raise ValueError