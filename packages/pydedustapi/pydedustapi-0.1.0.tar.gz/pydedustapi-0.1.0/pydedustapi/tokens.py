import requests

class Tokens:
        def __init__(self):
                self.baseUrl = 'https://api.dedust.io'
                self.headers = {"Accept": "application/json"}

        def get_token_price(self, symbol):
                response = requests.get(f"{self.baseUrl}/v2/prices", headers=self.headers)
                if response.status_code == 200:
                    data = response.json()
                    for entry in data:
                        if entry["symbol"] == f"{symbol}":
                            price = entry["price"]
                            return price
                else:
                    return f"Error: {response.status_code}"