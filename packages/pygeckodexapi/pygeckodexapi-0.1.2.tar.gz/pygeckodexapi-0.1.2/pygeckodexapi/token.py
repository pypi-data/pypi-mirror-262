import requests

class Token:
    def __init__(self):
        self.baseUrl = 'https://api.geckoterminal.com/api/v2'
        self.headers = {"Accept": "application/json"}

    def getTokenPrice(self, network, address):
        response = requests.get(f"{self.baseUrl}/simple/networks/{network}/token_price/{address}", headers=self.headers)
        if response.status_code == 200:
            data = response.json()
            return data['data']['attributes']['token_prices'][f'{address}']
        else:
            result = f"Error: {response.status_code}"
            return result

    def getTokenSymbol(self, network, address):
        response = requests.get(f"{self.baseUrl}/networks/{network}/tokens/{address}", headers=self.headers)
        if response.status_code == 200:
            data = response.json()
            return data['data']['attributes']['symbol']
        else:
            result = f"Error: {response.status_code}"
            return result

    def getTokenName(self, network, address):
        response = requests.get(f"{self.baseUrl}/networks/{network}/tokens/{address}", headers=self.headers)
        if response.status_code == 200:
            data = response.json()
            return data['data']['attributes']['name']
        else:
            result = f"Error: {response.status_code}"
            return result

    def getTokenImage(self, network, address):
        response = requests.get(f"{self.baseUrl}/networks/{network}/tokens/{address}", headers=self.headers)
        if response.status_code == 200:
            data = response.json()
            return data['data']['attributes']['image_url']
        else:
            result = f"Error: {response.status_code}"
            return result

    def getTokenSupply(self, network, address):
        response = requests.get(f"{self.baseUrl}/networks/{network}/tokens/{address}", headers=self.headers)
        if response.status_code == 200:
            data = response.json()
            return data['data']['attributes']['total_supply']
        else:
            result = f"Error: {response.status_code}"
            return result

    def getTokenFdvUsd(self, network, address):
        response = requests.get(f"{self.baseUrl}/networks/{network}/tokens/{address}", headers=self.headers)
        if response.status_code == 200:
            data = response.json()
            return data['data']['attributes']['fdv_usd']
        else:
            result = f"Error: {response.status_code}"
            return result

    def getTokenVolumeUsd24h(self, network, address):
        response = requests.get(f"{self.baseUrl}/networks/{network}/tokens/{address}", headers=self.headers)
        if response.status_code == 200:
            data = response.json()
            return data['data']['attributes']['volume_usd']['h24']
        else:
            result = f"Error: {response.status_code}"
            return result
        
    def getTokenTopPools(self, network, address):
        response = requests.get(f"{self.baseUrl}/networks/{network}/tokens/{address}", headers=self.headers)
        if response.status_code == 200:
            data = response.json()
            return data['data']['relationships']['top_pools']['data']
        else:
            result = f"Error: {response.status_code}"
            return result