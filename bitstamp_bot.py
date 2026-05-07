import json

import websocket
import bitstamp.client

import credentials

def client():
    return bitstamp.client.Trading(username=credentials.USERNAME, key=credentials.KEY, secret=credentials.SECRET) # JAMAIS colocar suas chaves, api keys, segredos etc. dentro de um script!!!

def buy(amount):
    trading_client = client()
    trading_client.buy_market_order(amount)

def sell(amount):
    trading_client = client()
    trading_client.sell_market_order(amount)

def on_message(ws, message):
    parsed_message = json.loads(message)

    print("-" * 50)
    #print(parsed_message)
    if 'id' in parsed_message['data']:
        price = parsed_message['data']['price']
        amount_sold = parsed_message['data']['amount']
        amount_sold_str = parsed_message['data']['amount_str']

        print(f"BTC Price: ${price}")
        print(f"Amount Sold: {amount_sold_str}")
        print(f"Price of {amount_sold_str} BTC: ${price * amount_sold:.2f}")

        if price >= 80115:
            sell(1)
        elif price <= 80100:
            buy(1)
        else:
            print("Aguardar.")

def on_error(ws, error):
    print(error)

def on_close(ws, close_status_code, close_message):
    print("*--- closed connection ---*")
    if close_status_code:
        print(close_status_code)
    if close_message:
        print(close_message)

def on_open(ws):
    print("*--- opened connection ---*")

    json_subscribe = """
    {
        "event": "bts:subscribe",
        "data": {
            "channel": "live_trades_btcusd"
        }
    }
    """
    ws.send(json_subscribe)

if __name__ == "__main__":
    ws = websocket.WebSocketApp("wss://ws.bitstamp.net", on_open=on_open, on_close=on_close, on_message=on_message, on_error=on_error)
    ws.run_forever()