from dotenv import load_dotenv
import pandas as pd
import os

from coinbase.wallet.client import Client

# Loading environemnt variables from .env
load_dotenv(dotenv_path=".env")
# Specifying slack token
API_KEY = os.environ.get("API_KEY")
API_SECRET = os.environ.get("API_SECRET")

# Initializing client
client = Client(API_KEY, API_SECRET)
# Reading in transaction history
history_df = pd.read_csv("transaction_history.csv", skiprows=7)


def calculate_current_assets():
    """
    Calculates how much of the asset you currently hold (in the respective currency) based on transaction history
    """
    filtered_df = history_df[
        (history_df["Transaction Type"] != "Convert") & (history_df["Asset"] != "SKL")
    ]
    current_assets_df = (
        filtered_df.groupby(["Asset"])["Quantity Transacted", "USD Subtotal"]
        .sum()
        .reset_index()
        .rename(
            columns={
                "Quantity Transacted": "total_assets_purchased",
                "USD Subtotal": "total_assets_purchased_cost",
            }
        )
    )
    return current_assets_df


def get_asset_price(ticker):
    return float(client.get_buy_price(currency_pair=f"{ticker}-USD")["amount"])


current_assets_df = calculate_current_assets()
current_assets_df["current_asset_price"] = current_assets_df["Asset"].apply(
    get_asset_price
)
current_assets_df["total_asset_value"] = (
    current_assets_df["total_assets_purchased"]
    * current_assets_df["current_asset_price"]
)
current_assets_df["total_profit"] = (
    current_assets_df["total_asset_value"]
    - current_assets_df["total_assets_purchased_cost"]
)
print(current_assets_df)