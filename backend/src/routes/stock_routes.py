from flask import Blueprint, request, jsonify
from ..services.stock_service import StockService

stock_bp = Blueprint('stocks', __name__, url_prefix='/api/stocks')
stock_service = StockService()

@stock_bp.route('/search', methods=['GET'])
def search_stocks():
    """Search for stocks"""
    try:
        query = request.args.get('q', '').strip()
        if len(query) < 1:
            return jsonify({'success': True, 'results': []})
        
        results = stock_service.search_stocks(query)
        return jsonify({'success': True, 'results': results})
    
    except Exception as e:
        return jsonify({'success': False, 'message': 'Search failed'}), 500

@stock_bp.route('/info/<symbol>', methods=['GET'])
def get_stock_info(symbol):
    """Get detailed stock information"""
    try:
        symbol = symbol.upper().strip()
        info = stock_service.get_stock_info(symbol)
        
        if info:
            return jsonify({'success': True, 'stock': info})
        else:
            return jsonify({'success': False, 'message': 'Stock not found'}), 404
    
    except Exception as e:
        return jsonify({'success': False, 'message': 'Failed to fetch stock info'}), 500

@stock_bp.route('/price/<symbol>', methods=['GET'])
def get_stock_price(symbol):
    """Get current stock price"""
    try:
        symbol = symbol.upper().strip()
        price = stock_service.get_stock_price(symbol)
        
        if price:
            return jsonify({'success': True, 'symbol': symbol, 'price': price})
        else:
            return jsonify({'success': False, 'message': 'Price not available'}), 404
    
    except Exception as e:
        return jsonify({'success': False, 'message': 'Failed to fetch price'}), 500

@stock_bp.route('/historical/<symbol>', methods=['GET'])
def get_historical_data(symbol):
    """Get historical stock data"""
    try:
        symbol = symbol.upper().strip()
        period = request.args.get('period', '1mo')
        
        # Validate period
        valid_periods = ['1d', '5d', '1mo', '3mo', '6mo', '1y', '2y', '5y', '10y', 'ytd', 'max']
        if period not in valid_periods:
            period = '1mo'
        
        data = stock_service.get_historical_data(symbol, period)
        return jsonify({'success': True, 'symbol': symbol, 'data': data})
    
    except Exception as e:
        return jsonify({'success': False, 'message': 'Failed to fetch historical data'}), 500

@stock_bp.route('/movers', methods=['GET'])
def get_market_movers():
    """Get market movers (gainers and losers)"""
    try:
        movers = stock_service.get_market_movers()
        return jsonify({'success': True, 'movers': movers})
    
    except Exception as e:
        return jsonify({'success': False, 'message': 'Failed to fetch market movers'}), 500

@stock_bp.route('/validate/<symbol>', methods=['GET'])
def validate_symbol(symbol):
    """Validate if a stock symbol exists"""
    try:
        symbol = symbol.upper().strip()
        is_valid = stock_service.validate_symbol(symbol)
        
        return jsonify({
            'success': True, 
            'symbol': symbol, 
            'valid': is_valid
        })
    
    except Exception as e:
        return jsonify({'success': False, 'message': 'Validation failed'}), 500

@stock_bp.route('/batch-prices', methods=['POST'])
def get_batch_prices():
    """Get prices for multiple symbols"""
    try:
        data = request.get_json()
        symbols = data.get('symbols', [])
        
        if not isinstance(symbols, list) or len(symbols) == 0:
            return jsonify({'success': False, 'message': 'Invalid symbols list'}), 400
        
        # Limit to 20 symbols to avoid rate limits
        symbols = [s.upper().strip() for s in symbols[:20]]
        prices = stock_service.get_multiple_prices(symbols)
        
        return jsonify({'success': True, 'prices': prices})
    
    except Exception as e:
        return jsonify({'success': False, 'message': 'Failed to fetch batch prices'}), 500