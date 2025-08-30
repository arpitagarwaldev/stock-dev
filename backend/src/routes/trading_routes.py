from flask import Blueprint, request, jsonify, session
from ..services.trading_service import TradingService

trading_bp = Blueprint('trading', __name__, url_prefix='/api/trading')
trading_service = TradingService()

def require_auth():
    """Check if user is authenticated"""
    username = session.get('username')
    if not username:
        return None
    return username

@trading_bp.route('/portfolio', methods=['GET'])
def get_portfolio():
    """Get user's portfolio"""
    username = require_auth()
    if not username:
        return jsonify({'success': False, 'message': 'Authentication required'}), 401
    
    try:
        portfolio = trading_service.get_user_portfolio(username)
        if portfolio:
            return jsonify({'success': True, 'portfolio': portfolio})
        else:
            return jsonify({'success': False, 'message': 'User not found'}), 404
    except Exception as e:
        return jsonify({'success': False, 'message': 'Failed to fetch portfolio'}), 500

@trading_bp.route('/buy', methods=['POST'])
def buy_stock():
    """Buy stocks"""
    username = require_auth()
    if not username:
        return jsonify({'success': False, 'message': 'Authentication required'}), 401
    
    try:
        data = request.get_json()
        symbol = data.get('symbol', '').strip().upper()
        shares = data.get('shares', 0)
        
        if not symbol:
            return jsonify({'success': False, 'message': 'Stock symbol is required'}), 400
        
        try:
            shares = int(shares)
        except (ValueError, TypeError):
            return jsonify({'success': False, 'message': 'Invalid number of shares'}), 400
        
        if shares <= 0:
            return jsonify({'success': False, 'message': 'Number of shares must be positive'}), 400
        
        result = trading_service.buy_stock(username, symbol, shares)
        
        if result['success']:
            return jsonify(result)
        else:
            return jsonify(result), 400
    
    except Exception as e:
        return jsonify({'success': False, 'message': 'Buy order failed'}), 500

@trading_bp.route('/sell', methods=['POST'])
def sell_stock():
    """Sell stocks"""
    username = require_auth()
    if not username:
        return jsonify({'success': False, 'message': 'Authentication required'}), 401
    
    try:
        data = request.get_json()
        symbol = data.get('symbol', '').strip().upper()
        shares = data.get('shares', 0)
        
        if not symbol:
            return jsonify({'success': False, 'message': 'Stock symbol is required'}), 400
        
        try:
            shares = int(shares)
        except (ValueError, TypeError):
            return jsonify({'success': False, 'message': 'Invalid number of shares'}), 400
        
        if shares <= 0:
            return jsonify({'success': False, 'message': 'Number of shares must be positive'}), 400
        
        result = trading_service.sell_stock(username, symbol, shares)
        
        if result['success']:
            return jsonify(result)
        else:
            return jsonify(result), 400
    
    except Exception as e:
        return jsonify({'success': False, 'message': 'Sell order failed'}), 500

@trading_bp.route('/transactions', methods=['GET'])
def get_transactions():
    """Get transaction history"""
    username = require_auth()
    if not username:
        return jsonify({'success': False, 'message': 'Authentication required'}), 401
    
    try:
        limit = request.args.get('limit', 50, type=int)
        transactions = trading_service.get_transaction_history(username, limit)
        return jsonify({'success': True, 'transactions': transactions})
    except Exception as e:
        return jsonify({'success': False, 'message': 'Failed to fetch transactions'}), 500

@trading_bp.route('/watchlist', methods=['GET'])
def get_watchlist():
    """Get user's watchlist"""
    username = require_auth()
    if not username:
        return jsonify({'success': False, 'message': 'Authentication required'}), 401
    
    try:
        watchlist = trading_service.get_watchlist(username)
        return jsonify({'success': True, 'watchlist': watchlist})
    except Exception as e:
        return jsonify({'success': False, 'message': 'Failed to fetch watchlist'}), 500

@trading_bp.route('/watchlist', methods=['POST'])
def add_to_watchlist():
    """Add stock to watchlist"""
    username = require_auth()
    if not username:
        return jsonify({'success': False, 'message': 'Authentication required'}), 401
    
    try:
        data = request.get_json()
        symbol = data.get('symbol', '').strip().upper()
        
        if not symbol:
            return jsonify({'success': False, 'message': 'Stock symbol is required'}), 400
        
        result = trading_service.add_to_watchlist(username, symbol)
        
        if result['success']:
            return jsonify(result)
        else:
            return jsonify(result), 400
    
    except Exception as e:
        return jsonify({'success': False, 'message': 'Failed to add to watchlist'}), 500

@trading_bp.route('/watchlist/<symbol>', methods=['DELETE'])
def remove_from_watchlist(symbol):
    """Remove stock from watchlist"""
    username = require_auth()
    if not username:
        return jsonify({'success': False, 'message': 'Authentication required'}), 401
    
    try:
        result = trading_service.remove_from_watchlist(username, symbol)
        return jsonify(result)
    except Exception as e:
        return jsonify({'success': False, 'message': 'Failed to remove from watchlist'}), 500