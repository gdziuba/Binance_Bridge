import requests, json, time
from chalice import Chalice
from binance.enums import *
from binance.client import Client
from binance.exceptions import BinanceAPIException, BinanceOrderException

app = Chalice(app_name='Binance')

API_KEY = 'mSxW5xpbUdsfOx0twZyjl2gpvQF29lt9peQqE3y1pkkyfaJlk4BYxkIYHMpHDpkl'
SECRET_KEY = 'SakaEvRu8SyX7hxCZcd18Bn5JTAiuCyRS3FkVAJSHZRkWfZR6sjdWad5V7RPdWMS'

client = Client(API_KEY, SECRET_KEY)


def buyFunc(webhook_message):
    # How much is available
    try:
        balance = client.get_asset_balance(asset='USDT')

    except BinanceAPIException as e:
        # error handling goes here
        print(e)
        pass
    
    except BinanceOrderException as e:
        # error handling goes here
        print(e)
        pass
    
    calqty = (float(balance['free']) / float(webhook_message['price'])) * float(webhook_message['qtypct'])

    # Place Buy Order
    try:
        order = client.order_limit_buy(
            symbol=webhook_message['ticker'],
            side=SIDE_BUY,
            type=ORDER_TYPE_LIMIT,
            timeInForce=TIME_IN_FORCE_GTC,
            quantity=round(calqty,2),
            price=webhook_message['price'])
    
    except BinanceAPIException as e:
        # error handling goes here
        print(e)
        pass
    
    except BinanceOrderException as e:
        # error handling goes here
        print(e)
        pass
    return order


def cancelFunc(webhook_message):
    try:
        openorders = client.get_open_orders(symbol=webhook_message['ticker'])
    
    except BinanceAPIException as e:
        # error handling goes here
        print(e)
    
    except BinanceOrderException as e:
        # error handling goes here
        print(e)
    
    for order in openorders:
        result = client.cancel_order(symbol=webhook_message['ticker'], orderId=order['orderId'])
        print(order['orderId'])
    
    return openorders

def sellFunc(webhook_message):
    try:
        order = client.order_limit_sell(
            symbol=webhook_message['ticker'],
            side=SIDE_SELL,
            type=ORDER_TYPE_LIMIT,
            timeInForce=TIME_IN_FORCE_GTC,
            quantity=webhook_message['qty'],
            price=webhook_message['price'])
    
    except BinanceAPIException as e:
        # error handling goes here
        print(e)
    
    except BinanceOrderException as e:
        # error handling goes here
        print(e)
    return order

def delayFunc(webhook_message):
    time.sleep(webhook_message['seconds'])


@app.route('/buy_crypto', methods=['POST'])
def buy_crypto():
    request = app.current_request
    webhook_message = request.json_body

    for messages in webhook_message:
        # This Cancels orders
        if messages['order'] == "cancel":
            cancelFunc(messages)
        
        # This Opens Buy Orders
        if messages['order'] == "buy" and messages['type'] == "limit":
            buyFunc(messages)

        #This Opens Sell Orders
        if messages['order'] == "sell" and messages['type'] == "limit":
            sellFunc(messages)

        if messages['delay'] == "true":
            delayFunc(messages)

    return 

