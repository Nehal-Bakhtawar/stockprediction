import plotly.graph_objects as go
import dateutil
import datetime
import numpy as np
import pandas as pd

def plotly_table(dataframe):
    headerColor = 'grey'
    rowEvenColor = '#f8fafd'
    rowOddColor = '#e1efff'
    fig = go.Figure(data=[go.Table(
    header=dict(
        values=["<b><b>"]+["<b>"+str(i)[:10]+"<b>" for i in dataframe.columns],
        line_color='#0078ff', fill_color='#0078ff',
        align='center', font=dict(color='white', size=15),height =35,
    ),
    cells=dict(
        values=[["<b>"+str(i)+"<b>" for i in dataframe.index]]+[dataframe[i] for i in dataframe.columns], fill_color = [[rowOddColor,rowEvenColor,rowOddColor, rowEvenColor]*10],
        align='left', line_color=['white'],font=dict(color=["black"], size=15)
    ))
    ])
    fig.update_layout( height= 400, margin=dict(l=0, r=0, t=0, b=0))
    return fig

def filter_data(dataframe, num_period):
    if num_period == '1mo':
        date = dataframe.index[-1] + dateutil.relativedelta.relativedelta(months=-1)
    elif num_period == '5d':
        date = dataframe.index[-1] + dateutil.relativedelta.relativedelta(days=-5)
    elif num_period == '6mo':
        date = dataframe.index[-1] + dateutil.relativedelta.relativedelta(months=-6)
    elif num_period == '1y':
        date = dataframe.index[-1] + dateutil.relativedelta.relativedelta(years=-1)
    elif num_period == '5y':
        date = dataframe.index[-1] + dateutil.relativedelta.relativedelta(years=-5)
    elif num_period == 'ytd':
        date = datetime.datetime(dataframe.index[-1].year, 1,1)
    else:
        date = dataframe.index[0]
    # Ensure index is timezone-naive for comparison
    if dataframe.index.tz is not None:
        dataframe.index = dataframe.index.tz_localize(None)
    
    # Ensure date is a pandas Timestamp and naive
    if isinstance(date, str):
        date = pd.to_datetime(date)
    if hasattr(date, 'tzinfo') and date.tzinfo is not None:
        date = date.replace(tzinfo=None)
    
    return dataframe[dataframe.index > date]


def close_chart(dataframe, num_period =False):
    if num_period:
        dataframe = filter_data(dataframe,num_period)
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=dataframe.index, y=dataframe['Open'],
                        mode='lines',
                        name='Open',line = dict( width=2,color = '#5ab7ff')))
    fig.add_trace(go.Scatter(x=dataframe.index, y=dataframe['Close'],
                        mode='lines',
                        name='Close',line = dict( width=2,color = 'black')))
    fig.add_trace(go.Scatter(x=dataframe.index, y=dataframe['High'],
                        mode='lines', name='High',line = dict( width=2,color = '#0078ff')))
    fig.add_trace(go.Scatter(x=dataframe.index, y=dataframe['Low'],
                        mode='lines', name='Low',line = dict( width=2,color = 'red')))
    fig.update_xaxes(rangeslider_visible=True)
    fig.update_layout(height = 500,margin=dict(l=0, r=20, t=20, b=0), plot_bgcolor = 'white',paper_bgcolor = '#f8fafd',legend=dict(
    yanchor="top",
    xanchor="right"
    ))
    return fig

def candlestick(dataframe, num_period):
    dataframe = filter_data(dataframe,num_period)
    fig = go.Figure()
    fig.add_trace(go.Candlestick(x=dataframe.index,
                    open=dataframe['Open'], high=dataframe['High'],
                    low=dataframe['Low'], close=dataframe['Close']))

    fig.update_layout(showlegend = False,height = 500,margin=dict(l=0, r=20, t=20, b=0), plot_bgcolor = 'white', paper_bgcolor = '#f8fafd')
    return fig

    
def RSI(dataframe, num_period):
    df = dataframe.copy()
    delta = df['Close'].diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
    rs = gain / loss
    df['RSI'] = 100 - (100 / (1 + rs))
    
    df = filter_data(df, num_period)
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=df.index,
        y=df.RSI, name = 'RSI',marker_color='orange',line = dict( width=2,color = 'orange'),
    ))
    fig.add_trace(go.Scatter(

        x=df.index,
        y=[70]*len(df), name = 'Overbought', marker_color='red',line = dict( width=2,color = 'red',dash='dash'),
    ))

    fig.add_trace(go.Scatter(
        x=df.index,
        y=[30]*len(df),fill='tonexty', name = 'Oversold', marker_color='#79da84',line = dict( width=2,color = '#79da84',dash='dash'),
    ))

    fig.update_layout(yaxis_range=[0,100],
        height=200,plot_bgcolor = 'white', paper_bgcolor = '#f8fafd',margin=dict(l=0, r=0, t=0, b=0),legend=dict(orientation="h",
    yanchor="top",
    y=1.02,
    xanchor="right",
    x=1
    )
    )
    return fig

