import streamlit as st
import datetime
import pandas as pd
import yfinance as yf
from pages.utils import capm_functions
from pages.utils import theme

st.set_page_config(
    page_title="CAPM Analysis",
    page_icon="📈",
    layout="wide",
)

# Apply Premium Global Styling
theme.apply_custom_style()

st.title('Capital Asset Pricing Model (CAPM) 📈')

@st.cache_data
def get_capm_data(stocks_list, year):
    end = datetime.date.today()
    start = datetime.date(end.year - year, end.month, end.day)
    
    # Downloading market data (^GSPC for S&P 500)
    sp500_data = yf.download('^GSPC', start=start, end=end)['Close'].squeeze()
    sp500_df = pd.DataFrame(sp500_data)
    sp500_df.reset_index(inplace=True)
    sp500_df.columns = ['Date', 'sp500']
    sp500_df['Date'] = pd.to_datetime(sp500_df['Date']).dt.tz_localize(None)
    
    # Downloading stock data
    stocks_df = pd.DataFrame()
    for stock in stocks_list:
        data = yf.download(stock, start=start, end=end)['Close']
        stocks_df[stock] = data.squeeze()
    
    stocks_df.reset_index(inplace=True)
    stocks_df['Date'] = pd.to_datetime(stocks_df['Date']).dt.tz_localize(None)
    
    # Merge and clean
    df = pd.merge(stocks_df, sp500_df, on='Date', how='inner')
    return df

col1, col2 = st.columns([2, 1])
with col1:
    stocks_list = st.multiselect("Select Stocks for Analysis", 
                                 ('TSLA', 'AAPL', 'NFLX', 'MGM', 'MSFT', 'AMZN', 'NVDA', 'GOOGL'),
                                 ['AAPL', 'MSFT', 'GOOGL', 'AMZN'])
with col2:
    year = st.number_input("Lookback Period (Years)", 1, 10, 2)

if stocks_list:
    try:
        with st.spinner('Calculating CAPM Metrics...'):
            stocks_df = get_capm_data(stocks_list, year)
            
            col_t1, col_t2 = st.columns(2)
            with col_t1:
                st.subheader('Raw Market Data (Head)')
                st.dataframe(stocks_df.head(), use_container_width=True)
            with col_t2:
                st.subheader('Raw Market Data (Tail)')
                st.dataframe(stocks_df.tail(), use_container_width=True)

            st.divider()
            
            col_p1, col_p2 = st.columns(2)
            with col_p1:
                st.subheader('Price Performance')
                st.plotly_chart(capm_functions.interactive_plot(stocks_df), use_container_width=True)
            with col_p2:
                st.subheader('Normalized Performance (Relative Change)')
                st.plotly_chart(capm_functions.interactive_plot(capm_functions.normalize(stocks_df)), use_container_width=True)

            # Calculating daily return 
            stocks_daily_return = capm_functions.daily_return(stocks_df)

            beta = {}
            for i in stocks_daily_return.columns:
                if i not in ['Date', 'sp500']:
                    b, a = capm_functions.calculate_beta(stocks_daily_return, i)
                    beta[i] = b

            # CAPM Results
            rf = 0.02 # Assumed Risk Free Rate (e.g., 2%)
            rm = stocks_daily_return['sp500'].mean() * 252 # Annualized Market Return
            
            st.divider()
            st.subheader('CAPM Metrics & Expected Returns')
            
            res_col1, res_col2 = st.columns(2)
            
            # Beta Table
            beta_df = pd.DataFrame({'Stock': beta.keys(), 'Beta Value': [round(v, 2) for v in beta.values()]})
            with res_col1:
                st.markdown('#### Beta Values (Systematic Risk)')
                st.dataframe(beta_df, use_container_width=True)

            # Expected Return Table
            expected_returns = {s: round(rf + (v * (rm - rf)), 2) for s, v in beta.items()}
            return_df = pd.DataFrame({'Stock': expected_returns.keys(), 'Expected Return (%)': expected_returns.values()})
            with res_col2:
                st.markdown('#### CAPM Expected Annual Return')
                st.dataframe(return_df, use_container_width=True)

    except Exception as e:
        st.error(f"Error in calculation: {e}")
else:
    st.info("Please select at least one stock to begin analysis.")