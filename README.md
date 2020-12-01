# Binance_Bridge

Process of setting things up require the following

Python 2.7.x

virtualenv

Chalice

AWS CLI

Guide to setup environment:

https://chalice-workshop.readthedocs.io/en/latest/todo-app/part1/00-intro-chalice.html

This is where I got the ideas from.  This will help understand the process:
https://www.youtube.com/watch?v=rvhnz1yBHgQ

Chalice Docs
 
https://chalice-workshop.readthedocs.io/en/latest/todo-app/part1/00-intro-chalice.html

https://github.com/hackingthemarkets/binance-tutorials

https://github.com/hackingthemarkets/tradingview-webhooks


Make sure to add your api keys to the script

Sample Structure:

Buy order then a sell order coming from TradingView

Juba Short Configurations:

First Sell ////////////////

[{
"order": "cancel",
"ticker": "{{ticker}}",
"delay": "false"
},
{
"order": "sell",
"type": "limit",
"ticker": "{{ticker}}",
"price": "{{plot_7}}",
"qty": "{{plot_4}}",
"delay": "false"
},
{
"order": "sell",
"type": "limit",
"ticker": "{{ticker}}",
"price": "{{plot_6}}",
"qty": "{{plot_4}}",
"delay": "false"
}]


First Buy ///////////////

[{
"order": "buy",
"base": "USDT",
"type": "limit",
"ticker": "{{ticker}}",
"price": "{{plot_5}}",
"qtypct": ".9998",
"delay": "false"
}]

Following Shorts /////////


[{
"order": "cancel",
"ticker": "{{ticker}}",
"delay": "false"
},
{
"order": "sell",
"type": "limit",
"ticker": "{{ticker}}",
"price": "{{plot_6}}",
"qty": "{{plot_4}}",
"delay": "false"
},
{
"order": "buy",
"base": "USDT",
"type": "limit",
"ticker": "{{ticker}}",
"price": "{{plot_5}}",
"qtypct": ".9998",
"delay": "false"
}]

Close Shorts ///////////

[{
"order": "cancel",
"ticker": "{{ticker}}",
"delay": "false"
},
{
"order": "buy",
"type": "market",
"ticker": "{{ticker}}",
"price": "{{close}}",
"qtypct": ".90",
"delay": "false"
},
{
"order": "NULL",
"base": "USDT",
"type": "NULL",
"ticker": "{{ticker}}",
"price": "100",
"qtypct": ".9998",
"delay": "true",
"seconds": 5
},
{
"order": "buy",
"type": "market",
"ticker": "{{ticker}}",
"price": "{{close}}",
"qtypct": ".9998",
"delay": "false"
}]
