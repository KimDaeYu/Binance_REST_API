from binance import ThreadedWebsocketManager
import config
api_key = config.api_key
api_secret = config.api_secret

def main():
    twm = ThreadedWebsocketManager(api_key=api_key, api_secret=api_secret)

    # start is required to initialise its internal loop
    twm.start()
    """
    {'e': 'ORDER_TRADE_UPDATE', 'T': 1640496696956, 'E': 1640496696964, 'o': {'s': 'ETHUSDT', 'c': 'android_ynd1I6QwEDqDkI7IU9II', 'S': 'SELL', 'o': 'MARKET', 'f': 'GTC', 'q': '0.001', 'p': '0', 'ap': '0', 'sp': '0', 'x': 'NEW', 'X': 'NEW', 'i': 8389765512848795674, 'l': '0', 'z': '0', 'L': '0', 'T': 1640496696956, 't': 0, 'b': '0', 'a': '0', 'm': False, 'R': True, 'wt': 'CONTRACT_PRICE', 'ot': 'MARKET', 'ps': 'BOTH', 'cp': False, 'rp': '0', 'pP': False, 'si': 0, 'ss': 0}}
    {'e': 'ACCOUNT_UPDATE', 'T': 1640496696956, 'E': 1640496696964, 'a': {'B': [{'a': 'USDT', 'wb': '4.86345961', 'cw': '4.86345961', 'bc': '0'}], 'P': [{'s': 'ETHUSDT', 'pa': '0', 'ep': '0.00000', 'cr': '-0.09337000', 'up': '0', 'mt': 'cross', 'iw': '0', 'ps': 'BOTH', 'ma': 'USDT'}, {'s': 'ETHUSDT', 'pa': '0', 'ep': '0.00000', 'cr': '-0.00090000', 'up': '0', 'mt': 'cross', 'iw': '0', 'ps': 'SHORT', 'ma': 'USDT'}], 'm': 'ORDER'}}
    {'e': 'ORDER_TRADE_UPDATE', 'T': 1640496696956, 'E': 1640496696964, 'o': {'s': 'ETHUSDT', 'c': 'android_ynd1I6QwEDqDkI7IU9II', 'S': 'SELL', 'o': 'MARKET', 'f': 'GTC', 'q': '0.001', 'p': '0', 'ap': '4025.18000', 'sp': '0', 'x': 'TRADE', 'X': 'FILLED', 'i': 8389765512848795674, 'l': '0.001', 'z': '0.001', 'L': '4025.18', 'n': '0.00161007', 'N': 'USDT', 'T': 1640496696956, 't': 1311468241, 'b': '0', 'a': '0', 'm': False, 'R': True, 'wt': 'CONTRACT_PRICE', 'ot': 'MARKET', 'ps': 'BOTH', 'cp': False, 'rp': '-0.01556000', 'pP': False, 'si': 0, 'ss': 0}}
    """
    def handle_socket_message(msg):
        #print(f"message type: {msg['e']}")
        print(msg)
    twm.start_futures_socket(callback=handle_socket_message)
    twm.join()



if __name__ == "__main__":
   main()