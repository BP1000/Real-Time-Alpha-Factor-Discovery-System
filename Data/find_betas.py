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


scaler = MinMaxScaler(feature_range=(-1, 1)) 


def get_SP_500_data():
    load_dotenv()
    with open("/Users/bhavikpatel/Desktop/Real-Time-Alpha-Factor-Discovery-System/Data/API_KEY.env") as f:
        api_key = f.read().strip().split('=')[1] 
    
    url = f"https://api.tiingo.com/tiingo/daily/SPY/prices?startDate=2010-01-01&endDate={date.today()}&format=csv&resampleFreq=daily"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Token {api_key}"
    }
    response = requests.get(url, headers=headers)
    data = response.text
    df = pd.read_csv(StringIO(data))
    return df[['adjClose']]



def get_ticker_data(ticker):
    load_dotenv()
    with open("/Users/bhavikpatel/Desktop/Real-Time-Alpha-Factor-Discovery-System/Data/API_KEY.env") as f:
        api_key = f.read().strip().split('=')[1]       
    
    url = f"https://api.tiingo.com/tiingo/daily/{ticker}/prices?startDate=2010-01-01&endDate={date.today()}&format=csv&resampleFreq=daily"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Token {api_key}"
    }
    response = requests.get(url, headers=headers)
    data = response.text
    df = pd.read_csv(StringIO(response.text))
    return df[['adjClose']]

def concat_dfs(ticker):
    s_and_p = get_SP_500_data()
    stock_data = get_ticker_data(ticker)
    df = pd.DataFrame({'S&P 500 Data': pd.Series(s_and_p.values.flatten()), f'{ticker} Data': pd.Series(stock_data.values.flatten())})
    return df

def get_average_beta(ticker):
    df = concat_dfs(ticker)
    X = df[['S&P 500 Data']]
    y = df[[f'{ticker} Data']]
    X = X.to_numpy()
    y = y.to_numpy()
    covariance_matrix = np.cov(y.T, X.T)
    variance = np.var(X)
    lst = []
    for num in covariance_matrix:
        result = num / variance
        lst.append(result)
    return np.mean(lst)
