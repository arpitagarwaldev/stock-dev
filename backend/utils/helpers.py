from datetime import datetime
from typing import Dict, Any
import re

def validate_email(email: str) -> bool:
    """Validate email format"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def validate_username(username: str) -> Dict[str, Any]:
    """Validate username format and requirements"""
    if not username:
        return {'valid': False, 'message': 'Username is required'}
    
    if len(username) < 3:
        return {'valid': False, 'message': 'Username must be at least 3 characters long'}
    
    if len(username) > 20:
        return {'valid': False, 'message': 'Username must be less than 20 characters long'}
    
    if not re.match(r'^[a-zA-Z0-9_]+$', username):
        return {'valid': False, 'message': 'Username can only contain letters, numbers, and underscores'}
    
    return {'valid': True, 'message': 'Valid username'}

def validate_stock_symbol(symbol: str) -> bool:
    """Validate stock symbol format"""
    if not symbol:
        return False
    
    # Basic validation: 1-5 uppercase letters
    return re.match(r'^[A-Z]{1,5}$', symbol.upper()) is not None

def format_currency(amount: float) -> str:
    """Format amount as currency"""
    return f"${amount:,.2f}"

def format_percentage(value: float) -> str:
    """Format value as percentage"""
    return f"{value:.2f}%"

def calculate_percentage_change(old_value: float, new_value: float) -> float:
    """Calculate percentage change between two values"""
    if old_value == 0:
        return 0
    return ((new_value - old_value) / old_value) * 100

def sanitize_input(text: str) -> str:
    """Sanitize user input"""
    if not text:
        return ""
    
    # Remove potentially harmful characters
    sanitized = re.sub(r'[<>"\']', '', text)
    return sanitized.strip()

def format_datetime(dt: datetime) -> str:
    """Format datetime for display"""
    return dt.strftime('%Y-%m-%d %H:%M:%S')

def validate_trade_amount(shares: int, price: float, balance: float) -> Dict[str, Any]:
    """Validate trade parameters"""
    if shares <= 0:
        return {'valid': False, 'message': 'Number of shares must be positive'}
    
    if price <= 0:
        return {'valid': False, 'message': 'Stock price must be positive'}
    
    total_cost = shares * price
    if total_cost > balance:
        return {
            'valid': False, 
            'message': f'Insufficient funds. Required: {format_currency(total_cost)}, Available: {format_currency(balance)}'
        }
    
    return {'valid': True, 'message': 'Valid trade parameters'}

def calculate_portfolio_metrics(holdings: list, current_prices: dict) -> Dict[str, float]:
    """Calculate portfolio performance metrics"""
    total_value = 0
    total_cost = 0
    
    for symbol, shares, avg_price in holdings:
        current_price = current_prices.get(symbol, avg_price)
        market_value = shares * current_price
        cost_basis = shares * avg_price
        
        total_value += market_value
        total_cost += cost_basis
    
    total_gain_loss = total_value - total_cost
    total_gain_loss_percent = calculate_percentage_change(total_cost, total_value) if total_cost > 0 else 0
    
    return {
        'total_value': total_value,
        'total_cost': total_cost,
        'total_gain_loss': total_gain_loss,
        'total_gain_loss_percent': total_gain_loss_percent
    }