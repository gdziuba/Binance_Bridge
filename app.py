import requests, json, time
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
                quantity=round(calqty,2),
                price=round(float(webhook_message['price']),4))
        
        elif "qty" in webhook_message:
            order = client.order_limit_buy(
                symbol=webhook_message['ticker'],
                side=SIDE_BUY,
                type=ORDER_TYPE_LIMIT,
                timeInForce=TIME_IN_FORCE_GTC,
                quantity=round(float(webhook_message['qty']),4),
                price=round(float(webhook_message['price']),4))
    
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

# Sell Limit
def sellFunc(webhook_message):
    try:
        if "qtypct" in webhook_message:
            balance = client.get_asset_balance(asset=webhook_message['base'])
            calqty = (float(balance['free']) / float(webhook_message['price'])) * float(webhook_message['qtypct'])

            order = client.order_limit_sell(
                symbol=webhook_message['ticker'],
                side=SIDE_SELL,
                type=ORDER_TYPE_LIMIT,
                timeInForce=TIME_IN_FORCE_GTC,
                quantity=round(calqty,2),
                price=round(float(webhook_message['price']),4))

        elif "qty" in webhook_message:    
            order = client.order_limit_sell(
                symbol=webhook_message['ticker'],
                side=SIDE_SELL,
                type=ORDER_TYPE_LIMIT,
                timeInForce=TIME_IN_FORCE_GTC,
                quantity=round(float(webhook_message['qty']),4),
                price=round(float(webhook_message['price']),4))
    
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
    try:
        if "qtypct" in webhook_message:
            balance = client.get_asset_balance(asset=webhook_message['base'])
            avg_price = client.get_avg_price(symbol=webhook_message['ticker'])

            calqty = (float(balance['free']) / float(avg_price['price'])) * float(webhook_message['qtypct'])
            order = client.order_market_sell(
                symbol=webhook_message['ticker'],
                quantity=round(calqty,2))

        elif "qty" in webhook_message:
            order = client.order_market_sell(
                symbol=webhook_message['ticker'], 
                quantity=round(float(webhook_message['qty']),4))
    
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
    try:
        if "qtypct" in webhook_message:
            
            balance = client.get_asset_balance(asset=webhook_message['base'])
            avg_price = client.get_avg_price(symbol=webhook_message['ticker'])

            calqty = (float(balance['free']) / float(avg_price['price'])) * float(webhook_message['qtypct'])
            order = client.order_market_buy(
                symbol=webhook_message['ticker'],
                quantity=round(calqty,2))

        elif "qty" in webhook_message:
            order = client.order_market_buy(
                symbol=webhook_message['ticker'],
                quantity=round(float(webhook_message['qty']),4))
    

    
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

