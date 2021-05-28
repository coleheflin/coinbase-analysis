from dotenv import load_dotenv
import os

from coinbase.wallet.client import Client

# Loading environemnt variables from .env
load_dotenv(dotenv_path=".env")
# Specifying slack token
API_KEY = os.environ.get("API_KEY")
API_SECRET = os.environ.get("API_SECRET")

# Initializing client
client = Client(API_KEY, API_SECRET)

# Grabbing current price info
eth_price = float(client.get_buy_price(currency_pair="ETH-USD")["amount"])
ltc_price = float(client.get_buy_price(currency_pair="LTC-USD")["amount"])
algo_price = float(client.get_buy_price(currency_pair="ALGO-USD")["amount"])
ada_price = float(client.get_buy_price(currency_pair="ADA-USD")["amount"])
print(eth_price, ltc_price, algo_price, ada_price)
