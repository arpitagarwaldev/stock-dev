from typing import Dict, List, Optional
from ..models.database import Database
from .stock_service import StockService

class TradingService:
    def __init__(self):
        self.db = Database()
        self.stock_service = StockService()
    
    def create_user(self, username: str, email: str = None, initial_balance: float = 100000) -> Optional[int]:
        """Create a new user account"""
        return self.db.create_user(username, email, initial_balance)
    
    def authenticate_user(self, username: str) -> Optional[Dict]:
        """Authenticate user and return user info"""
        user = self.db.get_user(username)
        if not user:
            return None
        
        user_id, username, email, balance, created_at, updated_at = user
        return {
            'user_id': user_id,
            'username': username,
            'email': email,
            'balance': balance,
            'created_at': created_at,
            'updated_at': updated_at
        }
    
    def get_user_portfolio(self, username: str) -> Optional[Dict]:
        """Get comprehensive user portfolio information"""
        user = self.db.get_user(username)
        if not user:
            return None
        
        user_id, username, email, balance, created_at, updated_at = user
        portfolio_holdings = self.db.get_portfolio(user_id)
        
        portfolio_value = 0
        portfolio_details = []
        total_gain_loss = 0
        
        # Get current prices for all holdings
        symbols = [holding[0] for holding in portfolio_holdings]
        current_prices = self.stock_service.get_multiple_prices(symbols)
        
        for symbol, shares, avg_price in portfolio_holdings:
            current_price = current_prices.get(symbol)
            if current_price:
                market_value = shares * current_price
                portfolio_value += market_value
                gain_loss = (current_price - avg_price) * shares
                gain_loss_percent = ((current_price - avg_price) / avg_price) * 100
                total_gain_loss += gain_loss
                
                portfolio_details.append({
                    'symbol': symbol,
                    'shares': shares,
                    'avg_price': round(avg_price, 2),
                    'current_price': round(current_price, 2),
                    'market_value': round(market_value, 2),
                    'gain_loss': round(gain_loss, 2),
                    'gain_loss_percent': round(gain_loss_percent, 2)
                })
        
        total_value = balance + portfolio_value
        total_gain_loss_percent = ((total_value - 100000) / 100000) * 100 if total_value > 0 else 0
        
        return {
            'user_id': user_id,
            'username': username,
            'email': email,
            'balance': round(balance, 2),
            'portfolio_value': round(portfolio_value, 2),
            'total_value': round(total_value, 2),
            'total_gain_loss': round(total_gain_loss, 2),
            'total_gain_loss_percent': round(total_gain_loss_percent, 2),
            'portfolio': portfolio_details,
            'created_at': created_at
        }
    
    def buy_stock(self, username: str, symbol: str, shares: int) -> Dict:
        """Execute a buy order"""
        user = self.db.get_user(username)
        if not user:
            return {'success': False, 'message': 'User not found'}
        
        user_id, _, _, balance, _, _ = user
        symbol = symbol.upper()
        
        # Validate inputs
        if shares <= 0:
            return {'success': False, 'message': 'Invalid number of shares'}
        
        # Validate symbol
        if not self.stock_service.validate_symbol(symbol):
            return {'success': False, 'message': 'Invalid stock symbol'}
        
        # Get current price
        current_price = self.stock_service.get_stock_price(symbol)
        if not current_price:
            return {'success': False, 'message': 'Unable to fetch current stock price'}
        
        total_cost = shares * current_price
        
        # Check if user has enough balance
        if balance < total_cost:
            return {
                'success': False, 
                'message': f'Insufficient funds. Required: ${total_cost:.2f}, Available: ${balance:.2f}'
            }
        
        # Execute trade
        new_balance = balance - total_cost
        self.db.update_balance(user_id, new_balance)
        self.db.add_transaction(user_id, symbol, 'BUY', shares, current_price, total_cost)
        self.db.update_portfolio(user_id, symbol, shares, current_price)
        
        return {
            'success': True,
            'message': f'Successfully bought {shares} shares of {symbol}',
            'symbol': symbol,
            'shares': shares,
            'price': round(current_price, 2),
            'total_cost': round(total_cost, 2),
            'new_balance': round(new_balance, 2)
        }
    
    def sell_stock(self, username: str, symbol: str, shares: int) -> Dict:
        """Execute a sell order"""
        user = self.db.get_user(username)
        if not user:
            return {'success': False, 'message': 'User not found'}
        
        user_id, _, _, balance, _, _ = user
        symbol = symbol.upper()
        
        # Validate inputs
        if shares <= 0:
            return {'success': False, 'message': 'Invalid number of shares'}
        
        # Check if user owns the stock
        portfolio = self.db.get_portfolio(user_id)
        owned_shares = 0
        
        for port_symbol, port_shares, _ in portfolio:
            if port_symbol == symbol:
                owned_shares = port_shares
                break
        
        if owned_shares < shares:
            return {
                'success': False, 
                'message': f'Insufficient shares. You own {owned_shares} shares of {symbol}'
            }
        
        # Get current price
        current_price = self.stock_service.get_stock_price(symbol)
        if not current_price:
            return {'success': False, 'message': 'Unable to fetch current stock price'}
        
        total_proceeds = shares * current_price
        
        # Execute trade
        new_balance = balance + total_proceeds
        self.db.update_balance(user_id, new_balance)
        self.db.add_transaction(user_id, symbol, 'SELL', shares, current_price, total_proceeds)
        self.db.update_portfolio(user_id, symbol, -shares, current_price)
        
        return {
            'success': True,
            'message': f'Successfully sold {shares} shares of {symbol}',
            'symbol': symbol,
            'shares': shares,
            'price': round(current_price, 2),
            'total_proceeds': round(total_proceeds, 2),
            'new_balance': round(new_balance, 2)
        }
    
    def get_transaction_history(self, username: str, limit: int = 50) -> List[Dict]:
        """Get user's transaction history"""
        user = self.db.get_user(username)
        if not user:
            return []
        
        user_id = user[0]
        transactions = self.db.get_transactions(user_id, limit)
        
        return [
            {
                'symbol': t[0],
                'type': t[1],
                'shares': t[2],
                'price': round(t[3], 2),
                'total_amount': round(t[4], 2),
                'timestamp': t[5]
            }
            for t in transactions
        ]
    
    def add_to_watchlist(self, username: str, symbol: str) -> Dict:
        """Add stock to user's watchlist"""
        user = self.db.get_user(username)
        if not user:
            return {'success': False, 'message': 'User not found'}
        
        user_id = user[0]
        symbol = symbol.upper()
        
        # Validate symbol
        if not self.stock_service.validate_symbol(symbol):
            return {'success': False, 'message': 'Invalid stock symbol'}
        
        success = self.db.add_to_watchlist(user_id, symbol)
        if success:
            return {'success': True, 'message': f'{symbol} added to watchlist'}
        else:
            return {'success': False, 'message': f'{symbol} is already in your watchlist'}
    
    def remove_from_watchlist(self, username: str, symbol: str) -> Dict:
        """Remove stock from user's watchlist"""
        user = self.db.get_user(username)
        if not user:
            return {'success': False, 'message': 'User not found'}
        
        user_id = user[0]
        symbol = symbol.upper()
        
        self.db.remove_from_watchlist(user_id, symbol)
        return {'success': True, 'message': f'{symbol} removed from watchlist'}
    
    def get_watchlist(self, username: str) -> List[Dict]:
        """Get user's watchlist with current prices"""
        user = self.db.get_user(username)
        if not user:
            return []
        
        user_id = user[0]
        symbols = self.db.get_watchlist(user_id)
        
        watchlist = []
        for symbol in symbols:
            info = self.stock_service.get_stock_info(symbol)
            if info:
                watchlist.append(info)
        
        return watchlist