#!/usr/bin/env python3
"""
Script ya kupima utendaji wa bot ya biashara
"""

import os
import sys
import json
import unittest
from unittest.mock import patch, MagicMock
import logging

# Disable logging during tests
logging.disable(logging.CRITICAL)

# Add the current directory to the path so we can import the improved_scalper module
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Import the classes from the improved_scalper module
try:
    from improved_scalper import Config, MyfxbookAPI, MT5Handler, TradingStrategies, PerformanceTracker, TradingBot
except ImportError:
    print("Could not import from improved_scalper.py. Make sure the file exists in the current directory.")
    sys.exit(1)

class TestConfig(unittest.TestCase):
    """Test the Config class"""
    
    def setUp(self):
        """Set up test environment"""
        # Create a temporary .env file for testing
        with open(".env.test", "w") as f:
            f.write("""
MT5_LOGIN=123456
MT5_PASSWORD=test_password
MT5_SERVER=test_server
MYFXBOOK_EMAIL=test@example.com
MYFXBOOK_PASSWORD=test_password
SYMBOLS=EURUSD,GBPUSD
RISK_PERCENT=2.0
            """)
        
        # Create a temporary JSON config file for testing
        with open("config.test.json", "w") as f:
            json.dump({
                "mt5": {
                    "login": 654321,
                    "password": "json_password",
                    "server": "json_server"
                },
                "trading": {
                    "symbols": ["USDJPY", "GBPJPY"],
                    "risk_percent": 3.0
                }
            }, f)
    
    def tearDown(self):
        """Clean up test environment"""
        # Remove temporary files
        if os.path.exists(".env.test"):
            os.remove(".env.test")
        if os.path.exists("config.test.json"):
            os.remove("config.test.json")
    
    @patch('improved_scalper.load_dotenv')
    @patch('improved_scalper.os')
    def test_config_from_env(self, mock_os, mock_load_dotenv):
        """Test loading configuration from environment variables"""
        # Mock environment variables
        mock_os.getenv.side_effect = lambda key, default=None: {
            "MT5_LOGIN": "123456",
            "MT5_PASSWORD": "test_password",
            "MT5_SERVER": "test_server",
            "MYFXBOOK_EMAIL": "test@example.com",
            "MYFXBOOK_PASSWORD": "test_password",
            "SYMBOLS": "EURUSD,GBPUSD",
            "RISK_PERCENT": "2.0"
        }.get(key, default)
        
        # Create config instance
        config = Config()
        
        # Check if values are loaded correctly
        self.assertEqual(config.get("mt5", "login"), "123456")
        self.assertEqual(config.get("mt5", "password"), "test_password")
        self.assertEqual(config.get("mt5", "server"), "test_server")
        self.assertEqual(config.get("myfxbook", "email"), "test@example.com")
        self.assertEqual(config.get("trading", "symbols"), ["EURUSD", "GBPUSD"])
        self.assertEqual(config.get("trading", "risk_percent"), 2.0)
    
    @patch('improved_scalper.load_dotenv')
    @patch('improved_scalper.os')
    def test_config_from_json(self, mock_os, mock_load_dotenv):
        """Test loading configuration from JSON file"""
        # Mock os.path.exists to return True for the config file
        mock_os.path.exists.return_value = True
        
        # Mock open to return our test JSON data
        mock_open = unittest.mock.mock_open(read_data=json.dumps({
            "mt5": {
                "login": 654321,
                "password": "json_password",
                "server": "json_server"
            },
            "trading": {
                "symbols": ["USDJPY", "GBPJPY"],
                "risk_percent": 3.0
            }
        }))
        
        # Mock environment variables (these should be overridden by JSON)
        mock_os.getenv.side_effect = lambda key, default=None: {
            "MT5_LOGIN": "123456",
            "MT5_PASSWORD": "test_password",
            "MT5_SERVER": "test_server",
            "SYMBOLS": "EURUSD,GBPUSD",
            "RISK_PERCENT": "2.0"
        }.get(key, default)
        
        # Apply the mock to the built-in open function
        with patch('builtins.open', mock_open):
            # Create config instance with JSON file
            config = Config("config.test.json")
            
            # Check if JSON values override environment variables
            self.assertEqual(config.get("mt5", "login"), 654321)
            self.assertEqual(config.get("mt5", "password"), "json_password")
            self.assertEqual(config.get("mt5", "server"), "json_server")
            self.assertEqual(config.get("trading", "symbols"), ["USDJPY", "GBPJPY"])
            self.assertEqual(config.get("trading", "risk_percent"), 3.0)

