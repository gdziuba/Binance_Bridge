# Binance_Bridge


This will be the guide that I used to setup my instance.  See links below to get your environment setup.
https://www.youtube.com/watch?v=rvhnz1yBHgQ

Chalice Docs
 
https://chalice-workshop.readthedocs.io/en/latest/todo-app/part1/00-intro-chalice.html

https://github.com/hackingthemarkets/binance-tutorials

https://github.com/hackingthemarkets/tradingview-webhooks


Make sure to Adjust:
client = Client(config_Real.API_KEY, config_Real.SECRET_KEY)
to:
client = Client(config.API_KEY, config.SECRET_KEY)

And add your keys to the config file

Sample Structure:

Buy order then a sell order coming from TradingView

[{
"order": "buy",
"type": "limit",
"ticker": "BATUSDT",
"price": "0.2248",
"qtypct": ".9995",
"delay": "false"
},{
"order": "sell",
"type": "limit",
"ticker": "BATUSDT",
"price": "0.2406",
"qty": "900",
"delay": "false"
}]

Cancel Orders
[{
"order": "cancel",
"ticker": "BATUSDT",
"delay": "false"
}]

Delay
[{
    "delay": "true",
    "seconds": "10"
}]