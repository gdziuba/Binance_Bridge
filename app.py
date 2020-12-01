import requests, json, time, math
from chalice import Chalice
from binance.enums import *
from binance.client import Client
from binance.exceptions import BinanceAPIException, BinanceOrderException

app = Chalice(app_name='Binance')

#  *******************************
#   Replace Key and secret with respective api keys from binance
#   Will incorporate AWS Secrets at a later time for a more secure way of storing keys
#  *******************************
client = Client('key', 'secret')

# Buy Limit
def buyFunc(webhook_message):

    info = client.get_symbol_info(webhook_message['ticker'])
    filters = info['filters']
    _min_notional = filters
    for f in filters:
        print("filter~~~~~~~~~~~~ " + str(f))
        if f['filterType'] == 'LOT_SIZE': 
            _step_size = float(f['stepSize'])
            _precision_quan = int(round(-math.log(_step_size, 10), 0))
            print(_precision_quan)
    # Place Buy Order
    try:
        if "qtypct" in webhook_message:
            balance = client.get_asset_balance(asset=webhook_message['base'])
            calqty = (float(balance['free']) / float(webhook_message['price'])) * float(webhook_message['qtypct'])

            order = client.order_limit_buy(
                symbol=webhook_message['ticker'],
                side=SIDE_BUY,
                type=ORDER_TYPE_LIMIT,
                timeInForce=TIME_IN_FORCE_GTC,
                quantity=round(calqty,_precision_quan),
                price=round(float(webhook_message['price']),8))
            return order
        
        elif "qty" in webhook_message:
            order = client.order_limit_buy(
                symbol=webhook_message['ticker'],
                side=SIDE_BUY,
                type=ORDER_TYPE_LIMIT,
                timeInForce=TIME_IN_FORCE_GTC,
                quantity=round(float(webhook_message['qty']),_precision_quan),
                price=round(float(webhook_message['price']),8))
            return order
    
    except BinanceAPIException as e:
        # error handling goes here
        print(e)
        pass
    
    except BinanceOrderException as e:
        # error handling goes here
        print(e)
        pass
    return


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

# Sell Limit
def sellFunc(webhook_message):

    info = client.get_symbol_info(webhook_message['ticker'])
    filters = info['filters']
    _min_notional = filters
    for f in filters:
        print("filter~~~~~~~~~~~~ " + str(f))
        if f['filterType'] == 'LOT_SIZE': 
            _step_size = float(f['stepSize'])
            _precision_quan = int(round(-math.log(_step_size, 10), 0))
            print(_precision_quan)
    try:
        if "qtypct" in webhook_message:
            balance = client.get_asset_balance(asset=webhook_message['base'])
            calqty = (float(balance['free']) / float(webhook_message['price'])) * float(webhook_message['qtypct'])

            order = client.order_limit_sell(
                symbol=webhook_message['ticker'],
                side=SIDE_SELL,
                type=ORDER_TYPE_LIMIT,
                timeInForce=TIME_IN_FORCE_GTC,
                quantity=round(calqty,_precision_quan),
                price=round(float(webhook_message['price']),8))

        elif "qty" in webhook_message:    
            order = client.order_limit_sell(
                symbol=webhook_message['ticker'],
                side=SIDE_SELL,
                type=ORDER_TYPE_LIMIT,
                timeInForce=TIME_IN_FORCE_GTC,
                quantity=round(float(webhook_message['qty']),_precision_quan),
                price=round(float(webhook_message['price']),8))
    
    except BinanceAPIException as e:
        # error handling goes here
        print(e)
    
    except BinanceOrderException as e:
        # error handling goes here
        print(e)
    return order

def delayFunc(webhook_message):
    time.sleep(webhook_message['seconds'])

def sellMarketFunc(webhook_message):
    info = client.get_symbol_info(webhook_message['ticker'])
    filters = info['filters']
    _min_notional = filters
    for f in filters:
        print("filter~~~~~~~~~~~~ " + str(f))
        if f['filterType'] == 'LOT_SIZE': 
            _step_size = float(f['stepSize'])
            _precision_quan = int(round(-math.log(_step_size, 10), 0))
            print(_precision_quan)
    try:
        if "qtypct" in webhook_message:
            balance = client.get_asset_balance(asset=webhook_message['base'])
            avg_price = client.get_avg_price(symbol=webhook_message['ticker'])

            calqty = (float(balance['free']) / float(avg_price['price'])) * float(webhook_message['qtypct'])
            order = client.order_market_sell(
                symbol=webhook_message['ticker'],
                quantity=round(calqty,_precision_quan))

        elif "qty" in webhook_message:
            order = client.order_market_sell(
                symbol=webhook_message['ticker'], 
                quantity=round(float(webhook_message['qty']),_precision_quan))
    
    except BinanceAPIException as e:
        # error handling goes here
        print(e)
        pass
    
    except BinanceOrderException as e:
        # error handling goes here
        print(e)
        pass
    
        return order


def buyMarketFunc(webhook_message):
    info = client.get_symbol_info(webhook_message['ticker'])
    filters = info['filters']
    _min_notional = filters
    for f in filters:
        print("filter~~~~~~~~~~~~ " + str(f))
        if f['filterType'] == 'LOT_SIZE': 
            _step_size = float(f['stepSize'])
            _precision_quan = int(round(-math.log(_step_size, 10), 0))
            print(_precision_quan)
    try:
        if "qtypct" in webhook_message:
            
            balance = client.get_asset_balance(asset=webhook_message['base'])
            avg_price = client.get_avg_price(symbol=webhook_message['ticker'])

            calqty = (float(balance['free']) / float(avg_price['price'])) * float(webhook_message['qtypct'])
            order = client.order_market_buy(
                symbol=webhook_message['ticker'],
                quantity=round(calqty,_precision_quan))

        elif "qty" in webhook_message:
            order = client.order_market_buy(
                symbol=webhook_message['ticker'],
                quantity=round(float(webhook_message['qty']),_precision_quan))
    

    
    except BinanceAPIException as e:
                # error handling goes here
                print(e)
                pass
            
    except BinanceOrderException as e:
        # error handling goes here
        print(e)
        pass
    return order



@app.route('/buy_crypto', methods=['POST'])
def buy_crypto():


    request = app.current_request
    webhook_message = request.json_body

    for messages in webhook_message:
        # This Cancels orders
        if messages['order'] == "cancel":
            cancelFunc(messages)
        
        # This Opens limit Buy Orders
        elif messages['order'] == "buy" and messages['type'] == "limit":
            buyFunc(messages)

        #This Opens limit Sell Orders
        elif messages['order'] == "sell" and messages['type'] == "limit":
            sellFunc(messages)

        #This will open Market Buy Orders
        elif messages['order'] == "buy" and messages['type'] == "market":
            buyMarketFunc(messages)

        #This will open Mareket Sell Orders
        elif messages['order'] == "sell" and messages['type'] == "market":
            sellMarketFunc(messages)
   
        #This is a delay function - Untested
        elif messages['delay'] == "true":
            delayFunc(messages)

    return 

