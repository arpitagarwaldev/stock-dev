import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
    DATABASE_PATH = os.getenv('DATABASE_PATH', 'trading.db')
    INITIAL_BALANCE = float(os.getenv('INITIAL_BALANCE', '100000'))
    
    # API Configuration
    ALPHA_VANTAGE_API_KEY = os.getenv('ALPHA_VANTAGE_API_KEY', 'demo')  # Free tier
    
    # Flask Configuration
    FLASK_ENV = os.getenv('FLASK_ENV', 'development')
    DEBUG = FLASK_ENV == 'development'
    
    # CORS Configuration
    CORS_ORIGINS = ["http://localhost:3000", "http://127.0.0.1:5500"]
    
    # WebSocket Configuration
    PRICE_UPDATE_INTERVAL = 5  # seconds