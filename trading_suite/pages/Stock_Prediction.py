import streamlit as st
from pages.utils.model_train import get_data, get_rolling_mean, get_differencing_order, scaling, evaluate_model, get_forecast, inverse_scaling
import pandas as pd
from pages.utils.plotly_figure import plotly_table, Moving_average_forecast
from pages.utils import theme

st.set_page_config(
    page_title="Stock Prediction",
    page_icon="🔮",
    layout="wide",
)

# Apply Premium Global Styling
theme.apply_custom_style()
theme.centered_header("Stock Price Prediction 🔮")

col1, col2, col3 = st.columns([1, 1, 1])

with col1:
    ticker = st.text_input('Enter Stock Ticker', 'AAPL').strip().upper()

if ticker:
    try:
        with st.spinner(f'Analyzing {ticker}... This may take a moment for complex models.'):
            close_price = get_data(ticker)
            rolling_price = get_rolling_mean(close_price)
            
            differencing_order = get_differencing_order(rolling_price)
            scaled_data, scaler = scaling(rolling_price)
            rmse = evaluate_model(scaled_data, differencing_order)
            
            st.success(f"Analysis complete for {ticker}")
            
            col_stat1, col_stat2 = st.columns(2)
            with col_stat1:
                st.metric("Model RMSE Score", f"{rmse:.4f}", help="Lower is better.")
            
            forecast = get_forecast(scaled_data, differencing_order)
            forecast['Close'] = inverse_scaling(scaler, forecast['Close'])
            
            st.subheader('📈 Forecast Visualization')
            # Ensure rolling_price is a DataFrame for correct concatenation
            rolling_df = rolling_price.to_frame(name='Close')
            full_forecast = pd.concat([rolling_df, forecast])
            st.plotly_chart(Moving_average_forecast(full_forecast.iloc[-180:]), use_container_width=True)
            
            st.subheader('📋 Forecast Data (Next 30 Days)')
            fig_tail = plotly_table(forecast.sort_index(ascending=True).round(3))
            fig_tail.update_layout(height=300)
            st.plotly_chart(fig_tail, use_container_width=True)

    except Exception as e:
        st.error(f"Error fetching or predicting data for {ticker}: {e}")
        st.info("Please ensure the ticker symbol is correct and you have an active internet connection.")
