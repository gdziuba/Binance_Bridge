import requests, json, time, math
import boto3
import base64
from chalice import Chalice
from binance.enums import *
from binance.client import Client
from binance.exceptions import BinanceAPIException, BinanceOrderException
from botocore.exceptions import ClientError

app = Chalice(app_name='Binance')

def get_secret():

    secret_name = "BinanceApi"
    region_name = "us-east-1"

    # Create a Secrets Manager client
    session = boto3.session.Session()
    client = session.client(
        service_name='secretsmanager',
        region_name=region_name
    )

    # In this sample we only handle the specific exceptions for the 'GetSecretValue' API.
    # See https://docs.aws.amazon.com/secretsmanager/latest/apireference/API_GetSecretValue.html
    # We rethrow the exception by default.

    try:
        get_secret_value_response = client.get_secret_value(
            SecretId=secret_name
        )
    except ClientError as e:
        if e.response['Error']['Code'] == 'DecryptionFailureException':
            # Secrets Manager can't decrypt the protected secret text using the provided KMS key.
            # Deal with the exception here, and/or rethrow at your discretion.
            raise e
        elif e.response['Error']['Code'] == 'InternalServiceErrorException':
            # An error occurred on the server side.
            # Deal with the exception here, and/or rethrow at your discretion.
            raise e
        elif e.response['Error']['Code'] == 'InvalidParameterException':
            # You provided an invalid value for a parameter.
            # Deal with the exception here, and/or rethrow at your discretion.
            raise e
        elif e.response['Error']['Code'] == 'InvalidRequestException':
            # You provided a parameter value that is not valid for the current state of the resource.
            # Deal with the exception here, and/or rethrow at your discretion.
            raise e
        elif e.response['Error']['Code'] == 'ResourceNotFoundException':
            # We can't find the resource that you asked for.
            # Deal with the exception here, and/or rethrow at your discretion.
            raise e
    else:
        # Decrypts secret using the associated KMS CMK.
        # Depending on whether the secret is a string or binary, one of these fields will be populated.
        if 'SecretString' in get_secret_value_response:
            secret = get_secret_value_response['SecretString']

        else:
            decoded_binary_secret = base64.b64decode(get_secret_value_response['SecretBinary'])
    return secret

apikeys = json.loads(get_secret())


#  *******************************
#   Replace Key and secret with respective api keys from binance
#   Will incorporate AWS Secrets at a later time for a more secure way of storing keys
#  *******************************
#   Hard code with the following
#   client = Client('your key', 'your secret')
client = Client(apikeys['gmail2key'], apikeys['gmail2secret'])

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
       if f['filterType'] == 'PRICE_FILTER':
            tic_sz = float(f['tickSize'])
            p1 = float(webhook_message['price'])
            p_precision_qty = int(round(-math.log(tic_sz, 10), 0))
            _price=round(float(p1),p_precision_qty)
            print("Convert "+str(p1)+" -> "+str(_price)+ " tickSize: "+str(tic_sz)+" Precision:"+str(p_precision_qty))

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
                #price=round(float(webhook_message['price']),8))
                price = _price)
            return order
        
        elif "qty" in webhook_message:
            order = client.order_limit_buy(
                symbol=webhook_message['ticker'],
                side=SIDE_BUY,
                type=ORDER_TYPE_LIMIT,
                timeInForce=TIME_IN_FORCE_GTC,
                quantity=round(float(webhook_message['qty']),_precision_quan),
                #price=round(float(webhook_message['price']),8))
                price = _price)
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
        if f['filterType'] == 'PRICE_FILTER':
            tic_sz = float(f['tickSize'])
            p1 = float(webhook_message['price'])
            p_precision_qty = int(round(-math.log(tic_sz, 10), 0))
            _price=round(float(p1),p_precision_qty)
            print("Convert "+str(p1)+" -> "+str(_price)+ " tickSize: "+str(tic_sz)+" Precision: "+str(p_precision_qty))
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
                #price=round(float(webhook_message['price']),8))
                price = _price)
        elif "qty" in webhook_message:    
            order = client.order_limit_sell(
                symbol=webhook_message['ticker'],
                side=SIDE_SELL,
                type=ORDER_TYPE_LIMIT,
                timeInForce=TIME_IN_FORCE_GTC,
                quantity=round(float(webhook_message['qty']),_precision_quan),
                #price=round(float(webhook_message['price']),8))
                price = _price)  
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

