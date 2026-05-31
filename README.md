# 📈 Stocks Price Prediction & Financial Analysis Platform

> An AI-powered web application for stock price forecasting and financial analysis using LSTM neural networks.

---

## 📌 About the Project

This platform is designed to help **retail investors and students** analyze stock market data without needing expensive tools. It combines deep learning (LSTM) with real-time data and interactive visualizations — all in a clean, glassmorphism-styled web interface.

Built as a **Final Year Project** at the University of Agriculture, Faisalabad (2022–2026).

---

## ✨ Features

- 📡 **Live Stock Data** — Fetches real-time OHLCV data for any ticker (AAPL, TSLA, etc.) via Yahoo Finance
- 📊 **Interactive Charts** — Candlestick and line charts powered by Plotly
- 📉 **Technical Indicators** — RSI (14-day), Moving Averages (MA-20, MA-50)
- 🤖 **LSTM Price Prediction** — 30-day future forecast using a 60-day sliding window
- 💹 **CAPM Analysis** — Beta coefficient and Expected Return vs S&P 500 benchmark

---

## 🛠️ Tech Stack

| Layer | Technology |
|-------|-----------|
| Frontend / UI | Streamlit + Custom CSS (Glassmorphism) |
| Deep Learning | TensorFlow 2.x / Keras |
| Data Visualization | Plotly 5.17+ |
| Data Processing | Pandas, NumPy, Scikit-learn |
| Data Source | yfinance (Yahoo Finance API) |
| Language | Python 3.10 |

---

## 📂 Project Structure

```
stocks-prediction/
│
├── app.py                  # Main Streamlit application
├── model/
│   └── lstm_model.py       # LSTM model definition & training
├── analysis/
│   ├── indicators.py       # RSI, Moving Averages
│   └── capm.py             # CAPM analysis
├── utils/
│   └── data_loader.py      # yfinance data fetching
├── assets/
│   └── style.css           # Glassmorphism custom styles
├── requirements.txt
└── README.md
```

---

## 🚀 Getting Started

### Prerequisites

- Python 3.10+
- pip

### Installation

```bash
# 1. Clone the repository
git clone https://github.com/your-username/stocks-prediction.git
cd stocks-prediction

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run the app
streamlit run app.py
```

The app will open at `http://localhost:8501`

---

## 📦 Requirements

```
streamlit
tensorflow
keras
plotly
yfinance
pandas
numpy
scikit-learn
```

Or install all at once:

```bash
pip install -r requirements.txt
```

---

## 🧠 Model Details

| Parameter | Value |
|-----------|-------|
| Architecture | 2-layer LSTM |
| Units per layer | 50 |
| Dropout | 0.2 |
| Input window | 60 days |
| Forecast horizon | 30 days |
| Scaler | MinMaxScaler |

### Model Performance

| Metric | AAPL | TSLA |
|--------|------|------|
| RMSE | 3.45 | 4.12 |
| MAE | 2.87 | 3.56 |
| R² Score | 0.94 | 0.91 |

---

## 🔮 Future Improvements

- [ ] NLP-based sentiment analysis from financial news
- [ ] Portfolio management module
- [ ] Multi-model comparison (ARIMA, Transformer)
- [ ] Cloud deployment (Streamlit Cloud / Heroku)
- [ ] Crypto and Forex support
- [ ] Trading signal generation

---

## 👩‍💻 Author

**Nehal Bakhtawar**
University of Agriculture, Faisalabad
Supervisor: Mr. Salman Afsar Awan

---

## 📄 License

This project is for academic purposes only.