class TestMyfxbookAPI(unittest.TestCase):
    """Test the MyfxbookAPI class"""
    
    def setUp(self):
        """Set up test environment"""
        # Create a mock config
        self.mock_config = MagicMock()
        self.mock_config.get.side_effect = lambda section, key=None: {
            ("myfxbook", "email"): "test@example.com",
            ("myfxbook", "password"): "test_password"
        }.get((section, key))
        
        # Create MyfxbookAPI instance
        self.api = MyfxbookAPI(self.mock_config)
    
    @patch('improved_scalper.requests.get')
    def test_login_success(self, mock_get):
        """Test successful login to Myfxbook"""
        # Mock successful response
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "error": False,
            "session": "test_session_id"
        }
        mock_get.return_value = mock_response
        
        # Call login method
        result = self.api.login()
        
        # Check if login was successful
        self.assertTrue(result)
        self.assertEqual(self.api.session_id, "test_session_id")
        
        # Check if the correct URL was called
        mock_get.assert_called_once()
        call_args = mock_get.call_args[0][0]
        self.assertIn("https://www.myfxbook.com/api/login.json", call_args)
        self.assertIn("test@example.com", call_args)
        self.assertIn("test_password", call_args)
    
    @patch('improved_scalper.requests.get')
    def test_login_failure(self, mock_get):
        """Test failed login to Myfxbook"""
        # Mock failed response
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "error": True,
            "message": "Invalid credentials"
        }
        mock_get.return_value = mock_response
        
        # Call login method
        result = self.api.login()
        
        # Check if login failed
        self.assertFalse(result)
        self.assertIsNone(self.api.session_id)
    
    @patch('improved_scalper.requests.get')
    def test_get_sentiment(self, mock_get):
        """Test getting sentiment data"""
        # Set session ID
        self.api.session_id = "test_session_id"
        
        # Mock successful response
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "symbols": [
                {
                    "name": "EURUSD",
                    "longPercentage": "60",
                    "shortPercentage": "40"
                },
                {
                    "name": "GBPUSD",
                    "longPercentage": "30",
                    "shortPercentage": "70"
                }
            ]
        }
        mock_get.return_value = mock_response
        
        # Call get_sentiment method
        result = self.api.get_sentiment("EURUSD")
        
        # Check if sentiment data is correct
        self.assertEqual(result["long"], 60.0)
        self.assertEqual(result["short"], 40.0)
        
        # Check if the correct URL was called
        mock_get.assert_called_once()
        call_args = mock_get.call_args[0][0]
        self.assertIn("https://www.myfxbook.com/api/get-community-outlook.json", call_args)
        self.assertIn("test_session_id", call_args)

class TestMT5Handler(unittest.TestCase):
    """Test the MT5Handler class"""
    
    def setUp(self):
        """Set up test environment"""
        # Create a mock config
        self.mock_config = MagicMock()
        self.mock_config.get.side_effect = lambda section, key=None: {
            ("mt5", "login"): 123456,
            ("mt5", "password"): "test_password",
            ("mt5", "server"): "test_server"
        }.get((section, key))
        
        # Create MT5Handler instance
        self.handler = MT5Handler(self.mock_config)
    
    @patch('improved_scalper.mt5')
    def test_connect_success(self, mock_mt5):
        """Test successful connection to MT5"""
        # Mock successful connection
        mock_mt5.initialize.return_value = True
        
        # Call connect method
        result = self.handler.connect()
        
        # Check if connection was successful
        self.assertTrue(result)
        self.assertTrue(self.handler.connected)
        
        # Check if MT5 was initialized with correct parameters
        mock_mt5.initialize.assert_called_once_with(
            login=123456,
            password="test_password",
            server="test_server"
        )
    
    @patch('improved_scalper.mt5')
    def test_connect_failure(self, mock_mt5):
        """Test failed connection to MT5"""
        # Mock failed connection
        mock_mt5.initialize.return_value = False
        mock_mt5.last_error.return_value = "Connection error"
        
        # Call connect method
        result = self.handler.connect()
        
        # Check if connection failed
        self.assertFalse(result)
        self.assertFalse(self.handler.connected)
    
    @patch('improved_scalper.mt5')
    def test_disconnect(self, mock_mt5):
        """Test disconnection from MT5"""
        # Set connected to True
        self.handler.connected = True
        
        # Call disconnect method
        self.handler.disconnect()
        
        # Check if disconnection was successful
        self.assertFalse(self.handler.connected)
        mock_mt5.shutdown.assert_called_once()
    
    @patch('improved_scalper.mt5')
    def test_get_account_info(self, mock_mt5):
        """Test getting account info"""
        # Set connected to True
        self.handler.connected = True
        
        # Mock account info
        mock_account_info = MagicMock()
        mock_account_info.balance = 10000
        mock_account_info.equity = 10500
        mock_account_info.margin = 1000
        mock_account_info.margin_free = 9500
        mock_account_info.leverage = 100
        mock_account_info.currency = "USD"
        mock_mt5.account_info.return_value = mock_account_info
        
        # Call get_account_info method
        result = self.handler.get_account_info()
        
        # Check if account info is correct
        self.assertEqual(result["balance"], 10000)
        self.assertEqual(result["equity"], 10500)
        self.assertEqual(result["margin"], 1000)
        self.assertEqual(result["free_margin"], 9500)
        self.assertEqual(result["leverage"], 100)
        self.assertEqual(result["currency"], "USD")

