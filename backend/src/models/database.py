import sqlite3
import os
from datetime import datetime
from typing import Optional, List, Tuple

class Database:
    def __init__(self, db_path: str = 'trading.db'):
        self.db_path = db_path
        self.init_db()
    
    def init_db(self):
        """Initialize database with required tables"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Users table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                email TEXT,
                balance REAL DEFAULT 100000,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Portfolio table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS portfolio (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                symbol TEXT NOT NULL,
                shares INTEGER NOT NULL,
                avg_price REAL NOT NULL,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users (id),
                UNIQUE(user_id, symbol)
            )
        ''')
        
        # Transactions table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS transactions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                symbol TEXT NOT NULL,
                type TEXT NOT NULL CHECK (type IN ('BUY', 'SELL')),
                shares INTEGER NOT NULL,
                price REAL NOT NULL,
                total_amount REAL NOT NULL,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users (id)
            )
        ''')
        
        # Watchlist table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS watchlist (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                symbol TEXT NOT NULL,
                added_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users (id),
                UNIQUE(user_id, symbol)
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def create_user(self, username: str, email: str = None, initial_balance: float = 100000) -> Optional[int]:
        """Create a new user"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        try:
            cursor.execute(
                'INSERT INTO users (username, email, balance) VALUES (?, ?, ?)', 
                (username, email, initial_balance)
            )
            user_id = cursor.lastrowid
            conn.commit()
            return user_id
        except sqlite3.IntegrityError:
            return None
        finally:
            conn.close()
    
    def get_user(self, username: str) -> Optional[Tuple]:
        """Get user by username"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM users WHERE username = ?', (username,))
        user = cursor.fetchone()
        conn.close()
        return user
    
    def get_user_by_id(self, user_id: int) -> Optional[Tuple]:
        """Get user by ID"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM users WHERE id = ?', (user_id,))
        user = cursor.fetchone()
        conn.close()
        return user
    
    def update_balance(self, user_id: int, new_balance: float):
        """Update user balance"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute(
            'UPDATE users SET balance = ?, updated_at = CURRENT_TIMESTAMP WHERE id = ?', 
            (new_balance, user_id)
        )
        conn.commit()
        conn.close()
    
    def add_transaction(self, user_id: int, symbol: str, transaction_type: str, 
                       shares: int, price: float, total_amount: float):
        """Add a transaction record"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO transactions (user_id, symbol, type, shares, price, total_amount)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (user_id, symbol, transaction_type, shares, price, total_amount))
        conn.commit()
        conn.close()
    
    def update_portfolio(self, user_id: int, symbol: str, shares: int, price: float):
        """Update portfolio holdings"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute(
            'SELECT shares, avg_price FROM portfolio WHERE user_id = ? AND symbol = ?', 
            (user_id, symbol)
        )
        existing = cursor.fetchone()
        
        if existing:
            current_shares, current_avg_price = existing
            new_shares = current_shares + shares
            
            if new_shares == 0:
                cursor.execute(
                    'DELETE FROM portfolio WHERE user_id = ? AND symbol = ?', 
                    (user_id, symbol)
                )
            elif new_shares > 0:
                # Calculate new average price
                if shares > 0:  # Buying more
                    total_cost = (current_shares * current_avg_price) + (shares * price)
                    new_avg_price = total_cost / new_shares
                else:  # Selling
                    new_avg_price = current_avg_price
                
                cursor.execute('''
                    UPDATE portfolio SET shares = ?, avg_price = ?, updated_at = CURRENT_TIMESTAMP
                    WHERE user_id = ? AND symbol = ?
                ''', (new_shares, new_avg_price, user_id, symbol))
        else:
            if shares > 0:
                cursor.execute('''
                    INSERT INTO portfolio (user_id, symbol, shares, avg_price)
                    VALUES (?, ?, ?, ?)
                ''', (user_id, symbol, shares, price))
        
        conn.commit()
        conn.close()
    
    def get_portfolio(self, user_id: int) -> List[Tuple]:
        """Get user's portfolio"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute(
            'SELECT symbol, shares, avg_price FROM portfolio WHERE user_id = ? AND shares > 0', 
            (user_id,)
        )
        portfolio = cursor.fetchall()
        conn.close()
        return portfolio
    
    def get_transactions(self, user_id: int, limit: int = 50) -> List[Tuple]:
        """Get user's transaction history"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('''
            SELECT symbol, type, shares, price, total_amount, timestamp 
            FROM transactions WHERE user_id = ? 
            ORDER BY timestamp DESC LIMIT ?
        ''', (user_id, limit))
        transactions = cursor.fetchall()
        conn.close()
        return transactions
    
    def add_to_watchlist(self, user_id: int, symbol: str) -> bool:
        """Add stock to watchlist"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        try:
            cursor.execute(
                'INSERT INTO watchlist (user_id, symbol) VALUES (?, ?)', 
                (user_id, symbol)
            )
            conn.commit()
            return True
        except sqlite3.IntegrityError:
            return False
        finally:
            conn.close()
    
    def remove_from_watchlist(self, user_id: int, symbol: str):
        """Remove stock from watchlist"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute(
            'DELETE FROM watchlist WHERE user_id = ? AND symbol = ?', 
            (user_id, symbol)
        )
        conn.commit()
        conn.close()
    
    def get_watchlist(self, user_id: int) -> List[str]:
        """Get user's watchlist"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute(
            'SELECT symbol FROM watchlist WHERE user_id = ? ORDER BY added_at DESC', 
            (user_id,)
        )
        watchlist = [row[0] for row in cursor.fetchall()]
        conn.close()
        return watchlist