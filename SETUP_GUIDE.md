# 🚀 Setup Guide - Stock Trading Simulator

## Prerequisites

- **Python 3.7+** installed
- **Web browser** (Chrome, Firefox, Safari, Edge)
- **Internet connection** for stock data

## 📦 Installation Methods

### Method 1: Automated Setup (Recommended)
```bash
# Navigate to project directory
cd stock_app

# Run automated setup
python setup.py
```

### Method 2: Manual Setup
```bash
# Create virtual environment
cd backend
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# Unix/Mac:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Initialize database
python -c "from src.models.database import Database; Database()"
```

## 🏃‍♂️ Running the Application

### Option 1: Use Run Scripts
```bash
# Unix/Mac/Linux
./run.sh

# Windows
run.bat
```

### Option 2: Manual Start
```bash
# Terminal 1: Start Backend
cd backend
source venv/bin/activate  # or venv\Scripts\activate on Windows
python src/app.py

# Terminal 2: Start Frontend
cd frontend
python -m http.server 8000
```

## 🌐 Access Points

- **Frontend**: http://localhost:8000
- **Backend API**: http://localhost:5000
- **API Health**: http://localhost:5000/api/health

## 🔧 Configuration

### Environment Variables (.env)
```bash
FLASK_ENV=development
SECRET_KEY=your-secret-key-here
INITIAL_BALANCE=100000
DATABASE_PATH=trading.db
```

### Port Configuration
- **Backend**: Port 5000 (configurable in app.py)
- **Frontend**: Port 8000 (configurable)

## 🧪 Testing the Setup

### 1. Backend Health Check
```bash
curl http://localhost:5000/api/health
# Should return: {"status": "healthy", "timestamp": ...}
```

### 2. Frontend Access
- Open http://localhost:8000
- Should see login/register page

### 3. Stock Data Test
```bash
curl "http://localhost:5000/api/stocks/info/AAPL"
# Should return Apple stock information
```

## 🐛 Troubleshooting

### Common Issues

#### Port Already in Use
```bash
# Find process using port
lsof -i :5000  # or :8000

# Kill process
kill -9 <PID>
```

#### Python Module Not Found
```bash
# Ensure virtual environment is activated
source venv/bin/activate

# Reinstall requirements
pip install -r requirements.txt
```

#### Stock Data Not Loading
- Check internet connection
- Yahoo Finance may have temporary issues
- Try different stock symbols

#### AI Predictions Not Working
```bash
# Install TensorFlow
pip install tensorflow==2.15.0

# Check if models directory exists
mkdir -p backend/models
```

### Error Messages

#### "Virtual environment not found"
```bash
# Run setup first
python setup.py
```

#### "Database connection failed"
```bash
# Recreate database
cd backend
python -c "from src.models.database import Database; Database()"
```

#### "WebSocket connection failed"
- Check if backend is running on port 5000
- Ensure CORS is properly configured

## 📱 Browser Compatibility

### Supported Browsers
- ✅ Chrome 80+
- ✅ Firefox 75+
- ✅ Safari 13+
- ✅ Edge 80+

### Required Features
- WebSocket support
- ES6 JavaScript
- CSS Grid/Flexbox
- Fetch API

## 🔒 Security Notes

### Development Mode
- Uses session-based authentication
- SQLite database (file-based)
- No HTTPS (development only)

### Production Considerations
- Change SECRET_KEY
- Use PostgreSQL/MySQL
- Enable HTTPS
- Add rate limiting
- Implement proper logging

## 📊 Performance Tips

### Backend Optimization
- AI model training can take 2-5 minutes
- Models are cached after training
- Use batch predictions for multiple stocks

### Frontend Optimization
- WebSocket connections are reused
- Price updates every 5 seconds
- Search results are debounced

## 🔄 Updates & Maintenance

### Updating Stock Data
- Data updates automatically from Yahoo Finance
- No manual intervention required

### Model Retraining
- Models retrain automatically when needed
- Can manually trigger via API:
```bash
curl -X POST http://localhost:5000/api/ai/train/AAPL
```

### Database Maintenance
- SQLite database grows with transactions
- Backup: Copy `trading.db` file
- Reset: Delete `trading.db` and restart

## 📈 Usage Tips

### Getting Started
1. Register with any username
2. Start with $100,000 virtual money
3. Search popular stocks: AAPL, GOOGL, MSFT
4. Try AI predictions before trading

### Best Practices
- Use AI as guidance, not absolute truth
- Diversify your virtual portfolio
- Track your performance over time
- Experiment with different strategies

## 🆘 Support

### Log Files
- Backend logs: Console output
- Frontend logs: Browser developer tools
- Database: `trading.db` file

### Debug Mode
```bash
# Enable Flask debug mode
export FLASK_ENV=development
python src/app.py
```

### Common Commands
```bash
# Check Python version
python --version

# List installed packages
pip list

# Check if ports are free
netstat -an | grep :5000
netstat -an | grep :8000
```

## 🎯 Next Steps

After successful setup:
1. **Explore Features**: Try all sections (Portfolio, Trading, Watchlist, History)
2. **Test AI**: Get predictions for different stocks
3. **Practice Trading**: Buy/sell with virtual money
4. **Learn Patterns**: Observe how AI recommendations perform
5. **Customize**: Modify code to add your own features

---

**Happy Trading!** 📈🚀