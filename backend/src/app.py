from flask import Flask, jsonify
from flask_socketio import SocketIO, emit
from flask_cors import CORS
import threading
import time
import sys
import os

# Add the backend directory to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config.settings import Config
from routes.auth_routes import auth_bp
from routes.trading_routes import trading_bp
from routes.stock_routes import stock_bp
from routes.ai_routes import ai_bp
from services.stock_service import StockService

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    # Initialize extensions
    CORS(app, origins=Config.CORS_ORIGINS, supports_credentials=True)
    socketio = SocketIO(app, cors_allowed_origins=Config.CORS_ORIGINS)
    
    # Register blueprints
    app.register_blueprint(auth_bp)
    app.register_blueprint(trading_bp)
    app.register_blueprint(stock_bp)
    app.register_blueprint(ai_bp)
    
    # Global variables for real-time updates
    active_symbols = set()
    stock_service = StockService()
    
    @app.route('/')
    def index():
        return jsonify({
            'message': 'Stock Trading Simulator API',
            'version': '1.0.0',
            'status': 'running'
        })
    
    @app.route('/api/health')
    def health_check():
        return jsonify({'status': 'healthy', 'timestamp': time.time()})
    
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({'success': False, 'message': 'Endpoint not found'}), 404
    
    @app.errorhandler(500)
    def internal_error(error):
        return jsonify({'success': False, 'message': 'Internal server error'}), 500
    
    # WebSocket events
    @socketio.on('connect')
    def handle_connect():
        print('Client connected')
        emit('connected', {'message': 'Connected to stock price updates'})
    
    @socketio.on('disconnect')
    def handle_disconnect():
        print('Client disconnected')
    
    @socketio.on('subscribe_stock')
    def handle_subscribe(data):
        symbol = data.get('symbol', '').upper()
        if symbol and stock_service.validate_symbol(symbol):
            active_symbols.add(symbol)
            emit('subscribed', {'symbol': symbol, 'message': f'Subscribed to {symbol} updates'})
            print(f'Client subscribed to {symbol}')
        else:
            emit('error', {'message': 'Invalid stock symbol'})
    
    @socketio.on('unsubscribe_stock')
    def handle_unsubscribe(data):
        symbol = data.get('symbol', '').upper()
        if symbol in active_symbols:
            active_symbols.remove(symbol)
            emit('unsubscribed', {'symbol': symbol, 'message': f'Unsubscribed from {symbol} updates'})
            print(f'Client unsubscribed from {symbol}')
    
    @socketio.on('get_active_symbols')
    def handle_get_active_symbols():
        emit('active_symbols', {'symbols': list(active_symbols)})
    
    def price_updater():
        """Background thread to send real-time price updates"""
        print('Price updater thread started')
        while True:
            try:
                if active_symbols:
                    print(f'Updating prices for {len(active_symbols)} symbols')
                    for symbol in list(active_symbols):
                        try:
                            price = stock_service.get_stock_price(symbol)
                            if price:
                                socketio.emit('price_update', {
                                    'symbol': symbol,
                                    'price': round(price, 2),
                                    'timestamp': time.time()
                                })
                        except Exception as e:
                            print(f"Error updating price for {symbol}: {e}")
                            # Remove problematic symbol
                            active_symbols.discard(symbol)
                
                time.sleep(Config.PRICE_UPDATE_INTERVAL)
            except Exception as e:
                print(f"Error in price updater: {e}")
                time.sleep(10)  # Wait longer on error
    
    # Start price update thread
    price_update_thread = threading.Thread(target=price_updater, daemon=True)
    price_update_thread.start()
    
    return app, socketio

if __name__ == '__main__':
    app, socketio = create_app()
    print("Starting Stock Trading Simulator API...")
    print(f"Debug mode: {app.config['DEBUG']}")
    print("Available endpoints:")
    print("  GET  /                     - API info")
    print("  GET  /api/health           - Health check")
    print("  POST /api/auth/register    - Register user")
    print("  POST /api/auth/login       - Login user")
    print("  GET  /api/trading/portfolio - Get portfolio")
    print("  POST /api/trading/buy      - Buy stocks")
    print("  POST /api/trading/sell     - Sell stocks")
    print("  GET  /api/stocks/search    - Search stocks")
    print("  GET  /api/stocks/info/<symbol> - Get stock info")
    print("  GET  /api/ai/predict/<symbol> - Get AI prediction")
    print("  GET  /api/ai/recommendations - Get AI recommendations")
    
    socketio.run(app, debug=app.config['DEBUG'], host='0.0.0.0', port=5000)