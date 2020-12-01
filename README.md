# Binance_Bridge


This will be the guide that I used to setup my instance.  See links below to get your environment setup.
https://www.youtube.com/watch?v=rvhnz1yBHgQ

https://github.com/hackingthemarkets/binance-tutorials

https://github.com/hackingthemarkets/tradingview-webhooks


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