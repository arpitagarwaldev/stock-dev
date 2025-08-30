import numpy as np
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import mean_squared_error
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, Dropout
import yfinance as yf
from datetime import datetime, timedelta
import pickle
import os

class StockPredictor:
    def __init__(self):
        self.model = None
        self.scaler = MinMaxScaler()
        self.sequence_length = 60
        self.model_path = 'models'
        self.ensure_model_dir()
    
    def ensure_model_dir(self):
        if not os.path.exists(self.model_path):
            os.makedirs(self.model_path)
    
    def get_stock_data(self, symbol, period='2y'):
        """Fetch stock data for training"""
        try:
            stock = yf.Ticker(symbol)
            data = stock.history(period=period)
            return data
        except Exception as e:
            print(f"Error fetching data for {symbol}: {e}")
            return None
    
    def prepare_data(self, data):
        """Prepare data for LSTM model"""
        # Use Close price and add technical indicators
        df = data.copy()
        df['MA_20'] = df['Close'].rolling(window=20).mean()
        df['MA_50'] = df['Close'].rolling(window=50).mean()
        df['RSI'] = self.calculate_rsi(df['Close'])
        df['Volume_MA'] = df['Volume'].rolling(window=20).mean()
        
        # Select features
        features = ['Close', 'Volume', 'MA_20', 'MA_50', 'RSI', 'Volume_MA']
        df = df[features].dropna()
        
        # Scale the data
        scaled_data = self.scaler.fit_transform(df)
        
        # Create sequences
        X, y = [], []
        for i in range(self.sequence_length, len(scaled_data)):
            X.append(scaled_data[i-self.sequence_length:i])
            y.append(scaled_data[i, 0])  # Predict Close price
        
        return np.array(X), np.array(y)
    
    def calculate_rsi(self, prices, period=14):
        """Calculate RSI indicator"""
        delta = prices.diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
        rs = gain / loss
        rsi = 100 - (100 / (1 + rs))
        return rsi
    
    def build_model(self, input_shape):
        """Build LSTM neural network"""
        model = Sequential([
            LSTM(50, return_sequences=True, input_shape=input_shape),
            Dropout(0.2),
            LSTM(50, return_sequences=True),
            Dropout(0.2),
            LSTM(50),
            Dropout(0.2),
            Dense(25),
            Dense(1)
        ])
        
        model.compile(optimizer='adam', loss='mean_squared_error')
        return model
    
    def train_model(self, symbol):
        """Train model for specific stock"""
        print(f"Training model for {symbol}...")
        
        # Get data
        data = self.get_stock_data(symbol)
        if data is None or len(data) < 100:
            return False
        
        # Prepare data
        X, y = self.prepare_data(data)
        if len(X) == 0:
            return False
        
        # Split data
        split = int(0.8 * len(X))
        X_train, X_test = X[:split], X[split:]
        y_train, y_test = y[:split], y[split:]
        
        # Build and train model
        self.model = self.build_model((X_train.shape[1], X_train.shape[2]))
        
        # Train with early stopping
        early_stop = tf.keras.callbacks.EarlyStopping(monitor='val_loss', patience=10)
        
        self.model.fit(
            X_train, y_train,
            batch_size=32,
            epochs=50,
            validation_data=(X_test, y_test),
            callbacks=[early_stop],
            verbose=0
        )
        
        # Save model and scaler
        model_file = f"{self.model_path}/{symbol}_model.h5"
        scaler_file = f"{self.model_path}/{symbol}_scaler.pkl"
        
        self.model.save(model_file)
        with open(scaler_file, 'wb') as f:
            pickle.dump(self.scaler, f)
        
        print(f"Model trained and saved for {symbol}")
        return True
    
    def load_model(self, symbol):
        """Load trained model for symbol"""
        model_file = f"{self.model_path}/{symbol}_model.h5"
        scaler_file = f"{self.model_path}/{symbol}_scaler.pkl"
        
        if os.path.exists(model_file) and os.path.exists(scaler_file):
            self.model = tf.keras.models.load_model(model_file)
            with open(scaler_file, 'rb') as f:
                self.scaler = pickle.load(f)
            return True
        return False
    
    def predict_trend(self, symbol, days=5):
        """Predict stock trend for next few days"""
        try:
            # Load or train model
            if not self.load_model(symbol):
                if not self.train_model(symbol):
                    return None
            
            # Get recent data
            data = self.get_stock_data(symbol, period='6mo')
            if data is None:
                return None
            
            # Prepare recent data
            df = data.copy()
            df['MA_20'] = df['Close'].rolling(window=20).mean()
            df['MA_50'] = df['Close'].rolling(window=50).mean()
            df['RSI'] = self.calculate_rsi(df['Close'])
            df['Volume_MA'] = df['Volume'].rolling(window=20).mean()
            
            features = ['Close', 'Volume', 'MA_20', 'MA_50', 'RSI', 'Volume_MA']
            df = df[features].dropna()
            
            if len(df) < self.sequence_length:
                return None
            
            # Scale recent data
            scaled_data = self.scaler.transform(df)
            
            # Get last sequence
            last_sequence = scaled_data[-self.sequence_length:].reshape(1, self.sequence_length, -1)
            
            # Predict next prices
            predictions = []
            current_sequence = last_sequence.copy()
            
            for _ in range(days):
                pred = self.model.predict(current_sequence, verbose=0)[0, 0]
                predictions.append(pred)
                
                # Update sequence for next prediction
                new_row = current_sequence[0, -1, :].copy()
                new_row[0] = pred  # Update close price
                new_row = new_row.reshape(1, 1, -1)
                current_sequence = np.concatenate([current_sequence[:, 1:, :], new_row], axis=1)
            
            # Inverse transform predictions
            dummy_array = np.zeros((len(predictions), scaled_data.shape[1]))
            dummy_array[:, 0] = predictions
            predicted_prices = self.scaler.inverse_transform(dummy_array)[:, 0]
            
            # Get current price
            current_price = df['Close'].iloc[-1]
            
            # Calculate trend
            future_price = predicted_prices[-1]
            trend_change = (future_price - current_price) / current_price * 100
            
            return {
                'symbol': symbol,
                'current_price': float(current_price),
                'predicted_price': float(future_price),
                'trend_change': float(trend_change),
                'prediction_days': days,
                'confidence': self.calculate_confidence(trend_change),
                'recommendation': self.get_recommendation(trend_change),
                'predicted_prices': [float(p) for p in predicted_prices]
            }
            
        except Exception as e:
            print(f"Prediction error for {symbol}: {e}")
            return None
    
    def calculate_confidence(self, trend_change):
        """Calculate confidence based on trend magnitude"""
        abs_change = abs(trend_change)
        if abs_change > 10:
            return 'High'
        elif abs_change > 5:
            return 'Medium'
        else:
            return 'Low'
    
    def get_recommendation(self, trend_change):
        """Get buy/sell recommendation"""
        if trend_change > 3:
            return 'BUY'
        elif trend_change < -3:
            return 'SELL'
        else:
            return 'HOLD'
    
    def get_multiple_predictions(self, symbols):
        """Get predictions for multiple symbols"""
        predictions = {}
        for symbol in symbols:
            pred = self.predict_trend(symbol)
            if pred:
                predictions[symbol] = pred
        return predictions