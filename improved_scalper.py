"""
Improved ICT Forex Trading Bot
Based on the original scalper.py with enhancements for:
- Security: Removed hardcoded credentials
- Risk Management: Dynamic position sizing
- Configuration: External config file
- Monitoring: Performance tracking
- Flexibility: More customizable parameters
"""

import MetaTrader5 as mt5
import pandas as pd
import requests
from datetime import datetime
import time as t
import json
import os
import logging
from dotenv import load_dotenv

# === SETUP LOGGING ===
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("trading_bot.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger("TradingBot")

# === CONFIGURATION ===
class Config:
    def __init__(self, config_file=None):
        # Load environment variables from .env file if it exists
        load_dotenv()
        
        # Default configuration
        self.config = {
            "mt5": {
                "login": os.getenv("MT5_LOGIN"),
                "password": os.getenv("MT5_PASSWORD"),
                "server": os.getenv("MT5_SERVER", "FBS-Demo")
            },
            "myfxbook": {
                "email": os.getenv("MYFXBOOK_EMAIL"),
                "password": os.getenv("MYFXBOOK_PASSWORD")
            },
            "trading": {
                "symbols": os.getenv("SYMBOLS", "GBPUSD,USDJPY,GBPJPY,EURUSD").split(","),
                "timeframe": mt5.TIMEFRAME_M5,
                "htf_timeframe": mt5.TIMEFRAME_M15,
                "risk_percent": float(os.getenv("RISK_PERCENT", "1.0")),
                "max_spread_pips": float(os.getenv("MAX_SPREAD_PIPS", "3.0")),
                "min_sentiment_threshold": float(os.getenv("MIN_SENTIMENT_THRESHOLD", "60.0")),
                "scan_interval": int(os.getenv("SCAN_INTERVAL", "60"))
            }
        }
        
        # Load from config file if provided
        if config_file and os.path.exists(config_file):
            with open(config_file, 'r') as f:
                file_config = json.load(f)
                self._update_dict(self.config, file_config)
    
    def _update_dict(self, d, u):
        for k, v in u.items():
            if isinstance(v, dict):
                d[k] = self._update_dict(d.get(k, {}), v)
            else:
                d[k] = v
        return d
    
    def get(self, section, key=None):
        if key:
            return self.config.get(section, {}).get(key)
        return self.config.get(section, {})

# === MYFXBOOK API ===
class MyfxbookAPI:
    def __init__(self, config):
        self.config = config
        self.session_id = None
    
    def login(self):
        email = self.config.get("myfxbook", "email")
        password = self.config.get("myfxbook", "password")
        
        if not email or not password:
            logger.error("Myfxbook credentials not found in configuration")
            return False
            
        url = f"https://www.myfxbook.com/api/login.json?email={email}&password={password}"
        try:
            res = requests.get(url)
            if res.status_code == 200 and res.json().get('error') == False:
                self.session_id = res.json()['session']
                logger.info("Successfully logged in to Myfxbook")
                return True
            else:
                logger.error(f"Failed to login to Myfxbook: {res.text}")
                return False
        except Exception as e:
            logger.error(f"Error logging in to Myfxbook: {str(e)}")
            return False
    
    def get_sentiment(self, symbol):
        if not self.session_id:
            logger.warning("Not logged in to Myfxbook, attempting login")
            if not self.login():
                return None
                
        url = f"https://www.myfxbook.com/api/get-community-outlook.json?session={self.session_id}"
        try:
            res = requests.get(url)
            if res.status_code != 200:
                logger.error(f"Failed to get sentiment data: {res.text}")
                return None
                
            data = res.json().get('symbols', [])
            for sym in data:
                if sym['name'].upper() == symbol.upper():
                    return {
                        "long": float(sym['longPercentage']),
                        "short": float(sym['shortPercentage'])
                    }
            logger.warning(f"Symbol {symbol} not found in sentiment data")
            return None
        except Exception as e:
            logger.error(f"Error getting sentiment data: {str(e)}")
            return None

# === MT5 TRADING ===
class MT5Handler:
    def __init__(self, config):
        self.config = config
        self.connected = False
        
    def connect(self):
        login = self.config.get("mt5", "login")
        password = self.config.get("mt5", "password")
        server = self.config.get("mt5", "server")
        
        if not login or not password:
            logger.error("MT5 credentials not found in configuration")
            return False
            
        try:
            # Convert login to integer if it's a string
            if isinstance(login, str) and login.isdigit():
                login = int(login)
                
            if not mt5.initialize(login=login, password=password, server=server):
                logger.error(f"MT5 connection failed: {mt5.last_error()}")
                return False
                
            logger.info("Connected to MT5")
            self.connected = True
            return True
        except Exception as e:
            logger.error(f"Error connecting to MT5: {str(e)}")
            return False
    
    def disconnect(self):
        if self.connected:
            mt5.shutdown()
            logger.info("Disconnected from MT5")
            self.connected = False
    
    def get_account_info(self):
        if not self.connected:
            logger.warning("Not connected to MT5")
            return None
            
        try:
            account_info = mt5.account_info()
            if account_info:
                return {
                    "balance": account_info.balance,
                    "equity": account_info.equity,
                    "margin": account_info.margin,
                    "free_margin": account_info.margin_free,
                    "leverage": account_info.leverage,
                    "currency": account_info.currency
                }
            return None
        except Exception as e:
            logger.error(f"Error getting account info: {str(e)}")
            return None
    
    def get_pip(self, symbol):
        """Get pip value for a symbol"""
        try:
            symbol_info = mt5.symbol_info(symbol)
            if not symbol_info:
                logger.error(f"Symbol {symbol} not found")
                return None
            return 0.0001 if symbol_info.digits >= 4 else 0.01
        except Exception as e:
            logger.error(f"Error getting pip value for {symbol}: {str(e)}")
            return None
    
    def get_data(self, symbol, timeframe, bars=500):
        """Get historical price data"""
        if not self.connected:
            logger.warning("Not connected to MT5")
            return None
            
        try:
            rates = mt5.copy_rates_from_pos(symbol, timeframe, 0, bars)
            if rates is None or len(rates) == 0:
                logger.warning(f"No data returned for {symbol} on timeframe {timeframe}")
                return None
                
            df = pd.DataFrame(rates)
            df['time'] = pd.to_datetime(df['time'], unit='s')
            return df
        except Exception as e:
            logger.error(f"Error getting data for {symbol}: {str(e)}")
            return None
    
    def calculate_position_size(self, symbol, risk_percent, stop_loss_pips):
        """Calculate position size based on risk percentage"""
        try:
            account_info = self.get_account_info()
            if not account_info:
                return 0.01  # Default minimum
                
            symbol_info = mt5.symbol_info(symbol)
            if not symbol_info:
                return 0.01
                
            # Get account balance and calculate risk amount
            balance = account_info["balance"]
            risk_amount = balance * (risk_percent / 100)
            
            # Calculate pip value
            pip_value = self.get_pip(symbol)
            if not pip_value:
                return 0.01
                
            # Get contract size and current price
            contract_size = symbol_info.trade_contract_size
            current_price = (symbol_info.bid + symbol_info.ask) / 2
            
            # Calculate position size
            if symbol_info.digits >= 4:  # Forex pairs typically have 4 or 5 digits
                pip_value_in_account_currency = (pip_value * contract_size) / current_price
            else:  # For other instruments
                pip_value_in_account_currency = pip_value * contract_size
                
            if stop_loss_pips <= 0 or pip_value_in_account_currency <= 0:
                return 0.01
                
            position_size = risk_amount / (stop_loss_pips * pip_value_in_account_currency)
            
            # Round down to nearest 0.01
            position_size = max(0.01, round(position_size * 100) / 100)
            
            # Ensure position size is within allowed limits
            min_volume = symbol_info.volume_min
            max_volume = symbol_info.volume_max
            step = symbol_info.volume_step
            
            # Adjust to step size
            position_size = round(position_size / step) * step
            
            # Ensure within limits
            position_size = max(min_volume, min(position_size, max_volume))
            
            logger.info(f"Calculated position size for {symbol}: {position_size} lots (Risk: {risk_percent}%, SL: {stop_loss_pips} pips)")
            return position_size
            
        except Exception as e:
            logger.error(f"Error calculating position size: {str(e)}")
            return 0.01  # Default minimum
    
    def check_spread(self, symbol, max_spread_pips):
        """Check if spread is acceptable"""
        try:
            symbol_info = mt5.symbol_info(symbol)
            if not symbol_info:
                return False
                
            spread_points = symbol_info.spread
            pip = self.get_pip(symbol)
            if not pip:
                return False
                
            spread_pips = spread_points * pip
            
            if spread_pips > max_spread_pips:
                logger.warning(f"Spread for {symbol} is too high: {spread_pips} pips > {max_spread_pips} pips")
                return False
                
            return True
        except Exception as e:
            logger.error(f"Error checking spread for {symbol}: {str(e)}")
            return False
    
    def place_order(self, symbol, direction, ob_zone, df, risk_percent=1.0):
        """Place a trading order"""
        if not self.connected:
            logger.warning("Not connected to MT5")
            return False
            
        try:
            tick = mt5.symbol_info_tick(symbol)
            info = mt5.symbol_info(symbol)
            if not tick or info is None:
                logger.error(f"Could not get symbol info for {symbol}")
                return False
                
            pip = self.get_pip(symbol)
            if not pip:
                return False
                
            ob_low, ob_high = ob_zone[1], ob_zone[2]
            
            # Calculate entry, stop loss and take profit
            entry = round(ob_low + pip, info.digits) if direction == "buy" else round(ob_high - pip, info.digits)
            sl = round(ob_low - 2 * pip, info.digits) if direction == "buy" else round(ob_high + 2 * pip, info.digits)
            
            # Calculate take profit based on recent highs/lows
            if direction == "buy":
                tp = round(df['high'][-20:-1].max() + 5 * pip, info.digits)
            else:
                tp = round(df['low'][-20:-1].min() - 5 * pip, info.digits)
            
            # Calculate stop loss in pips
            sl_pips = abs(entry - sl) / pip
            
            # Calculate position size based on risk
            lot = self.calculate_position_size(symbol, risk_percent, sl_pips)
            
            # Determine order type
            order_type = mt5.ORDER_TYPE_BUY_LIMIT if direction == "buy" else mt5.ORDER_TYPE_SELL_LIMIT
            
            # Prepare order request
            request = {
                "action": mt5.TRADE_ACTION_PENDING,
                "symbol": symbol,
                "volume": lot,
                "type": order_type,
                "price": entry,
                "sl": sl,
                "tp": tp,
                "deviation": 10,
                "magic": 112233,
                "comment": "ICT Entry",
                "type_time": mt5.ORDER_TIME_GTC,
                "type_filling": info.filling_mode,
            }
            
            # Send order
            result = mt5.order_send(request)
            if result and result.retcode == mt5.TRADE_RETCODE_DONE:
                logger.info(f"ORDER {direction.upper()} {symbol} @ {entry} | SL: {sl} | TP: {tp} | Lot: {lot}")
                return True
            else:
                logger.error(f"ORDER FAILED for {symbol}: {result.comment if result else 'Unknown error'}")
                return False
                
        except Exception as e:
            logger.error(f"Error placing order for {symbol}: {str(e)}")
            return False

# === TRADING STRATEGIES ===
class TradingStrategies:
    @staticmethod
    def get_htf_bias(mt5_handler, symbol, htf=mt5.TIMEFRAME_M15):
        """Get higher timeframe bias"""
        df = mt5_handler.get_data(symbol, htf, 150)
        if df is None or len(df) < 30:
            return None
            
        highs = []
        lows = []
        
        # Find swing highs and lows
        for i in range(2, len(df) - 2):
            if df['high'].iloc[i] > df['high'].iloc[i - 1] and df['high'].iloc[i] > df['high'].iloc[i + 1]:
                highs.append(df['high'].iloc[i])
            if df['low'].iloc[i] < df['low'].iloc[i - 1] and df['low'].iloc[i] < df['low'].iloc[i + 1]:
                lows.append(df['low'].iloc[i])
                
        if len(highs) < 2 or len(lows) < 2:
            return None
            
        # Get the last two highs and lows
        hh1, hh2 = highs[-1], highs[-2]
        ll1, ll2 = lows[-1], lows[-2]
        
        # Determine market structure
        if hh1 > hh2 and ll1 > ll2:
            return "bullish"
        elif hh1 < hh2 and ll1 < ll2:
            return "bearish"
        elif hh1 > hh2 and ll1 < ll2:
            return "choch_bullish"  # Change of character bullish
        elif hh1 < hh2 and ll1 > ll2:
            return "choch_bearish"  # Change of character bearish
            
        return None
    
    @staticmethod
    def has_fvg(df, i):
        """Check for fair value gap"""
        if i < 2 or i + 1 >= len(df):
            return False
            
        prev = df.iloc[i - 1]
        next_candle = df.iloc[i + 1]
        
        # Check for bullish or bearish FVG
        return next_candle['low'] > prev['high'] or next_candle['high'] < prev['low']
    
    @staticmethod
    def detect_order_block(df):
        """Detect order blocks"""
        for i in range(len(df) - 3, 2, -1):
            c = df.iloc[i]
            next_c = df.iloc[i + 1]
            
            # Bullish order block
            if c['close'] < c['open'] and next_c['close'] > next_c['open'] and TradingStrategies.has_fvg(df, i):
                return ('bullish', c['low'], c['high'], c['time'])
                
            # Bearish order block
            if c['close'] > c['open'] and next_c['close'] < next_c['open'] and TradingStrategies.has_fvg(df, i):
                return ('bearish', c['low'], c['high'], c['time'])
                
        return None
    
    @staticmethod
    def detect_turtle_soup(df):
        """Detect turtle soup pattern"""
        if len(df) < 21:
            return None
            
        prev = df.iloc[-2]
        last = df.iloc[-1]
        swing_low = df['low'][-21:-1].min()
        swing_high = df['high'][-21:-1].max()
        
        if prev['low'] < swing_low and last['low'] > prev['low']:
            return "buy"
        elif prev['high'] > swing_high and last['high'] < prev['high']:
            return "sell"
            
        return None
    
    @staticmethod
    def detect_sh_bms_rto(df):
        """Detect swing high break market structure return to origin"""
        if len(df) < 10:
            return None
            
        prev = df.iloc[-2]
        last = df.iloc[-1]
        
        if prev['low'] < df['low'][-10:-2].min() and last['close'] > prev['high']:
            return "buy"
        elif prev['high'] > df['high'][-10:-2].max() and last['close'] < prev['low']:
            return "sell"
            
        return None
    
    @staticmethod
    def detect_sms_bms_rto(df):
        """Detect swing market structure break market structure return to origin"""
        if len(df) < 10:
            return None
            
        highs = df['high']
        lows = df['low']
        prev = df.iloc[-2]
        last = df.iloc[-1]
        
        if prev['high'] > highs[-10:-2].max() and last['close'] < prev['low']:
            return "sell"
        elif prev['low'] < lows[-10:-2].min() and last['close'] > prev['high']:
            return "buy"
            
        return None
    
    @staticmethod
    def detect_stop_hunt(df):
        """Detect stop hunt pattern"""
        if len(df) < 20:
            return None
            
        recent_high = df['high'][-20:-2].max()
        recent_low = df['low'][-20:-2].min()
        prev = df.iloc[-2]
        last = df.iloc[-1]
        
        if prev['high'] > recent_high and last['close'] < prev['low']:
            return "sell"
        if prev['low'] < recent_low and last['close'] > prev['high']:
            return "buy"
            
        return None
    
    @staticmethod
    def detect_retail_trap(df):
        """Detect retail trap pattern"""
        if len(df) < 10:
            return None
            
        high = df['high'][-10:-2].max()
        low = df['low'][-10:-2].min()
        last = df.iloc[-1]
        prev = df.iloc[-2]
        
        if last['high'] > high and last['close'] < prev['low']:
            return "sell"
        if last['low'] < low and last['close'] > prev['high']:
            return "buy"
            
        return None

# === PERFORMANCE TRACKING ===
class PerformanceTracker:
    def __init__(self, file_path="performance.json"):
        self.file_path = file_path
        self.data = self._load_data()
    
    def _load_data(self):
        """Load performance data from file"""
        if os.path.exists(self.file_path):
            try:
                with open(self.file_path, 'r') as f:
                    return json.load(f)
            except Exception as e:
                logger.error(f"Error loading performance data: {str(e)}")
        
        # Default structure
        return {
            "trades": [],
            "stats": {
                "total_trades": 0,
                "winning_trades": 0,
                "losing_trades": 0,
                "win_rate": 0,
                "profit_factor": 0,
                "total_profit": 0,
                "max_drawdown": 0
            }
        }
    
    def _save_data(self):
        """Save performance data to file"""
        try:
            with open(self.file_path, 'w') as f:
                json.dump(self.data, f, indent=4)
        except Exception as e:
            logger.error(f"Error saving performance data: {str(e)}")
    
    def add_trade(self, trade_info):
        """Add a new trade to the performance tracker"""
        self.data["trades"].append(trade_info)
        self._update_stats()
        self._save_data()
    
    def _update_stats(self):
        """Update performance statistics"""
        trades = self.data["trades"]
        stats = self.data["stats"]
        
        stats["total_trades"] = len(trades)
        
        if not trades:
            return
            
        # Calculate basic stats
        winning_trades = [t for t in trades if t.get("profit", 0) > 0]
        losing_trades = [t for t in trades if t.get("profit", 0) <= 0]
        
        stats["winning_trades"] = len(winning_trades)
        stats["losing_trades"] = len(losing_trades)
        
        if stats["total_trades"] > 0:
            stats["win_rate"] = stats["winning_trades"] / stats["total_trades"] * 100
        
        # Calculate profit factor
        total_profit = sum(t.get("profit", 0) for t in winning_trades)
        total_loss = abs(sum(t.get("profit", 0) for t in losing_trades))
        
        stats["total_profit"] = total_profit - total_loss
        
        if total_loss > 0:
            stats["profit_factor"] = total_profit / total_loss
        else:
            stats["profit_factor"] = total_profit if total_profit > 0 else 0
        
        # Calculate drawdown (simplified)
        balance_curve = []
        current_balance = 0
        
        for trade in trades:
            current_balance += trade.get("profit", 0)
            balance_curve.append(current_balance)
        
        if balance_curve:
            peak = 0
            max_dd = 0
            
            for balance in balance_curve:
                if balance > peak:
                    peak = balance
                dd = peak - balance
                if dd > max_dd:
                    max_dd = dd
            
            stats["max_drawdown"] = max_dd

# === MAIN TRADING BOT ===
class TradingBot:
    def __init__(self, config_file=None):
        self.config = Config(config_file)
        self.mt5_handler = MT5Handler(self.config)
        self.myfxbook_api = MyfxbookAPI(self.config)
        self.performance_tracker = PerformanceTracker()
        self.running = False
    
    def initialize(self):
        """Initialize connections and prepare for trading"""
        logger.info("Initializing trading bot...")
        
        # Connect to MT5
        if not self.mt5_handler.connect():
            logger.error("Failed to connect to MT5, cannot continue")
            return False
        
        # Login to Myfxbook
        if not self.myfxbook_api.login():
            logger.warning("Failed to login to Myfxbook, will continue without sentiment data")
        
        logger.info("Trading bot initialized successfully")
        return True
    
    def shutdown(self):
        """Shutdown the bot and close connections"""
        logger.info("Shutting down trading bot...")
        self.running = False
        self.mt5_handler.disconnect()
        logger.info("Trading bot shutdown complete")
    
    def run(self):
        """Run the trading bot main loop"""
        if not self.initialize():
            return
        
        self.running = True
        logger.info("Starting trading bot main loop")
        
        # Get configuration
        symbols = self.config.get("trading", "symbols")
        timeframe = self.config.get("trading", "timeframe")
        htf_timeframe = self.config.get("trading", "htf_timeframe")
        risk_percent = self.config.get("trading", "risk_percent")
        max_spread_pips = self.config.get("trading", "max_spread_pips")
        min_sentiment_threshold = self.config.get("trading", "min_sentiment_threshold")
        scan_interval = self.config.get("trading", "scan_interval")
        
        logger.info(f"Trading configuration: {len(symbols)} symbols, {risk_percent}% risk, {scan_interval}s interval")
        
        try:
            while self.running:
                for symbol in symbols:
                    logger.info(f"Analyzing {symbol}...")
                    
                    # Check if spread is acceptable
                    if not self.mt5_handler.check_spread(symbol, max_spread_pips):
                        continue
                    
                    # Get price data
                    df = self.mt5_handler.get_data(symbol, timeframe)
                    if df is None or len(df) < 30:
                        logger.warning(f"Insufficient data for {symbol}, skipping")
                        continue
                    
                    # Get sentiment data
                    sentiment = self.myfxbook_api.get_sentiment(symbol)
                    if not sentiment:
                        logger.warning(f"No sentiment data for {symbol}, skipping")
                        continue
                    
                    # Determine contrarian direction based on sentiment
                    contrarian = None
                    if sentiment['long'] >= min_sentiment_threshold:
                        contrarian = "sell"
                        logger.info(f"{symbol} sentiment: {sentiment['long']}% long - contrarian SELL signal")
                    elif sentiment['short'] >= min_sentiment_threshold:
                        contrarian = "buy"
                        logger.info(f"{symbol} sentiment: {sentiment['short']}% short - contrarian BUY signal")
                    else:
                        logger.info(f"{symbol} sentiment neutral: {sentiment['long']}% long, {sentiment['short']}% short")
                        continue
                    
                    # Get higher timeframe bias
                    bias = TradingStrategies.get_htf_bias(self.mt5_handler, symbol, htf_timeframe)
                    choch = bias and bias.startswith("choch")
                    
                    if bias:
                        logger.info(f"{symbol} HTF bias: {bias}")
                    else:
                        logger.warning(f"Could not determine HTF bias for {symbol}, skipping")
                        continue
                    
                    # Check for trading setups
                    setup = direction = None
                    strategy_functions = [
                        TradingStrategies.detect_turtle_soup,
                        TradingStrategies.detect_sh_bms_rto,
                        TradingStrategies.detect_sms_bms_rto,
                        TradingStrategies.detect_stop_hunt,
                        TradingStrategies.detect_retail_trap
                    ]
                    
                    for func in strategy_functions:
                        result = func(df)
                        if result:
                            direction = result
                            setup = func.__name__
                            logger.info(f"{symbol} setup detected: {setup} - {direction}")
                            break
                    
                    # Check if direction matches contrarian view
                    if not direction:
                        logger.info(f"{symbol} no valid setup detected")
                        continue
                        
                    if direction != contrarian:
                        logger.info(f"{symbol} setup direction ({direction}) doesn't match sentiment ({contrarian})")
                        continue
                    
                    # Find order block
                    ob = TradingStrategies.detect_order_block(df)
                    if not ob:
                        logger.info(f"{symbol} no order block found")
                        continue
                    
                    logger.info(f"{symbol} order block found: {ob[0]} at {ob[3]}")
                    
                    # Validate setup with bias and order block
                    valid = (
                        (direction == "buy" and ob[0] == "bullish" and "bullish" in bias) or
                        (direction == "sell" and ob[0] == "bearish" and "bearish" in bias) or
                        choch
                    )
                    
                    if valid:
                        logger.info(f"{symbol} VALID SETUP: {setup} | Direction: {direction} | Bias: {bias}")
                        
                        # Place order
                        if self.mt5_handler.place_order(symbol, direction, ob, df, risk_percent):
                            # Record trade for performance tracking
                            trade_info = {
                                "symbol": symbol,
                                "direction": direction,
                                "setup": setup,
                                "entry_time": datetime.now().isoformat(),
                                "entry_price": ob[1] if direction == "buy" else ob[2],
                                "order_block": {
                                    "low": ob[1],
                                    "high": ob[2],
                                    "time": ob[3].isoformat() if isinstance(ob[3], pd.Timestamp) else ob[3]
                                }
                            }
                            self.performance_tracker.add_trade(trade_info)
                    else:
                        logger.info(f"{symbol} setup invalid: OB/Bias mismatch")
                
                # Wait before next scan
                logger.info(f"Scan complete, waiting {scan_interval} seconds...")
                t.sleep(scan_interval)
                
        except KeyboardInterrupt:
            logger.info("Trading bot stopped by user")
        except Exception as e:
            logger.error(f"Error in trading bot main loop: {str(e)}")
        finally:
            self.shutdown()

# === ENTRY POINT ===
if __name__ == "__main__":
    # Create .env file template if it doesn't exist
    if not os.path.exists(".env"):
        with open(".env", "w") as f:
            f.write("""# MT5 Credentials
MT5_LOGIN=
MT5_PASSWORD=
MT5_SERVER=FBS-Demo

# Myfxbook Credentials
MYFXBOOK_EMAIL=
MYFXBOOK_PASSWORD=

# Trading Parameters
SYMBOLS=GBPUSD,USDJPY,GBPJPY,EURUSD
RISK_PERCENT=1.0
MAX_SPREAD_PIPS=3.0
MIN_SENTIMENT_THRESHOLD=60.0
SCAN_INTERVAL=60
""")
        logger.info("Created .env template file. Please fill in your credentials before running the bot.")
    
    # Start the bot
    bot = TradingBot()
    bot.run()