def Moving_average(dataframe,num_period):
    df = dataframe.copy()
    df['SMA_50'] = df['Close'].rolling(window=50).mean()
    df['EMA_20'] = df['Close'].ewm(span=20, adjust=False).mean()
    
    df = filter_data(df, num_period)
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(x=df.index, y=df['Open'],
                        mode='lines',
                        name='Open',line = dict( width=2,color = '#5ab7ff')))
    fig.add_trace(go.Scatter(x=df.index, y=df['Close'],
                        mode='lines',
                        name='Close',line = dict( width=2,color = 'black')))
    fig.add_trace(go.Scatter(x=df.index, y=df['High'],
                        mode='lines', name='High',line = dict( width=2,color = '#0078ff')))
    fig.add_trace(go.Scatter(x=df.index, y=df['Low'],
                        mode='lines', name='Low',line = dict( width=2,color = 'red')))
    fig.add_trace(go.Scatter(x=df.index, y=df['SMA_50'],
                        mode='lines', name='SMA 50',line = dict( width=2,color = 'purple')))
    fig.add_trace(go.Scatter(x=df.index, y=df['EMA_20'],
                        mode='lines', name='EMA 20',line = dict( width=2,color = 'orange')))
    
    fig.update_xaxes(rangeslider_visible=True)
    fig.update_layout(height = 500,margin=dict(l=0, r=20, t=20, b=0), plot_bgcolor = 'white',paper_bgcolor = '#f8fafd',legend=dict(
    yanchor="top",
    xanchor="right"
    ))
    
    return fig


def Moving_average_candle_stick(dataframe,num_period):
    dataframe['SMA_50'] = dataframe['Close'].rolling(window=50).mean()
    dataframe = filter_data(dataframe,num_period)
    fig = go.Figure()
    fig.add_trace(go.Candlestick(x=dataframe.index,
                    open=dataframe['Open'], high=dataframe['High'],
                    low=dataframe['Low'], close=dataframe['Close']))

    fig.add_trace(go.Scatter(x=dataframe.index, y=dataframe['SMA_50'],
                        mode='lines', name='SMA 50',line = dict( width=2,color = 'purple')))
    fig.update_xaxes(rangeslider_visible=True)
    fig.update_layout(height = 500,margin=dict(l=0, r=20, t=20, b=0), plot_bgcolor = 'white',paper_bgcolor = '#f8fafd',legend=dict(
    yanchor="top",
    xanchor="right"
    ))
    
    return fig

def Bollinger_Bands(dataframe, num_period):
    df = dataframe.copy()
    sma = df['Close'].rolling(window=20).mean()
    std = df['Close'].rolling(window=20).std()
    df['BBU'] = sma + (std * 2)
    df['BBL'] = sma - (std * 2)
    df['BBM'] = sma
    
    df = filter_data(df, num_period)
    
    fig = go.Figure()
    fig.add_trace(go.Candlestick(x=df.index,
                    open=df['Open'], high=df['High'],
                    low=df['Low'], close=df['Close'], name='Market'))
    
    fig.add_trace(go.Scatter(x=df.index, y=df['BBU'],
                        mode='lines', name='Upper Band', line=dict(width=1, color='rgba(173, 216, 230, 0.7)')))
    fig.add_trace(go.Scatter(x=df.index, y=df['BBL'],
                        mode='lines', name='Lower Band', line=dict(width=1, color='rgba(173, 216, 230, 0.7)'),
                        fill='tonexty', fillcolor='rgba(173, 216, 230, 0.2)'))
    fig.add_trace(go.Scatter(x=df.index, y=df['BBM'],
                        mode='lines', name='Middle Band', line=dict(width=1, color='orange')))
    
    fig.update_xaxes(rangeslider_visible=True)
    fig.update_layout(height=500, margin=dict(l=0, r=20, t=20, b=0), 
                      plot_bgcolor='white', paper_bgcolor='#f8fafd',
                      legend=dict(yanchor="top", xanchor="right"))
    return fig

def MACD(dataframe, num_period):
    df = dataframe.copy()
    exp1 = df['Close'].ewm(span=12, adjust=False).mean()
    exp2 = df['Close'].ewm(span=26, adjust=False).mean()
    df['MACD'] = exp1 - exp2
    df['MACD Signal'] = df['MACD'].ewm(span=9, adjust=False).mean()
    df['MACD Hist'] = df['MACD'] - df['MACD Signal']
    
    df = filter_data(df, num_period)
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=df.index,
        y=df['MACD'], name = 'MACD',marker_color='blue',line = dict( width=2,color = 'blue'),
    ))
    fig.add_trace(go.Scatter(
        x=df.index,
        y=df['MACD Signal'], name = 'Signal', marker_color='red',line = dict( width=2,color = 'red',dash='dash'),
    ))
    
    fig.add_trace(go.Bar(
        x=df.index,
        y=df['MACD Hist'], name = 'Histogram', marker_color=['red' if cl <0 else "green" for cl in df['MACD Hist']]
    ))
    
    fig.update_layout(
        height=250,plot_bgcolor = 'white', paper_bgcolor = '#f8fafd',margin=dict(l=0, r=0, t=0, b=0),legend=dict(orientation="h",
    yanchor="top",
    y=1.02,
    xanchor="right",
    x=1
    )
    )
    return fig

def Moving_average_forecast(forecast):
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(x=forecast.index[:-30], y=forecast['Close'].iloc[:-30],
                        mode='lines',
                        name='Close Price', line = dict( width=2,color = 'black')))
    fig.add_trace(go.Scatter(x=forecast.index[-31:], y=forecast['Close'].iloc[-31:],
                        mode='lines', name='Future Close Price',line = dict( width=2,color = 'red')))
    
    fig.update_xaxes(rangeslider_visible=True)
    fig.update_layout(height = 500,margin=dict(l=0, r=20, t=20, b=0), plot_bgcolor = 'white',paper_bgcolor = '#f8fafd',legend=dict(
    yanchor="top",
    xanchor="right"
    ))
    
    return fig