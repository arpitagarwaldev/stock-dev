from flask import Blueprint, request, jsonify, session
from ..services.trading_service import TradingService

auth_bp = Blueprint('auth', __name__, url_prefix='/api/auth')
trading_service = TradingService()

@auth_bp.route('/register', methods=['POST'])
def register():
    """Register a new user"""
    try:
        data = request.get_json()
        username = data.get('username', '').strip()
        email = data.get('email', '').strip()
        
        if not username:
            return jsonify({'success': False, 'message': 'Username is required'}), 400
        
        if len(username) < 3:
            return jsonify({'success': False, 'message': 'Username must be at least 3 characters'}), 400
        
        user_id = trading_service.create_user(username, email)
        if user_id:
            session['username'] = username
            session['user_id'] = user_id
            return jsonify({
                'success': True, 
                'message': 'User registered successfully',
                'user': {'username': username, 'user_id': user_id}
            })
        else:
            return jsonify({'success': False, 'message': 'Username already exists'}), 409
    
    except Exception as e:
        return jsonify({'success': False, 'message': 'Registration failed'}), 500

@auth_bp.route('/login', methods=['POST'])
def login():
    """Login user"""
    try:
        data = request.get_json()
        username = data.get('username', '').strip()
        
        if not username:
            return jsonify({'success': False, 'message': 'Username is required'}), 400
        
        user_info = trading_service.authenticate_user(username)
        if user_info:
            session['username'] = username
            session['user_id'] = user_info['user_id']
            return jsonify({'success': True, 'user': user_info})
        else:
            return jsonify({'success': False, 'message': 'User not found'}), 404
    
    except Exception as e:
        return jsonify({'success': False, 'message': 'Login failed'}), 500

@auth_bp.route('/logout', methods=['POST'])
def logout():
    """Logout user"""
    session.clear()
    return jsonify({'success': True, 'message': 'Logged out successfully'})

@auth_bp.route('/me', methods=['GET'])
def get_current_user():
    """Get current logged-in user info"""
    username = session.get('username')
    if not username:
        return jsonify({'success': False, 'message': 'Not authenticated'}), 401
    
    user_info = trading_service.authenticate_user(username)
    if user_info:
        return jsonify({'success': True, 'user': user_info})
    else:
        session.clear()
        return jsonify({'success': False, 'message': 'User not found'}), 404