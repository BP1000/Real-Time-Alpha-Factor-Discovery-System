import datetime
import numpy as np
import pandas as pd
import requests
from datetime import date
import yfinance as yf
from sklearn.preprocessing import MinMaxScaler
import os
from dotenv import load_dotenv
import json
from io import StringIO
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression

scaler = MinMaxScaler(feature_range=(-1, 1)) 


def get_nasdaq_composite_data(date):
    ticker = yf.Ticker("^GSPC")
    sp500 = ticker.history(start=date, end=datetime.date.today())
    sp500 = sp500.reset_index()
    sp500['Date'] = sp500['Date'].dt.strftime('%Y-%m-%d')

    return sp500




def get_ticker_data(ticker, date):
    
    load_dotenv()
    with open("/Users/bhavikpatel/Desktop/Real-Time-Alpha-Factor-Discovery-System/Data/API_KEY.env") as f:
        api_key = f.read().strip().split('=')[1]       
    
    url = f"https://api.tiingo.com/tiingo/daily/{ticker}/prices?startDate={pd.to_datetime(date)}1&endDate={datetime.date.today()}&format=csv&resampleFreq=daily"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Token {api_key}"
    }
    response = requests.get(url, headers=headers)
    df = pd.read_csv(StringIO(response.text))
    return df
    




def concat_dfs(ticker, date):
    nasdaq = get_nasdaq_composite_data(date)
    stock_data = get_ticker_data(ticker, date)
    if nasdaq.iloc[1]['Date'] != stock_data.iloc[1]['date']:
        df = pd.DataFrame({'Date': pd.Series(nasdaq['Date']), 'S&P 500 Data': pd.Series(nasdaq['Close'].values.flatten()), f'{ticker} Data': pd.Series(stock_data[['adjClose']].values.flatten())})
        df = df.iloc[1:]
    else:
        df = pd.DataFrame({'Date': pd.Series(nasdaq['Date']), 'S&P 500 Data': pd.Series(nasdaq['Close'].values.flatten()), f'{ticker} Data': pd.Series(stock_data['adjClose'].values.flatten())})

    return df


def get_beta(ticker, date):
    df = concat_dfs(ticker, date)
    X = df['S&P 500 Data']
    y = df[f'{ticker} Data']
    covariance = np.cov(X, y)
    variance = np.var(X)
    return covariance[0, 1] / variance







