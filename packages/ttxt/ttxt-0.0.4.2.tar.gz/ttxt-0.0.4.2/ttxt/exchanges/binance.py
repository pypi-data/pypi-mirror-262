from email import header
import hmac
import base64
import hashlib
import json
import time
from wsgiref import headers
import requests
from urllib.parse import urlencode
from cryptography.hazmat.primitives.serialization import load_pem_private_key
from ttxt.base import baseSpotExchange
from ttxt.types import baseTypes

class binance(baseSpotExchange.BaseSpotExchange):
    def __init__(self, key, secret, **kwargs):
        super().__init__(key, secret, **kwargs)
        self.domain_url = "https://api.binance.com"
        
    def _getSymbol(self, symbol):
        return symbol.replace("/", "")
    
    def _getUserSymbol(self, symbol):
        return symbol.replace("-", "/")
    
    def generate_timestamp(self):
        """
        Return a millisecond integer timestamp.
        """
        return int(time.time() * 10**3)
    
    # Auth
    def sign(self, message):
        mac = hmac.new(bytes(self.secret, encoding='utf-8'), bytes(message, encoding='utf-8'), digestmod='sha256')
        d = mac.digest()
        return base64.b64encode(d)
    
    def parse_params_to_str(self, message):
        url = ''
        if message == None or message == '':
            params = [(key, val) for key, val in message.items()]
            params = "".join(["%s=%s" % (key, val) for key, val in message.items()])
            url=urlencode(params)
        if url == '':
            return ''
        return url
    
    def _signedRequest(self, method, request_path, queryString, body):
        timeMs = self.generate_timestamp()
        if method == "POST":
            body = json.dumps(body)
            queryString = json.dumps(queryString) if queryString is not None else ''
            signature = self.sign(self.parse_params_to_str(queryString)+self.parse_params_to_str(body))
        elif method == "GET":
            body = json.dumps(body)
            queryString = json.dumps(queryString) if queryString is not None else ''
            # print(queryString)
            signature = self.sign(self.parse_params_to_str(queryString))
            headers = {
                "X-MBX-APIKEY": signature
            }
            url = self.domain_url+request_path
            try:
                response = requests.request(url, headers=headers)
                return response.json()
            except Exception as e:
                raise e
            
    # Parsers
    def _parseBalance(self, balData):
        parsedBal = {"free": {}, "total": {}, "unrealisedPnl": {}}
        data = balData.get("data", None)['balances']
        if data is not None:
            for element in data:
                parsedBal["free"][element["asset"]] = element.get("free", None)
                parsedBal["total"][element["asset"]] = str(int(element.get("free", None))+int(element.get("locked", None)))
        return parsedBal
    
    def _parseCreateorder(self, order):
        pass
    
    def _parseOpenOrders(self, data):
        pass
    
    def _parseFetchOrder(self, data):
        pass
    
    def _parseCancelorder(self, order):
        pass
    
    # Exchange functions 
    def fetch_ticker(self, symbol):
        pass
    
    def fetch_balance(self, params={}) -> baseTypes.Balances:
        apiUrl = "/api/v3/account"
        try:
            params = {
                "timestamp": self.generate_timestamp()
            }
            resp = self._signedRequest('GET', apiUrl, params, '')
            return self._parseBalance(resp)
        except Exception as e:
            raise e
    
    def fetch_trades(self, symbol=None, startTime=None, endTime=None, limit=None, params={}): 
        pass
    
    def create_order(self, symbol, side, quantity, price, order_type, params={}): # change body
        pass
    
    def create_market_order(self, symbol, side, quantity, price, params={}): # change body
        pass
    
    def create_limit_order(self, symbol, side, quantity, price, params={}):
        pass
    
    def cancel_order(self, id, symbol=None, params={}):
        pass
    
    def fetch_open_orders(self, symbol=None, kwargs=None):
        pass
    
    def fetch_order(self, id, symbol = None, params={}):
        pass