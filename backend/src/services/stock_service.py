import yfinance as yf
import requests
from typing import Dict, List, Optional
from datetime import datetime, timedelta
import time

class StockService:
    def __init__(self):
        self.cache = {}
        self.cache_timeout = 60  # 1 minute cache
        
        # Popular stocks for search suggestions
        self.popular_stocks = [
            'AAPL', 'GOOGL', 'MSFT', 'AMZN', 'TSLA', 'META', 'NVDA', 
            'NFLX', 'BABA', 'V', 'JPM', 'JNJ', 'WMT', 'PG', 'UNH',
            'HD', 'DIS', 'PYPL', 'ADBE', 'CRM', 'INTC', 'AMD', 'ORCL',
            'IBM', 'CSCO', 'QCOM', 'TXN', 'AVGO', 'COST', 'PEP'
        ]
    
    def _is_cache_valid(self, symbol: str) -> bool:
        """Check if cached data is still valid"""
        if symbol not in self.cache:
            return False
        
        cache_time = self.cache[symbol].get('timestamp', 0)
        return (time.time() - cache_time) < self.cache_timeout
    
    def get_stock_price(self, symbol: str) -> Optional[float]:
        """Get current stock price using yfinance"""
        try:
            # Check cache first
            if self._is_cache_valid(symbol):
                return self.cache[symbol]['price']
            
            stock = yf.Ticker(symbol)
            
            # Try different periods to get price data
            for period in ["1d", "5d"]:
                try:
                    data = stock.history(period=period)
                    if not data.empty:
                        current_price = float(data['Close'].iloc[-1])
                        
                        # Update cache
                        self.cache[symbol] = {
                            'price': current_price,
                            'timestamp': time.time()
                        }
                        
                        return current_price
                except:
                    continue
            
            return None
        except Exception as e:
            print(f"Error fetching price for {symbol}: {e}")
            return None
    
    def get_stock_info(self, symbol: str) -> Optional[Dict]:
        """Get detailed stock information"""
        try:
            stock = yf.Ticker(symbol)
            info = stock.info
            hist = stock.history(period="2d")
            
            if hist.empty:
                return None
            
            current_price = float(hist['Close'].iloc[-1])
            prev_close = float(hist['Close'].iloc[-2]) if len(hist) > 1 else current_price
            
            change = current_price - prev_close
            change_percent = (change / prev_close) * 100 if prev_close != 0 else 0
            
            return {
                'symbol': symbol,
                'name': info.get('longName', info.get('shortName', symbol)),
                'price': current_price,
                'change': round(change, 2),
                'changePercent': round(change_percent, 2),
                'volume': info.get('volume', 0),
                'marketCap': info.get('marketCap', 0),
                'sector': info.get('sector', 'N/A'),
                'industry': info.get('industry', 'N/A'),
                'previousClose': prev_close,
                'dayHigh': float(hist['High'].iloc[-1]),
                'dayLow': float(hist['Low'].iloc[-1])
            }
        except Exception as e:
            print(f"Error fetching info for {symbol}: {e}")
            return None
    
    def search_stocks(self, query: str) -> List[Dict]:
        """Search for stocks by symbol or name"""
        results = []
        query = query.upper().strip()
        
        if not query:
            return results
        
        # Search in popular stocks first
        for symbol in self.popular_stocks:
            if query in symbol:
                info = self.get_stock_info(symbol)
                if info:
                    results.append(info)
        
        # If we have few results, try to get more using yfinance search
        if len(results) < 5:
            try:
                # Simple symbol validation and info fetch
                if len(query) <= 5 and query.isalpha():
                    info = self.get_stock_info(query)
                    if info and not any(r['symbol'] == query for r in results):
                        results.insert(0, info)
            except:
                pass
        
        return results[:10]  # Return top 10 results
    
    def get_historical_data(self, symbol: str, period: str = "1mo") -> List[Dict]:
        """Get historical stock data"""
        try:
            stock = yf.Ticker(symbol)
            data = stock.history(period=period)
            
            if data.empty:
                return []
            
            historical = []
            for date, row in data.iterrows():
                historical.append({
                    'date': date.strftime('%Y-%m-%d'),
                    'open': round(float(row['Open']), 2),
                    'high': round(float(row['High']), 2),
                    'low': round(float(row['Low']), 2),
                    'close': round(float(row['Close']), 2),
                    'volume': int(row['Volume'])
                })
            
            return historical
        except Exception as e:
            print(f"Error fetching historical data for {symbol}: {e}")
            return []
    
    def validate_symbol(self, symbol: str) -> bool:
        """Validate if a stock symbol exists"""
        try:
            stock = yf.Ticker(symbol)
            
            # Try multiple periods to handle market hours/weekends
            for period in ["1d", "5d", "1mo"]:
                try:
                    hist = stock.history(period=period)
                    if not hist.empty:
                        return True
                except:
                    continue
            
            # Also check if we can get basic info
            info = stock.info
            return bool(info and len(info) > 1)
        except:
            return False
    
    def get_market_movers(self) -> Dict[str, List[Dict]]:
        """Get market movers (gainers and losers)"""
        try:
            movers = {'gainers': [], 'losers': []}
            
            # Get info for popular stocks and sort by performance
            stocks_info = []
            for symbol in self.popular_stocks[:20]:  # Limit to avoid rate limits
                info = self.get_stock_info(symbol)
                if info and info.get('changePercent') is not None:
                    stocks_info.append(info)
            
            # Sort by change percent
            stocks_info.sort(key=lambda x: x['changePercent'], reverse=True)
            
            # Top 5 gainers and losers
            movers['gainers'] = stocks_info[:5]
            movers['losers'] = stocks_info[-5:]
            
            return movers
        except Exception as e:
            print(f"Error fetching market movers: {e}")
            return {'gainers': [], 'losers': []}
    
    def get_multiple_prices(self, symbols: List[str]) -> Dict[str, float]:
        """Get prices for multiple symbols efficiently"""
        prices = {}
        
        for symbol in symbols:
            price = self.get_stock_price(symbol)
            if price:
                prices[symbol] = price
        
        return prices