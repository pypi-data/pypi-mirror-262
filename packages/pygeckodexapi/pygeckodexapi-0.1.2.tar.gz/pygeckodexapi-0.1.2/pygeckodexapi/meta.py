from requests import get

class Metadata:
        def __init__(self):
                self.baseUrl = 'https://api.geckoterminal.com/api/v2'
                self.headers = {"Accept": "application/json"}

        # networks

        def getNetworks(self):
                return get(f'{self.baseUrl}/networks?page=1', headers=self.headers).json()

        # dexes

        def getDexes(self, network):
                return get(f'{self.baseUrl}/networks/{network}/dexes?page=1', headers=self.headers).json()

        # pools

        def getTrendingPools(self):
                return get(f'{self.baseUrl}/networks/trending_pools?page=1', headers=self.headers).json()

        def getTrendingPoolsNet(self, network):
                return get(f'{self.baseUrl}/networks/{network}/trending_pools?page=1', headers=self.headers).json()

        def getSpecificPoolNet(self, network, address):
                return get(f'{self.baseUrl}/networks/{network}/pools/{address}', headers=self.headers).json()

        def getMultiplePoolsNet(self, network, address):
                return get(f'{self.baseUrl}/networks/{network}/pools/multi/{address}', headers=self.headers).json()

        def getTopPoolsNet(self, network):
                return get(f'{self.baseUrl}/networks/{network}/pools?page=1', headers=self.headers).json()

        def getTopPoolsDexNet(self, network, dex):
                return get(f'{self.baseUrl}/networks/{network}/dexes/{dex}/pools?page=1', headers=self.headers).json()

        def getLatestPoolsNet(self, network):
                return get(f'{self.baseUrl}/networks/{network}/new_pools?page=1', headers=self.headers).json()

        def getLatestPools(self):
                return get(f'{self.baseUrl}/networks/new_pools?page=1', headers=self.headers).json()

        def SearchPoolsNet(self, query, network):
                return get(f'{self.baseUrl}/search/pools?query={query}&network={network}&page=1', headers=self.headers).json()

        # tokens

        def getTopPoolsToken(self, network, token_address):
                return get(f'{self.baseUrl}/networks/{network}/tokens/{token_address}/pools?page=1', headers=self.headers).json()

        def getSpecificTokenNet(self, network, address):
                return get(f'{self.baseUrl}/networks/{network}/tokens/{address}', headers=self.headers).json()

        def getMultipleTokenNet(self, network, address):
                return get(f'{self.baseUrl}/networks/{network}/tokens/multi/{address}', headers=self.headers).json()

        def getSpecificTokenInfoNet(self, network, address):
                return get(f'{self.baseUrl}/networks/{network}/tokens/{address}/info', headers=self.headers).json()

        def getPoolTokensInfoNet(self, network, pool_address):
                return get(f'{self.baseUrl}/networks/{network}/pools/{pool_address}/info', headers=self.headers).json()

        def getRecentlyUpdatedTokens(self):
                return get(f'{self.baseUrl}/tokens/info_recently_updated', headers=self.headers).json()

        # trades

        def getTrades(self, network, pool_address):
                return get(f'{self.baseUrl}/networks/{network}/pools/{pool_address}/trades', headers=self.headers).json()
