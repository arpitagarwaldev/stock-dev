# 📈 Stock Trading Simulator with AI Predictions

A comprehensive real-time stock trading simulator that allows users to practice trading with $100,000 virtual money using real market data and AI-powered predictions.

![Stock Trading Simulator](https://img.shields.io/badge/Python-3.7+-blue.svg)
![TensorFlow](https://img.shields.io/badge/TensorFlow-2.15-orange.svg)
![Flask](https://img.shields.io/badge/Flask-2.3-green.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

![Application Screenshot](https://via.placeholder.com/800x400/1a1a1a/ffffff?text=Stock+Trading+Simulator+Dashboard)

## 🎯 Key Features

### 💰 **Virtual Trading**
- Start with **$100,000** virtual money
- Buy and sell real stocks with **real-time prices**
- **Risk-free** learning environment
- Complete **portfolio tracking**

### 🧠 **AI-Powered Predictions**
- **LSTM Neural Network** for stock price forecasting
- **BUY/SELL/HOLD** recommendations
- **Confidence levels** (High/Medium/Low)
- **Multi-day predictions** (1-30 days)
- **Technical indicators** analysis

### 📊 **Real-Time Data**
- Live stock prices from **Yahoo Finance**
- **WebSocket** real-time updates
- **5-second** price refresh intervals
- **Historical charts** and data

### 🎨 **Modern Interface**
- **Responsive design** (mobile-friendly)
- **Real-time dashboard**
- **Interactive charts**
- **Toast notifications**

## 🚀 Quick Start

### 1. **Setup**
```bash
# Clone or download the project
cd stock_app

# Run automated setup
python setup.py
```

### 2. **Start Application**
```bash
# Unix/Mac/Linux
./run.sh

# Windows
run.bat
```

### 3. **Access Application**
- **Frontend**: http://localhost:8000
- **Backend API**: http://localhost:5000

## 📱 Screenshots

### Dashboard Overview
```
┌─────────────────────────────────────────────────────────────┐
│ 📈 Stock Trader                    Portfolio | Trading | ... │
│                                    Balance: $98,547.23       │
├─────────────────────────────────────────────────────────────┤
│ Portfolio Overview                                          │
│ ┌─────────────┐ ┌─────────────┐ ┌─────────────┐ ┌─────────┐ │
│ │Total Value  │ │Cash Balance │ │Portfolio    │ │Gain/Loss│ │
│ │$101,234.56  │ │$45,678.90   │ │$55,555.66   │ │+$1,234  │ │
│ └─────────────┘ └─────────────┘ └─────────────┘ └─────────┘ │
│                                                             │
│ Holdings                                                    │
│ ┌─────┬───────┬─────────┬─────────┬─────────┬─────────────┐ │
│ │AAPL │  10   │ $150.25 │ $155.30 │ $1,553  │ +$50.50    │ │
│ │GOOGL│   5   │ $120.00 │ $125.75 │ $628.75 │ +$28.75    │ │
│ └─────┴───────┴─────────┴─────────┴─────────┴─────────────┘ │
└─────────────────────────────────────────────────────────────┘
```

### AI Recommendations
```
┌─────────────────────────────────────────────────────────────┐
│ 🤖 AI Recommendations                                       │
│ ┌─────────────┐ ┌─────────────┐ ┌─────────────┐             │
│ │ AAPL   [BUY]│ │ TSLA  [SELL]│ │ MSFT  [HOLD]│             │
│ │ +5.2%       │ │ -8.1%       │ │ +1.2%       │             │
│ │ High Conf.  │ │ Medium Conf.│ │ Low Conf.   │             │
│ └─────────────┘ └─────────────┘ └─────────────┘             │
└─────────────────────────────────────────────────────────────┘
```

### Stock Analysis
```
┌─────────────────────────────────────────────────────────────┐
│ AAPL - Apple Inc.                           $155.30 +$2.15 │
│                                                             │
│ 🧠 AI Prediction                                           │
│ ┌─────────────────────────────────────────────────────────┐ │
│ │ [BUY] +5.36% Medium Confidence                          │ │
│ │ AI predicts AAPL will rise to $158.30 over 5 days      │ │
│ └─────────────────────────────────────────────────────────┘ │
│                                                             │
│ Trading Actions                                             │
│ Shares: [10] [Buy] [Sell] [Watchlist] [🤖 Get AI Prediction]│
└─────────────────────────────────────────────────────────────┘
```

## 🏗️ Architecture

### **Backend (Python)**
```
backend/
├── src/
│   ├── models/          # Database models
│   ├── services/        # Business logic & AI
│   ├── routes/          # API endpoints
│   └── app.py          # Flask application
├── config/             # Configuration
└── utils/              # Helper functions
```

### **Frontend (JavaScript)**
```
frontend/
├── src/
│   ├── app.js          # Main application
│   └── styles.css      # Styling
└── index.html          # Main page
```

## 🤖 AI Features

### **Neural Network Architecture**
- **LSTM** (Long Short-Term Memory) layers
- **60-day** input sequences
- **Technical indicators**: MA, RSI, Volume
- **Multi-layer** with dropout for regularization

### **Prediction System**
- **BUY**: Predicted increase > 3%
- **SELL**: Predicted decrease > 3%
- **HOLD**: Change between -3% to +3%

### **API Endpoints**
```http
GET  /api/ai/predict/AAPL?days=5    # Stock prediction
GET  /api/ai/recommendations        # Top AI picks
POST /api/ai/batch-predict          # Multiple stocks
```

## 📊 Complete Feature List

### **Trading Features**
- ✅ Real-time stock prices (Yahoo Finance)
- ✅ Buy/Sell with live market data
- ✅ Portfolio management & tracking
- ✅ Transaction history
- ✅ Watchlist functionality
- ✅ Gain/Loss calculations

### **AI Features**
- ✅ LSTM neural network predictions
- ✅ Technical indicator analysis
- ✅ BUY/SELL/HOLD recommendations
- ✅ Confidence scoring
- ✅ Multi-day forecasting
- ✅ Batch predictions

### **Technical Features**
- ✅ WebSocket real-time updates
- ✅ RESTful API design
- ✅ SQLite database
- ✅ Session-based authentication
- ✅ Responsive web design
- ✅ Error handling & validation

### **User Experience**
- ✅ Intuitive dashboard
- ✅ Mobile-friendly interface
- ✅ Toast notifications
- ✅ Loading states
- ✅ Search functionality
- ✅ One-click setup

## 🛠️ Technology Stack

### **Backend**
- **Python 3.7+**
- **Flask** - Web framework
- **TensorFlow** - Neural networks
- **scikit-learn** - ML utilities
- **yfinance** - Stock data (free)
- **SQLite** - Database
- **WebSocket** - Real-time updates

### **Frontend**
- **HTML5/CSS3/JavaScript**
- **Socket.IO** - Real-time communication
- **Chart.js** - Data visualization
- **Responsive design**

### **AI/ML**
- **LSTM** neural networks
- **Technical analysis** indicators
- **Time series** forecasting
- **Feature engineering**

## 📈 API Documentation

### **Authentication**
```http
POST /api/auth/register    # Create account
POST /api/auth/login       # Login
GET  /api/auth/me          # Current user
```

### **Trading**
```http
GET  /api/trading/portfolio     # Portfolio data
POST /api/trading/buy           # Buy stocks
POST /api/trading/sell          # Sell stocks
GET  /api/trading/transactions  # History
```

### **Market Data**
```http
GET  /api/stocks/search?q=AAPL  # Search stocks
GET  /api/stocks/info/AAPL      # Stock details
GET  /api/stocks/price/AAPL     # Current price
```

### **AI Predictions**
```http
GET  /api/ai/predict/AAPL       # AI prediction
GET  /api/ai/recommendations    # Top picks
POST /api/ai/batch-predict      # Multiple stocks
```

## 🎓 Educational Value

### **Learning Opportunities**
- **Risk-free trading** practice
- **Market dynamics** understanding
- **Portfolio management** skills
- **Technical analysis** basics
- **AI/ML** in finance

### **Skill Development**
- **Decision making** under uncertainty
- **Financial literacy** improvement
- **Technology integration**
- **Data analysis** skills

## ⚠️ Important Notes

### **Disclaimer**
- **Educational purposes only**
- **Not financial advice**
- **Virtual money only**
- **Past performance ≠ future results**

### **Data Sources**
- **Yahoo Finance** (free, no API key needed)
- **Real-time prices** with 5-second updates
- **Historical data** for AI training

## 🚀 Getting Started Guide

### **Step 1: Installation**
```bash
# Download/clone the project
cd stock_app

# Run setup (installs dependencies, creates database)
python setup.py
```

### **Step 2: Start Servers**
```bash
# Start both backend and frontend
./run.sh    # Unix/Mac/Linux
run.bat     # Windows
```

### **Step 3: Create Account**
1. Open http://localhost:8000
2. Click "Register"
3. Enter username
4. Start with $100,000 virtual money

### **Step 4: Start Trading**
1. Search for stocks (try AAPL, GOOGL, MSFT)
2. View AI recommendations
3. Get AI predictions
4. Buy/sell stocks
5. Track your portfolio

## 🔮 Future Enhancements

- **Options trading** simulation
- **Crypto trading** support
- **News integration**
- **Social trading** features
- **Mobile app** version
- **Advanced charting**
- **Portfolio optimization**

## 📄 License

MIT License - Feel free to use for educational purposes.

## 🤝 Contributing

Contributions welcome! Please read the contributing guidelines.

---

**Start your trading journey today with AI-powered insights!** 🚀📈