class TestTradingStrategies(unittest.TestCase):
    """Test the TradingStrategies class"""
    
    def setUp(self):
        """Set up test environment"""
        # Create sample data for testing
        import pandas as pd
        import numpy as np
        
        # Create sample data for testing
        dates = pd.date_range('2025-01-01', periods=100, freq='H')
        self.sample_data = pd.DataFrame({
            'time': dates,
            'open': np.random.normal(1.1, 0.01, 100),
            'high': np.random.normal(1.11, 0.01, 100),
            'low': np.random.normal(1.09, 0.01, 100),
            'close': np.random.normal(1.1, 0.01, 100),
            'tick_volume': np.random.randint(100, 1000, 100),
            'spread': np.random.randint(1, 10, 100),
            'real_volume': np.random.randint(1000, 10000, 100)
        })
        
        # Ensure high is always >= open and close
        self.sample_data['high'] = self.sample_data[['open', 'close', 'high']].max(axis=1)
        
        # Ensure low is always <= open and close
        self.sample_data['low'] = self.sample_data[['open', 'close', 'low']].min(axis=1)
        
        # Create some bullish and bearish candles
        for i in range(10, 90, 10):
            # Bullish candle
            self.sample_data.loc[i, 'open'] = 1.09
            self.sample_data.loc[i, 'close'] = 1.11
            self.sample_data.loc[i, 'high'] = 1.115
            self.sample_data.loc[i, 'low'] = 1.085
            
            # Bearish candle
            self.sample_data.loc[i+1, 'open'] = 1.11
            self.sample_data.loc[i+1, 'close'] = 1.09
            self.sample_data.loc[i+1, 'high'] = 1.115
            self.sample_data.loc[i+1, 'low'] = 1.085
    
    def test_has_fvg(self):
        """Test fair value gap detection"""
        # Create a fair value gap
        self.sample_data.loc[50, 'high'] = 1.12
        self.sample_data.loc[50, 'low'] = 1.11
        self.sample_data.loc[52, 'high'] = 1.15
        self.sample_data.loc[52, 'low'] = 1.13
        
        # Test bullish FVG
        result = TradingStrategies.has_fvg(self.sample_data, 51)
        self.assertTrue(result)
        
        # Create a bearish fair value gap
        self.sample_data.loc[60, 'high'] = 1.12
        self.sample_data.loc[60, 'low'] = 1.11
        self.sample_data.loc[62, 'high'] = 1.10
        self.sample_data.loc[62, 'low'] = 1.09
        
        # Test bearish FVG
        result = TradingStrategies.has_fvg(self.sample_data, 61)
        self.assertTrue(result)
        
        # Test no FVG
        result = TradingStrategies.has_fvg(self.sample_data, 30)
        self.assertFalse(result)
    
    def test_detect_order_block(self):
        """Test order block detection"""
        # Create a bullish order block
        self.sample_data.loc[70, 'open'] = 1.11
        self.sample_data.loc[70, 'close'] = 1.09  # Bearish candle
        self.sample_data.loc[70, 'high'] = 1.115
        self.sample_data.loc[70, 'low'] = 1.085
        
        self.sample_data.loc[71, 'open'] = 1.09
        self.sample_data.loc[71, 'close'] = 1.11  # Bullish candle
        self.sample_data.loc[71, 'high'] = 1.115
        self.sample_data.loc[71, 'low'] = 1.085
        
        # Create FVG
        self.sample_data.loc[69, 'high'] = 1.08
        self.sample_data.loc[69, 'low'] = 1.07
        self.sample_data.loc[71, 'high'] = 1.115
        self.sample_data.loc[71, 'low'] = 1.09
        
        # Test order block detection
        with patch.object(TradingStrategies, 'has_fvg', return_value=True):
            result = TradingStrategies.detect_order_block(self.sample_data.iloc[68:72])
            self.assertIsNotNone(result)
            self.assertEqual(result[0], 'bullish')

