import requests

class Pool:
    def __init__(self):
        self.baseUrl = 'https://api.geckoterminal.com/api/v2'
        self.headers = {"Accept": "application/json"}

    def getPoolBaseTokenPriceUsd(self, network, address):
        response = requests.get(f"{self.baseUrl}/networks/{network}/pools/{address}", headers=self.headers)
        if response.status_code == 200:
            data = response.json()
            return data['data']['attributes']['base_token_price_usd']
        else:
            result = f"Error: {response.status_code}"
            return result

    def getPoolBaseTokenPriceNativeCurrency(self, network, address):
        response = requests.get(f"{self.baseUrl}/networks/{network}/pools/{address}", headers=self.headers)
        if response.status_code == 200:
            data = response.json()
            return data['data']['attributes']['base_token_price_native_currency']
        else:
            result = f"Error: {response.status_code}"
            return result

    def getPoolQuoteTokenPriceUsd(self, network, address):
        response = requests.get(f"{self.baseUrl}/networks/{network}/pools/{address}", headers=self.headers)
        if response.status_code == 200:
            data = response.json()
            return data['data']['attributes']['quote_token_price_usd']
        else:
            result = f"Error: {response.status_code}"
            return result

    def getPoolQuoteTokenPriceNativeCurrency(self, network, address):
        response = requests.get(f"{self.baseUrl}/networks/{network}/pools/{address}", headers=self.headers)
        if response.status_code == 200:
            data = response.json()
            return data['data']['attributes']['quote_token_price_native_currency']
        else:
            result = f"Error: {response.status_code}"
            return result
        
    def getPoolBaseTokenPriceQuoteToken(self, network, address):
            response = requests.get(f"{self.baseUrl}/networks/{network}/pools/{address}", headers=self.headers)
            if response.status_code == 200:
                data = response.json()
                return data['data']['attributes']['base_token_price_quote_token']
            else:
                result = f"Error: {response.status_code}"
                return result
        
    def getPoolQuoteTokenPriceBaseToken(self, network, address):
            response = requests.get(f"{self.baseUrl}/networks/{network}/pools/{address}", headers=self.headers)
            if response.status_code == 200:
                data = response.json()
                return data['data']['attributes']['quote_token_price_base_token']
            else:
                result = f"Error: {response.status_code}"
                return result

    def getPoolName(self, network, address):
            response = requests.get(f"{self.baseUrl}/networks/{network}/pools/{address}", headers=self.headers)
            if response.status_code == 200:
                data = response.json()
                return data['data']['attributes']['name']
            else:
                result = f"Error: {response.status_code}"
                return result

    def getPoolCreatedAt(self, network, address):
            response = requests.get(f"{self.baseUrl}/networks/{network}/pools/{address}", headers=self.headers)
            if response.status_code == 200:
                data = response.json()
                return data['data']['attributes']['pool_created_at']
            else:
                result = f"Error: {response.status_code}"
                return result

    def getPoolFdvUsd(self, network, address):
            response = requests.get(f"{self.baseUrl}/networks/{network}/pools/{address}", headers=self.headers)
            if response.status_code == 200:
                data = response.json()
                return data['data']['attributes']['fdv_usd']
            else:
                result = f"Error: {response.status_code}"
                return result

    def getPoolMarketCapUsd(self, network, address):
            response = requests.get(f"{self.baseUrl}/networks/{network}/pools/{address}", headers=self.headers)
            if response.status_code == 200:
                data = response.json()
                return data['data']['attributes']['market_cap_usd']
            else:
                result = f"Error: {response.status_code}"
                return result

    def getPoolPriceChangePercentage(self, network, address):
            response = requests.get(f"{self.baseUrl}/networks/{network}/pools/{address}", headers=self.headers)
            if response.status_code == 200:
                data = response.json()
                return data['data']['attributes']['price_change_percentage']
            else:
                result = f"Error: {response.status_code}"
                return result

    def getPoolTransactions(self, network, address):
            response = requests.get(f"{self.baseUrl}/networks/{network}/pools/{address}", headers=self.headers)
            if response.status_code == 200:
                data = response.json()
                return data['data']['attributes']['transactions']
            else:
                result = f"Error: {response.status_code}"
                return result

    def getPoolReserveInUsd(self, network, address):
            response = requests.get(f"{self.baseUrl}/networks/{network}/pools/{address}", headers=self.headers)
            if response.status_code == 200:
                data = response.json()
                return data['data']['attributes']['reserve_in_usd']
            else:
                result = f"Error: {response.status_code}"
                return result