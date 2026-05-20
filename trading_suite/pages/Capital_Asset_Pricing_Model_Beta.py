import streamlit as st
import datetime
import pandas as pd
import yfinance as yf
from pages.utils import capm_functions
import plotly.express as px
import numpy as np
from pages.utils import theme

st.set_page_config(
    page_title="Individual Stock Beta",
    page_icon="🎯",
    layout="wide",
)

# Apply Premium Global Styling
theme.apply_custom_style()

st.title('🎯 Individual Stock Beta & Return')

@st.cache_data
def get_beta_data(stock, year):
    end = datetime.date.today()
    start = datetime.date(end.year - year, end.month, end.day)
    
    # Market Data
    sp500_data = yf.download('^GSPC', start=start, end=end)['Close'].squeeze()
    sp500_df = pd.DataFrame(sp500_data)
    sp500_df.reset_index(inplace=True)
    sp500_df.columns = ['Date', 'sp500']
    sp500_df['Date'] = pd.to_datetime(sp500_df['Date']).dt.tz_localize(None)
    
    # Stock Data
    data = yf.download(stock, start=start, end=end)['Close'].squeeze()
    stock_df = pd.DataFrame(data)
    stock_df.reset_index(inplace=True)
    stock_df.columns = ['Date', stock]
    stock_df['Date'] = pd.to_datetime(stock_df['Date']).dt.tz_localize(None)
    
    df = pd.merge(stock_df, sp500_df, on='Date', how='inner')
    return df

col1, col2 = st.columns([1, 1])
with col1:
    stock = st.selectbox("Select a Stock", ('AAPL', 'TSLA', 'NFLX', 'MGM', 'MSFT', 'AMZN', 'NVDA', 'GOOGL'))
with col2:
    year = st.number_input("Lookback Period (Years)", 1, 10, 2)

if stock:
    try:
        with st.spinner(f'Analyzing {stock}...'):
            stocks_df = get_beta_data(stock, year)
            stocks_daily_return = capm_functions.daily_return(stocks_df)
            
            beta, alpha = capm_functions.calculate_beta(stocks_daily_return, stock)
            
            # Assumptions
            rf = 0.02
            rm = stocks_daily_return['sp500'].mean() * 252
            return_value = round(rf + (beta * (rm - rf)), 2)

            # Display Metrics
            m_col1, m_col2 = st.columns(2)
            with m_col1:
                st.markdown(f"""
                <div class="metric-card">
                    <h3 style='color: #1e293b; margin-bottom: 0;'>Beta Value</h3>
                    <p style='font-size: 3rem; font-weight: bold; color: #0078ff; margin: 0;'>{beta:.2f}</p>
                    <p style='color: #64748b;'>Systematic Risk vs Market</p>
                </div>
                """, unsafe_allow_html=True)
            
            with m_col2:
                st.markdown(f"""
                <div class="metric-card">
                    <h3 style='color: #1e293b; margin-bottom: 0;'>Expected Return</h3>
                    <p style='font-size: 3rem; font-weight: bold; color: #10b981; margin: 0;'>{return_value}%</p>
                    <p style='color: #64748b;'>Annualized CAPM Estimate</p>
                </div>
                """, unsafe_allow_html=True)

            st.divider()
            
            # Regression Plot
            st.subheader(f'Regression Analysis: {stock} vs S&P 500')
            fig = px.scatter(stocks_daily_return, x='sp500', y=stock, 
                             labels={'sp500': 'S&P 500 Daily Return (%)', stock: f'{stock} Daily Return (%)'})
            
            # Add Regression Line
            x_range = np.linspace(stocks_daily_return['sp500'].min(), stocks_daily_return['sp500'].max(), 100)
            y_range = beta * x_range + alpha
            fig.add_scatter(x=x_range, y=y_range, name='Regression Line (Beta)', line=dict(color='red', width=3))
            
            fig.update_layout(plot_bgcolor='white', paper_bgcolor='#f8fafd', height=500)
            st.plotly_chart(fig, use_container_width=True)

    except Exception as e:
        st.error(f"Error analyzing {stock}: {e}")