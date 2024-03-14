from requests import get

class Dedust:
        def __init__(self):
                self.baseUrl = 'https://api.dedust.io'
                self.headers = {"Accept": "application/json"}

        def get_liquidity_providers_v1(self, address):
                return get(f'{self.baseUrl}/v1/pools/{address}/liquidity-providers', headers=self.headers).json()

        def get_accounts_assets(self, address):
                return get(f'{self.baseUrl}/v2/accounts/{address}/assets', headers=self.headers).json()

        def get_accounts_trades(self, address):
                return get(f'{self.baseUrl}/v2/accounts/{address}/trades', headers=self.headers).json()

        def get_assets(self):
                return get(f'{self.baseUrl}/v2/assets', headers=self.headers).json()

        def get_assets_symbol(self, symbol):
                return get(f'{self.baseUrl}v2/assets/{symbol}', headers=self.headers).json()

        def get_gcko_pairs(self):
                return get(f'{self.baseUrl}/v2/gcko/pairs', headers=self.headers).json()
        
        def get_gcko_tickers(self):
                return get(f'{self.baseUrl}/v2/gcko/tickers', headers=self.headers).json()
        
        def get_gcko_trades(self, ticker_id, type, limit):
                return get(f'{self.baseUrl}/v2/gcko/trades?ticker_id={ticker_id}&type={type}&limit={limit}', headers=self.headers).json()
        
        def get_jettons_metadata(self, address):
                return get(f'{self.baseUrl}/v2/jettons/{address}/metadata', headers=self.headers).json()
        
        def get_pools(self):
            return get(f'{self.baseUrl}/v2/pools', headers=self.headers).json()
        
        def get_pools_metadata(self, address):
            return get(f'{self.baseUrl}/v2/pools/{address}/metadata', headers=self.headers).json()
        
        def get_pools_trades(self, address):
            return get(f'{self.baseUrl}/v2/pools/{address}/trades', headers=self.headers).json()
        
        def get_prices(self):
            return get(f'{self.baseUrl}/v2/prices', headers=self.headers).json()