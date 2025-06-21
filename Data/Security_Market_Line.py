import numpy as np
import pandas as pd
from find_betas import *
import matplotlib.pyplot as plt
import os
from dotenv import load_dotenv
from io import StringIO
import requests


def get_risk_free_market_line(ticker):
    beta = get_average_beta(ticker)
    s_and_p = get_SP_500_data()
    s_and_p = s_and_p['adjClose']

    lines = []
    for price in s_and_p.iloc:
        line = 0.054 + beta * (price - 0.054)
        lines.append(line)
    return lines


def get_ticker_dividends(ticker):
    load_dotenv()
    with open("/Users/bhavikpatel/Desktop/Real-Time-Alpha-Factor-Discovery-System/Data/API_KEY.env") as f:
        api_key = f.read().strip().split('=')[1]

    url = f"https://api.tiingo.com/tiingo/corporate-actions/{ticker}/distribution-yield"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Token {api_key}"
    }
    response = requests.get(url, headers=headers)
    data = response.json()

    df = pd.DataFrame(columns=['date', 'dividend'])


    for item in data:
        new_df= pd.DataFrame({'date': pd.Series(item['date']), 'dividend': pd.Series(item['trailingDiv1Y'])})
        df = pd.concat([df, new_df], ignore_index=True)
    return df


