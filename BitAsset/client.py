import hashlib
import hmac
import json
import requests

from urllib.parse import urlencode

from constants import *
from helpers import *

class Client(object):
    def __init__(self, key, secret, timeout=30):
        self._api_key = key
        self._api_secret = secret
        self._api_timeout = int(timeout)

    def _build_headers(self):
        
        headers = {
            'Accept': 'application/json',
            'User-Agent': 'FTX-Trader/1.0',
        }
            
        return headers
    
    def _build_authorization(self, query=None):
        if query is None:
            query = {}

        nonce = str(get_current_timestamp())

        body = {
            'apiAccessKey': self._api_key,
            'apiTimeStamp': nonce
            }
        
        body.update(query)

        sha1 = hashlib.sha1()
        sha1.update(self._api_secret.encode("utf-8"))
        secret = sha1.hexdigest()

        payload = urlencode(body)

        sign = hmac.new(bytes(secret, 'utf-8'), bytes(payload, 'utf-8'), hashlib.sha256).hexdigest()

        body = {
            'apiAccessKey': self._api_key,
            'apiTimeStamp': nonce,
            'apiSign': sign,
        }

        body.update(query)

        return body

    def _build_url(self, scope, endpoint, body=None):
        if body is None:
            body = {}

        if scope.lower() == 'private':
            url = f"{PRIVATE_API_URL}/{PRIVATE_API_VERSION}/cash/{endpoint}"
        else:
            url = f"{PUBLIC_API_URL}/{PUBLIC_API_VERSION}/cash/public/{endpoint}"

        return f"{url}?{urlencode(body, True, '/[]')}" if len(body) > 0 else url

    def _send_request(self, scope, method, endpoint, query=None, param=None):
        if query is None:
            query = {}
        
        if param is None:
            param = {}
        
        # Build header first
        headers = self._build_headers()

        # Build body query
        if scope.lower() == 'private':
            body = self._build_authorization(query)
        else:
            body = query

        # Build final url here
        url = self._build_url(scope, endpoint, body)

        try:
            if method == 'GET':
                response = requests.get(url, headers = headers).json()
            elif method == 'POST':
                response = requests.post(url, headers = headers, json = param).json()
        except Exception as e:
            print ('[x] Error: {}'.format(e.args[0]))

        if 'data' in response:
            return response['data']
        else:
            return response

    # Public API

    def get_public_all_markets(self):
        """
        https://github.com/bitasset-exchange/bitasset-api/blob/master/rest-api-spot_EN.md#111-get-currency-pair

        :return: a list contains all available markets
        """

        return self._send_request('public', 'GET', 'symbols')

    def get_public_market_id(self, pair):
        """
        https://github.com/bitasset-exchange/bitasset-api/blob/master/rest-api-spot_EN.md#111-get-currency-pair

        :param pair: the trading pair to query
        :return: an ID number of the market
        """

        for market in self._send_request('public', 'GET', 'symbols'):
            if market['name'] == pair.upper():
                return market['id']
    
        return '[x] Error: trading pair not exist'

    def get_public_all_currencies(self):
        """
        https://github.com/bitasset-exchange/bitasset-api/blob/master/rest-api-spot_EN.md#112-get-currency-info

        :return: a list contains all available currencies
        """

        return self._send_request('public', 'GET', 'currencies')

    def get_public_currency_id(self, currency):
        """
        https://github.com/bitasset-exchange/bitasset-api/blob/master/rest-api-spot_EN.md#112-get-currency-info

        :param currency: the trading currency to query
        :return: an ID number of the currency
        """

        for coin in self._send_request('public', 'GET', 'currencies'):
            if coin['name'] == currency.upper():
                return coin['id']
        
        return '[x] Error: the currency not exist'

    def get_public_server_time(self):
        """
        https://github.com/bitasset-exchange/bitasset-api/blob/master/rest-api-spot_EN.md#113-server-time

        :return: 13 digits Timestamp of server time
        """

        return self._send_request('public', 'GET', 'server-time')

    def get_public_orderbook(self, pair):
        """
        https://github.com/bitasset-exchange/bitasset-api/blob/master/rest-api-spot_EN.md#114-market-depth

        :param pair: the trading pair to query
        :return: a dict contains asks and bids data
        """

        contractId = self.get_public_market_id(pair)

        if contractId == '[x] Error: trading pair not exist':
            return contractId

        return self._send_request('public', 'GET', 'query-depth', {'contractId': contractId})

    # Private API

    def get_private_balances(self):
        """
        https://github.com/bitasset-exchange/bitasset-api/blob/master/rest-api-spot_EN.md#121-get-users-balance

        :return: a list contains current account balances
        """

        return self._send_request('private', 'GET', 'accounts/balance')

    def get_private_active_orders(self, contractId=None):
        """
        https://github.com/bitasset-exchange/bitasset-api/blob/master/rest-api-spot_EN.md#122-get-order

        :param contractId: the id of market pair
        :return: a list contains all active_orders
        """

        if contractId is None:
            query = {}
        else:
            query = {'contractId': contractId}

        return self._send_request('private', 'GET', 'accounts/order/active', query)

    def get_private_order_info(self, orderId):
        """
        https://github.com/bitasset-exchange/bitasset-api/blob/master/rest-api-spot_EN.md#125-get-order-info

        :param orderId: Order ID
        :return: a list contains all info of the order
        """

        return self._send_request('private', 'GET', 'accounts/order/get', {'orderId': orderId})

    # Private API (Write)

    def set_private_order(self, contractId, side, price, quantity, orderType):
        """
        https://github.com/bitasset-exchange/bitasset-api/blob/master/rest-api-spot_EN.md#123-order

        :param contractId: the id of market pair
        :param side: buy for 1, sell for -1
        :param price: order price
        :param quantity: Order quantity
        :param orderType: 1(Limited price) 3(Market price)
        :return: success for order id, error for error message
        """

        param = {
            'contractId': contractId,
            'side': side,
            'price': price,
            'quantity': quantity,
            'orderType': orderType
        }

        return self._send_request('private', 'POST', 'trade/order', {}, param)

    def set_private_cancel_order(self, contractId, originalOrderId):
        """
        https://github.com/bitasset-exchange/bitasset-api/blob/master/rest-api-spot_EN.md#123-order

        :param contractId: the id of market pair
        :param originalOrderId: order id
        :return: success or error message
        """

        param = {
            'contractId': contractId,
            'originalOrderId': originalOrderId
        }

        return self._send_request('private', 'POST', 'trade/order/cancel', {'orderId': originalOrderId}, param)

client = Client('', '')
print (client.get_public_orderbook('BTC-USDT')['bids'])