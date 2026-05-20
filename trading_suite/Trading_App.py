import streamlit as st
import base64
from pages.utils import theme

st.set_page_config(
    page_title="Antigravity Trading Suite",
    page_icon="💰",
    layout="wide",
)

# Apply Premium Global Styling
theme.apply_custom_style()

# Hero Section
st.markdown('<div class="hero-section">', unsafe_allow_html=True)
st.markdown('<h1 class="hero-title">Stocks Price Prediction 📊</h1>', unsafe_allow_html=True)
st.subheader("Your all-in-one platform for professional stock analysis, predictive forecasting, and risk management.")
st.markdown('</div>', unsafe_allow_html=True)

# Main Video
try:
    import os
    video_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "first.mp4")
    st.video(video_path, autoplay=True, loop=True)
except:
    pass

st.divider()

st.markdown("## 🚀 Our Core Services")

def get_base64_image(image_path):
    try:
        with open(image_path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode('utf-8')
    except Exception:
        return ""

img1 = get_base64_image("C:/Users/Admin/Desktop/stocks_rnn/pic1.jpeg")
img2 = get_base64_image("C:/Users/Admin/Desktop/stocks_rnn/pic2.jpeg")
img3 = get_base64_image("C:/Users/Admin/Desktop/stocks_rnn/pic3.jpeg")
img4 = get_base64_image("C:/Users/Admin/Desktop/stocks_rnn/pic4.jpeg")

st.markdown("""
<style>
details.clickable-card summary {
    list-style: none;
    cursor: pointer;
    margin-bottom: 10px;
}
details.clickable-card summary::-webkit-details-marker {
    display: none;
}
details.clickable-card img {
    width: 100%;
    height: 220px;
    object-fit: cover;
    border-radius: 15px;
    box-shadow: 0 4px 10px rgba(0,0,0,0.15);
    transition: transform 0.3s ease;
    border: 2px solid transparent;
}
details.clickable-card summary:hover img {
    transform: scale(1.03);
    border: 2px solid #0078ff;
}
details.clickable-card .desc {
    padding: 20px;
    background: rgba(255, 255, 255, 0.7);
    backdrop-filter: blur(10px);
    border-radius: 10px;
    border: 1px solid rgba(255, 255, 255, 0.5);
    color: #1e293b;
    margin-top: 15px;
    margin-bottom: 25px;
    box-shadow: 0 4px 6px rgba(0,0,0,0.05);
}
</style>
""", unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    st.markdown(f"""
    <details class="clickable-card">
      <summary><img src="data:image/jpeg;base64,{img1}" alt="Stock Intelligence"></summary>
      <div class="desc">
        <h3>🔍 Stock Intelligence</h3>
        <p>Get deep insights into real-time stock performance, technical indicators (RSI, MACD, Bollinger Bands), and fundamental data with high-performance interactive visualizations.</p>
      </div>
    </details>
    
    <details class="clickable-card">
      <summary><img src="data:image/jpeg;base64,{img2}" alt="CAPM Risk Analysis"></summary>
      <div class="desc">
        <h3>📈 CAPM Risk Analysis</h3>
        <p>Calculate systematic risk (Beta) and expected returns using the Capital Asset Pricing Model. Compare multiple assets against market benchmarks seamlessly.</p>
      </div>
    </details>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <details class="clickable-card">
      <summary><img src="data:image/jpeg;base64,{img3}" alt="AI-Powered Prediction"></summary>
      <div class="desc">
        <h3>🔮 AI-Powered Prediction</h3>
        <p>Leverage advanced time-series forecasting (ARIMA) to project closing prices for the next 30 days. Stay ahead of market trends with statistical confidence.</p>
      </div>
    </details>
    
    <details class="clickable-card">
      <summary><img src="data:image/jpeg;base64,{img4}" alt="Beta Optimization"></summary>
      <div class="desc">
        <h3>📊 Beta Optimization</h3>
        <p>Individualized risk assessment tools to determine how specific assets react to market volatility, helping you build a more resilient portfolio.</p>
      </div>
    </details>
    """, unsafe_allow_html=True)

st.info("💡 **Pro Tip:** Use the sidebar to navigate between different modules. All data is fetched live and processed in real-time.")