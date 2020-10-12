# BA-Trader

## Warning

This is an UNOFFICIAL wrapper for BitAsset exchange [HTTP API](https://github.com/bitasset-exchange/bitasset-api/blob/master/rest-api-spot_EN.md) written in Python 3.7

The library can be used to fetch market data, make trades, place orders or create third-party clients

USE THIS WRAPPER AT YOUR OWN RISK, I WILL NOT CORRESPOND TO ANY LOSES

## Features

- Implementation of all [public](#) and trade-related [private](#) endpoints
- Simple handling of [authentication](https://github.com/bitasset-exchange/bitasset-api/blob/master/rest-api-spot_EN.md#public-api-for-bitasset) with API key and secret
- For asset safety, WITHDRAWAL function will never be supported !

## Donate

If useful, buy me a coffee?

- ETH: 0xA9D89A5CAf6480496ACC8F4096fE254F24329ef0

## Installation

    $ git clone https://github.com/LeeChunHao2000/bitasset-api-wrapper-python3

## Requirement

1. [Register an account](https://www.bitasset.com/reg?icode=f46l) with BitAsset exchange _(referral link)_
2. [Generate API key and secret](https://www.bitasset.com/apiset), assign relevant permissions to it
3. Clone this repository, and put in the key and secret
4. Write your own trading policies 

## Quickstart

This is an introduction on how to get started with BitAsset client. First, make sure the BitAsset library is installed.

The next thing you need to do is import the library and get an instance of the client:

    from BitAsset.client import Client
    client = Client('PUY_MY_API_KEY_HERE', 'PUY_MY_API_SECRET_HERE')

### Get ordedrbook

    >>> from BitAsset.client import Client
    >>> client = Client('PUY_MY_API_KEY_HERE', 'PUY_MY_API_SECRET_HERE')
    >>> result = client.get_public_orderbook('BTC-USDT')
    >>> result
    {'contractId': 6, 'timestamp': 1602525647762, 'lastPrice': '11558.18', 'sign': 0, 'bids': [{'price': '11557.68', 'quantity': '2.5601'}], 'asks': [{'price': '11558.02', 'quantity': '1.2546'}]}
    >>> result['asks']
    [{'price': '11558.02', 'quantity': '1.2546'}]
    >>> result['bids']
    [{'price': '11557.68', 'quantity': '2.5601'}]
