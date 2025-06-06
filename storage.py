import pandas as pd
import sqlite3
from typing import Dict, List, Optional
from datetime import datetime
import os

class DataStorage:
    """
    Stores and retrieves market data.
    """
    
    def __init__(self, db_path: str = None):
        """
        Initialize the data storage.
        
        Args:
            db_path: The path to the SQLite database
        """
        if db_path is None:
            # Create a data directory if it doesn't exist
            data_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))), "data")
            os.makedirs(data_dir, exist_ok=True)
            db_path = os.path.join(data_dir, "market_data.db")
        
        self.conn = sqlite3.connect(db_path)
        self.create_tables()
    
    def create_tables(self):
        """
        Create the necessary tables.
        """
        cursor = self.conn.cursor()
        
        # Create symbols table
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS symbols (
            id INTEGER PRIMARY KEY,
            symbol TEXT UNIQUE,
            name TEXT,
            exchange TEXT
        )
        """)
        
        # Create data table
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS market_data (
            id INTEGER PRIMARY KEY,
            symbol_id INTEGER,
            date TEXT,
            open REAL,
            high REAL,
            low REAL,
            close REAL,
            adj_close REAL,
            volume INTEGER,
            FOREIGN KEY (symbol_id) REFERENCES symbols (id),
            UNIQUE (symbol_id, date)
        )
        """)
        
        self.conn.commit()
    
    def store_data(self, symbol: str, data: pd.DataFrame):
        """
        Store market data for a symbol.
        
        Args:
            symbol: The symbol
            data: The market data
        """
        cursor = self.conn.cursor()
        
        # Insert or update symbol
        cursor.execute(
            "INSERT OR IGNORE INTO symbols (symbol) VALUES (?)",
            (symbol,)
        )
        
        # Get symbol ID
        cursor.execute("SELECT id FROM symbols WHERE symbol = ?", (symbol,))
        symbol_id = cursor.fetchone()[0]
        
        # Insert market data
        for _, row in data.iterrows():
            cursor.execute(
                """
                INSERT OR REPLACE INTO market_data
                (symbol_id, date, open, high, low, close, adj_close, volume)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    symbol_id,
                    row["date"].strftime("%Y-%m-%d %H:%M:%S"),
                    row["open"],
                    row["high"],
                    row["low"],
                    row["close"],
                    row.get("adj_close", row["close"]),
                    row["volume"],
                )
            )
        
        self.conn.commit()
    
    def get_data(
        self,
        symbol: str,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
    ) -> pd.DataFrame:
        """
        Get market data for a symbol.
        
        Args:
            symbol: The symbol
            start_date: The start date
            end_date: The end date
            
        Returns:
            A pandas DataFrame with the market data
        """
        cursor = self.conn.cursor()
        
        # Get symbol ID
        cursor.execute("SELECT id FROM symbols WHERE symbol = ?", (symbol,))
        result = cursor.fetchone()
        
        if result is None:
            return pd.DataFrame()
        
        symbol_id = result[0]
        
        # Build query
        query = """
        SELECT date, open, high, low, close, adj_close, volume
        FROM market_data
        WHERE symbol_id = ?
        """
        params = [symbol_id]
        
        if start_date is not None:
            query += " AND date >= ?"
            params.append(start_date.strftime("%Y-%m-%d %H:%M:%S"))
        
        if end_date is not None:
            query += " AND date <= ?"
            params.append(end_date.strftime("%Y-%m-%d %H:%M:%S"))
        
        query += " ORDER BY date"
        
        # Execute query
        cursor.execute(query, params)
        rows = cursor.fetchall()
        
        # Create DataFrame
        data = pd.DataFrame(
            rows,
            columns=["date", "open", "high", "low", "close", "adj_close", "volume"]
        )
        
        # Convert Date column to datetime
        data["date"] = pd.to_datetime(data["date"])
        
        return data
    
    def close(self):
        """
        Close the database connection.
        """
        self.conn.close()

