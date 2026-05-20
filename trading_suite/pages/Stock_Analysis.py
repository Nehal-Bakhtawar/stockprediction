import streamlit as st
import pandas as pd
import yfinance as yf
import plotly.graph_objects as go
import datetime
from pages.utils.plotly_figure import plotly_table, close_chart, candlestick, RSI, Moving_average, MACD, Bollinger_Bands
from pages.utils import theme
from pages.utils import theme

# setting page config
st.set_page_config(
        page_title="Stock Analysis",
        page_icon="page_with_curl",
        layout="wide",
    )

# Apply Premium Global Styling
theme.apply_custom_style()
theme.centered_header("Stock Analysis 🔍")

@st.cache_data
def fetch_stock_data(ticker, start, end):
    data = yf.download(ticker, start=start, end=end)
    if isinstance(data.columns, pd.MultiIndex):
        data.columns = data.columns.get_level_values(0)
    return data

@st.cache_data
def fetch_stock_info(ticker):
    return yf.Ticker(ticker).info


col1, col2, col3 = st.columns(3)

today = datetime.date.today()

with col1:
    ticker = st.text_input('Stock Ticker', 'AAPL').strip().upper()
with col2:
    start_date = st.date_input("Start Date", datetime.date(today.year-1, today.month, today.day))
with col3:
    end_date = st.date_input("End Date", datetime.date(today.year,today.month,today.day))

st.subheader(ticker)

try:
    stock_info = fetch_stock_info(ticker)
    st.write(stock_info.get('longBusinessSummary', 'No summary available.'))
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.write("**Sector:**", stock_info.get('sector', 'N/A'))
    with col2:
        st.write("**Employees:**", stock_info.get('fullTimeEmployees', 'N/A'))
    with col3:
        st.write("**Website:**", stock_info.get('website', 'N/A'))
except Exception as e:
    st.error(f"Error fetching stock info: {e}")
    stock_info = {}


col1, col2 = st.columns(2)
with col1:
    df = pd.DataFrame(index = ['Market Cap','Beta',
                            'EPS','PE Ratio'])
    df[''] = [stock_info.get("marketCap", "N/A"), stock_info.get("beta", "N/A"), stock_info.get("trailingEps", "N/A"), stock_info.get("trailingPE", "N/A")]
    fig_df = plotly_table(df)
    st.plotly_chart(fig_df, use_container_width=True)
with col2:
    df = pd.DataFrame(index = ['Qucik Ratio','Revenue per share','Profit Margins',
                            'Debt to Equity','Return on Equity'])
    df[''] = [stock_info.get("quickRatio", "N/A"), stock_info.get("revenuePerShare", "N/A"), stock_info.get("profitMargins", "N/A"), stock_info.get("debtToEquity", "N/A"), stock_info.get("returnOnEquity", "N/A")]
    fig_df = plotly_table(df)
    st.plotly_chart(fig_df, use_container_width=True)

data = fetch_stock_data(ticker, start_date, end_date)

if len(data) <1:
    st.write('##### Please write the name of valid Ticker')
else:
    col1, col2, col3 = st.columns(3)
    daily_change = data['Close'].iloc[-1] - data['Close'].iloc[-2]
    
    col1.metric("Daily Change", str(round(data['Close'].iloc[-1],2)), str(round(daily_change,2)))
    
    data.index = [str(i)[:10] for i in data.index]
    fig_tail = plotly_table(data.tail(10).sort_index(ascending = False).round(3))
    fig_tail.update_layout(height = 220)
    st.write('##### Historical Data (Last 10 days)')
    st.plotly_chart(fig_tail, use_container_width=True)
   
    st.markdown("""<hr style="height:2px;border:none;color:#dddddd;background-color:#dddddd;" /> """, unsafe_allow_html=True)
    col1, col2, col3, col4, col5, col6, col7, col8, col9, col10, col11,col12 = st.columns([1,1,1,1,1,1,1,1,1,1,1,1,])

    num_period = ''
    with col1:
        if st.button('5D'):
            num_period = '5d'
    with col2:
        if st.button('1M'):
            num_period = '1mo'
    with col3:
        if st.button('6M'):
            num_period = '6mo'
    with col4:
        if st.button('YTD'):
            num_period = 'ytd'
    with col5:
        if st.button('1Y'):
            num_period = '1y'
    with col6:
        if st.button('5Y'):
            num_period = '5y'
    with col7:
        if st.button('MAX'):
            num_period = 'max'
    
    col1, col2, col3 = st.columns([1,1,4])
    with col1:
        chart_type = st.selectbox('',('Candle','Line'))
    with col2:
        if chart_type == 'Candle':
            indicators = st.selectbox('',('RSI','MACD', 'Bollinger Bands'))
        else:
            indicators = st.selectbox('',('RSI','Moving Average','MACD'))

    data1 = yf.download(ticker, period='max')
    if isinstance(data1.columns, pd.MultiIndex):
        data1.columns = data1.columns.get_level_values(0)
    
    if data1.empty:
        st.error(f"No historical data found for {ticker}")
    else:
        new_df1 = data1.copy()
        if num_period == '':
            if chart_type == 'Candle' and indicators == 'RSI':
                st.plotly_chart(candlestick(data1, '1y'), use_container_width=True)
                st.plotly_chart(RSI(data1, '1y'), use_container_width=True)

            if chart_type == 'Candle' and indicators == 'MACD':
                st.plotly_chart(candlestick(data1, '1y'), use_container_width=True)
                st.plotly_chart(MACD(data1, '1y'), use_container_width=True)

            if chart_type == 'Candle' and indicators == 'Bollinger Bands':
                st.plotly_chart(Bollinger_Bands(data1, '1y'), use_container_width=True)

            if chart_type == 'Line' and indicators == 'RSI':
                st.plotly_chart(close_chart(data1, '1y'), use_container_width=True)
                st.plotly_chart(RSI(data1, '1y'), use_container_width=True)

            if chart_type == 'Line' and indicators == 'Moving Average':
                st.plotly_chart(Moving_average(data1, '1y'), use_container_width=True)

            if chart_type == 'Line' and indicators == 'MACD':
                st.plotly_chart(close_chart(data1, '1y'), use_container_width=True)
                st.plotly_chart(MACD(data1, '1y'), use_container_width=True)
        else:
            if chart_type == 'Candle' and indicators == 'RSI':
                st.plotly_chart(candlestick(new_df1, num_period), use_container_width=True)
                st.plotly_chart(RSI(new_df1, num_period), use_container_width=True)

            if chart_type == 'Candle' and indicators == 'MACD':
                st.plotly_chart(candlestick(new_df1, num_period), use_container_width=True)
                st.plotly_chart(MACD(new_df1, num_period), use_container_width=True)

            if chart_type == 'Line' and indicators == 'RSI':
                st.plotly_chart(close_chart(new_df1, num_period), use_container_width=True)
                st.plotly_chart(RSI(new_df1, num_period), use_container_width=True)

            if chart_type == 'Line' and indicators == 'Moving Average':
                st.plotly_chart(Moving_average(new_df1, num_period), use_container_width=True)
            if chart_type == 'Line' and indicators == 'MACD':
                st.plotly_chart(close_chart(new_df1, num_period), use_container_width=True)
                st.plotly_chart(MACD(new_df1, num_period), use_container_width=True)