class TestPerformanceTracker(unittest.TestCase):
    """Test the PerformanceTracker class"""
    
    def setUp(self):
        """Set up test environment"""
        # Create a temporary file for testing
        self.test_file = "performance_test.json"
        
        # Create PerformanceTracker instance
        self.tracker = PerformanceTracker(self.test_file)
    
    def tearDown(self):
        """Clean up test environment"""
        # Remove temporary file
        if os.path.exists(self.test_file):
            os.remove(self.test_file)
    
    def test_add_trade(self):
        """Test adding a trade"""
        # Add a winning trade
        self.tracker.add_trade({
            "symbol": "EURUSD",
            "direction": "buy",
            "setup": "turtle_soup",
            "entry_time": "2025-01-01T10:00:00",
            "entry_price": 1.1000,
            "exit_price": 1.1100,
            "profit": 100.0
        })
        
        # Check if trade was added
        self.assertEqual(len(self.tracker.data["trades"]), 1)
        self.assertEqual(self.tracker.data["trades"][0]["symbol"], "EURUSD")
        
        # Check if stats were updated
        self.assertEqual(self.tracker.data["stats"]["total_trades"], 1)
        self.assertEqual(self.tracker.data["stats"]["winning_trades"], 1)
        
        # Add a losing trade
        self.tracker.add_trade({
            "symbol": "GBPUSD",
            "direction": "sell",
            "setup": "stop_hunt",
            "entry_time": "2025-01-01T11:00:00",
            "entry_price": 1.3000,
            "exit_price": 1.3100,
            "profit": -100.0
        })
        
        # Check if trade was added
        self.assertEqual(len(self.tracker.data["trades"]), 2)
        
        # Check if stats were updated
        self.assertEqual(self.tracker.data["stats"]["total_trades"], 2)
        self.assertEqual(self.tracker.data["stats"]["winning_trades"], 1)
        self.assertEqual(self.tracker.data["stats"]["losing_trades"], 1)
        self.assertEqual(self.tracker.data["stats"]["win_rate"], 50.0)

class TestTradingBot(unittest.TestCase):
    """Test the TradingBot class"""
    
    def setUp(self):
        """Set up test environment"""
        # Create a mock config
        self.mock_config = MagicMock()
        
        # Create TradingBot instance with mocked dependencies
        with patch('improved_scalper.MT5Handler'), \
             patch('improved_scalper.MyfxbookAPI'), \
             patch('improved_scalper.PerformanceTracker'):
            self.bot = TradingBot()
            self.bot.config = self.mock_config
    
    @patch('improved_scalper.MT5Handler')
    @patch('improved_scalper.MyfxbookAPI')
    def test_initialize(self, mock_myfxbook_api, mock_mt5_handler):
        """Test bot initialization"""
        # Mock MT5Handler.connect to return True
        self.bot.mt5_handler.connect.return_value = True
        
        # Mock MyfxbookAPI.login to return True
        self.bot.myfxbook_api.login.return_value = True
        
        # Call initialize method
        result = self.bot.initialize()
        
        # Check if initialization was successful
        self.assertTrue(result)
        self.bot.mt5_handler.connect.assert_called_once()
        self.bot.myfxbook_api.login.assert_called_once()
    
    @patch('improved_scalper.MT5Handler')
    @patch('improved_scalper.MyfxbookAPI')
    def test_initialize_mt5_failure(self, mock_myfxbook_api, mock_mt5_handler):
        """Test bot initialization with MT5 connection failure"""
        # Mock MT5Handler.connect to return False
        self.bot.mt5_handler.connect.return_value = False
        
        # Call initialize method
        result = self.bot.initialize()
        
        # Check if initialization failed
        self.assertFalse(result)
        self.bot.mt5_handler.connect.assert_called_once()
        self.bot.myfxbook_api.login.assert_not_called()
    
    def test_shutdown(self):
        """Test bot shutdown"""
        # Set running to True
        self.bot.running = True
        
        # Call shutdown method
        self.bot.shutdown()
        
        # Check if shutdown was successful
        self.assertFalse(self.bot.running)
        self.bot.mt5_handler.disconnect.assert_called_once()

if __name__ == "__main__":
    unittest.main()

