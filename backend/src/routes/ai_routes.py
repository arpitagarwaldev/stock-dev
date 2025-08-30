from flask import Blueprint, request, jsonify, session
from ..services.ai_predictor import StockPredictor
import threading

ai_bp = Blueprint('ai', __name__, url_prefix='/api/ai')
predictor = StockPredictor()

def require_auth():
    """Check if user is authenticated"""
    username = session.get('username')
    if not username:
        return None
    return username

@ai_bp.route('/predict/<symbol>', methods=['GET'])
def predict_stock(symbol):
    """Get AI prediction for a stock"""
    username = require_auth()
    if not username:
        return jsonify({'success': False, 'message': 'Authentication required'}), 401
    
    try:
        symbol = symbol.upper().strip()
        days = request.args.get('days', 5, type=int)
        
        if days < 1 or days > 30:
            days = 5
        
        # Run prediction in background to avoid timeout
        prediction = predictor.predict_trend(symbol, days)
        
        if prediction:
            return jsonify({'success': True, 'prediction': prediction})
        else:
            return jsonify({'success': False, 'message': 'Unable to generate prediction'}), 404
    
    except Exception as e:
        return jsonify({'success': False, 'message': 'Prediction failed'}), 500

@ai_bp.route('/batch-predict', methods=['POST'])
def batch_predict():
    """Get predictions for multiple stocks"""
    username = require_auth()
    if not username:
        return jsonify({'success': False, 'message': 'Authentication required'}), 401
    
    try:
        data = request.get_json()
        symbols = data.get('symbols', [])
        
        if not isinstance(symbols, list) or len(symbols) == 0:
            return jsonify({'success': False, 'message': 'Invalid symbols list'}), 400
        
        # Limit to 10 symbols to avoid timeout
        symbols = [s.upper().strip() for s in symbols[:10]]
        
        predictions = predictor.get_multiple_predictions(symbols)
        
        return jsonify({'success': True, 'predictions': predictions})
    
    except Exception as e:
        return jsonify({'success': False, 'message': 'Batch prediction failed'}), 500

@ai_bp.route('/recommendations', methods=['GET'])
def get_recommendations():
    """Get AI recommendations for popular stocks"""
    username = require_auth()
    if not username:
        return jsonify({'success': False, 'message': 'Authentication required'}), 401
    
    try:
        # Popular stocks for recommendations
        popular_stocks = ['AAPL', 'GOOGL', 'MSFT', 'AMZN', 'TSLA', 'META', 'NVDA']
        
        predictions = predictor.get_multiple_predictions(popular_stocks)
        
        # Sort by recommendation strength
        recommendations = []
        for symbol, pred in predictions.items():
            if pred['recommendation'] in ['BUY', 'SELL']:
                recommendations.append(pred)
        
        # Sort by trend change magnitude
        recommendations.sort(key=lambda x: abs(x['trend_change']), reverse=True)
        
        return jsonify({
            'success': True, 
            'recommendations': recommendations[:5]  # Top 5 recommendations
        })
    
    except Exception as e:
        return jsonify({'success': False, 'message': 'Failed to get recommendations'}), 500

@ai_bp.route('/train/<symbol>', methods=['POST'])
def train_model(symbol):
    """Train model for specific stock (admin feature)"""
    username = require_auth()
    if not username:
        return jsonify({'success': False, 'message': 'Authentication required'}), 401
    
    try:
        symbol = symbol.upper().strip()
        
        # Train model in background thread
        def train_async():
            predictor.train_model(symbol)
        
        thread = threading.Thread(target=train_async)
        thread.start()
        
        return jsonify({
            'success': True, 
            'message': f'Training started for {symbol}. This may take a few minutes.'
        })
    
    except Exception as e:
        return jsonify({'success': False, 'message': 'Training failed'}), 500