import numpy as np
import pandas as pd
from find_betas import *
import matplotlib.pyplot as plt
import os
from dotenv import load_dotenv
from io import StringIO
import requests
from Security_Market_Line import *
import yfinance as yf
import datetime


def get_historical_shifts(ticker, date):
    df = concat_dfs(ticker, date)
    sp_500 = df['S&P 500 Data']
    stock_data = df[f'{ticker} Data']

    sp_500_returns = []
    for i in range(1, len(sp_500)):
        value = np.log(sp_500[i] / sp_500[i-1])
        sp_500_returns.append(value)
    

    stock_returns = []
    for i in range(1, len(stock_data)):
        value = np.log(stock_data[i] / stock_data[i-1])
        stock_returns.append(value)
    return stock_returns, sp_500_returns



def get_alphas(ticker, date, risk_rate):
    risk_rate = risk_rate / 252
    beta = get_beta(ticker, date)
    stock_returns, market_returns = get_historical_shifts(ticker, date)
    date = get_nasdaq_composite_data(date)['Date']
    
    alphas = []

    for i in range(len(market_returns)):
        alpha = stock_returns[i] - (risk_rate + beta * (market_returns[i] - risk_rate))
        alphas.append(alpha)
    date = date.iloc[1:len(alphas)+1]
    df = pd.DataFrame({'Date': date, f'{ticker} Alphas': alphas})
    df = df.set_index('Date')
    return df
    

    
print(get_alphas('AAPL', '2000-01-03', 0.0438))











