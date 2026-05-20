import yfinance as yf
import matplotlib.pyplot as plt
from statsmodels.tsa.stattools import adfuller
from sklearn.metrics import mean_squared_error, r2_score
from statsmodels.tsa.arima.model import ARIMA
import numpy as np
from sklearn.preprocessing import StandardScaler
from datetime import datetime, timedelta
import pandas as pd 
import streamlit as st

@st.cache_data
def get_data(ticker):
    # Using a standard start date to ensure consistency and better caching
    stock_data = yf.download(ticker, start='2020-01-01')
    # Flatten MultiIndex and ensure we return a 1D-compatible Series
    if isinstance(stock_data.columns, pd.MultiIndex):
        stock_data.columns = stock_data.columns.get_level_values(0)
    
    if stock_data.empty or 'Close' not in stock_data.columns:
        raise ValueError(f"Could not fetch Close price for ticker: {ticker}")
        
    return stock_data['Close'].squeeze()

def stationary_check(close_price):
    # Ensure input is a 1D array for adfuller
    close_price_arr = np.array(close_price).flatten()
    adf_test = adfuller(close_price_arr)
    p_value = round(adf_test[1],3)
    return p_value

def get_rolling_mean(close_price):
    rolling_price = close_price.rolling(window=7).mean().dropna()
    return rolling_price
    
def get_differencing_order(close_price):
    p_value = stationary_check(close_price)
    d = 0
    while True:
        if p_value > 0.05:
            d += 1
            close_price = close_price.diff().dropna()
            p_value = stationary_check(close_price)
        else:
            break
    return d

@st.cache_data
def fit_model(data, differencing_order):
    # ARIMA models can be slow, especially with large orders. 
    # Caching helps but we should keep orders reasonable.
    try:
        model = ARIMA(data, order=(5, differencing_order, 5))
        model_fit = model.fit()
        forecast_steps = 30
        forecast = model_fit.get_forecast(steps=forecast_steps)
        predictions = forecast.predicted_mean
        return predictions
    except:
        # Fallback to a simpler model if ARIMA(30,d,30) fails or is too complex
        model = ARIMA(data, order=(2, differencing_order, 2))
        model_fit = model.fit()
        forecast_steps = 30
        forecast = model_fit.get_forecast(steps=forecast_steps)
        predictions = forecast.predicted_mean
        return predictions
    
def evaluate_model(original_price, differencing_order):
    train_data, test_data = original_price[:-30], original_price[-30:]
    predictions = fit_model(train_data, differencing_order)
    rmse = np.sqrt(mean_squared_error(test_data, predictions))
    return round(rmse,2)

def scaling(close_price):
    scaler = StandardScaler()
    scaled_data = scaler.fit_transform(np.array(close_price).reshape(-1,1))
    return scaled_data, scaler

def get_forecast(original_price, differencing_order):
    predictions = fit_model(original_price, differencing_order)
    start_date = datetime.now().strftime('%Y-%m-%d')
    end_date = (datetime.now() + timedelta(days = 29)).strftime('%Y-%m-%d')
    forecast_index = pd.date_range(start=start_date, end=end_date, freq='D')
    forecast_df = pd.DataFrame(predictions, index = forecast_index, columns = ['Close'])
    return forecast_df

def inverse_scaling(scaler, scaled_data):
    close_price = scaler.inverse_transform(np.array(scaled_data).reshape(-1,1))
    return close_price