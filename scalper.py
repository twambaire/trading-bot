# === FULL ICT BOT with Myfxbook Direct Login Credentials (TEMP USE ONLY) ===
import MetaTrader5 as mt5
import pandas as pd
import requests
from datetime import datetime
import time as t
import json

# === LOGIN FUNCTIONS ===
def get_myfxbook_credentials():
    return "njokianne029@gmail.com", "Test1234!"

def login_myfxbook_direct():
    email, password = get_myfxbook_credentials()
    url = f"https://www.myfxbook.com/api/login.json?email={email}&password={password}"
    res = requests.get(url)
    if res.status_code == 200 and res.json().get('error') == False:
        print("✅ Logged in to Myfxbook")
        return res.json()['session']
    else:
        print("❌ Failed to login to Myfxbook")
        print("🔍 Response:", res.text)
        return None

def get_sentiment(session_id, symbol):
    url = f"https://www.myfxbook.com/api/get-community-outlook.json?session={session_id}"
    res = requests.get(url)
    if res.status_code != 200:
        return None
    data = res.json().get('symbols', [])
    for sym in data:
        if sym['name'].upper() == symbol.upper():
            return {
                "long": float(sym['longPercentage']),
                "short": float(sym['shortPercentage'])
            }
    return None

# === CONNECT TO MT5 ===
def connect():
    login = 102143034
    password = "2g[89P$R"
    server = "FBS-Demo"
    if not mt5.initialize(login=login, password=password, server=server):
        print("❌ MT5 connection failed")
        print(mt5.last_error())
        return False
    print("✅ Connected to MT5")
    return True

# === GET DATA, PIP ===
def get_pip(symbol):
    return 0.0001 if mt5.symbol_info(symbol).digits >= 4 else 0.01

def get_data(symbol, timeframe, bars=500):
    rates = mt5.copy_rates_from_pos(symbol, timeframe, 0, bars)
    if rates is None or len(rates) == 0:
        return None
    df = pd.DataFrame(rates)
    df['time'] = pd.to_datetime(df['time'], unit='s')
    return df

# === HTF BIAS ===
def get_htf_bias(symbol, htf=mt5.TIMEFRAME_M15):
    df = get_data(symbol, htf, 150)
    if df is None or len(df) < 30:
        return None
    highs = []
    lows = []
    for i in range(2, len(df) - 2):
        if df['high'].iloc[i] > df['high'].iloc[i - 1] and df['high'].iloc[i] > df['high'].iloc[i + 1]:
            highs.append(df['high'].iloc[i])
        if df['low'].iloc[i] < df['low'].iloc[i - 1] and df['low'].iloc[i] < df['low'].iloc[i + 1]:
            lows.append(df['low'].iloc[i])
    if len(highs) < 2 or len(lows) < 2:
        return None
    hh1, hh2 = highs[-1], highs[-2]
    ll1, ll2 = lows[-1], lows[-2]
    if hh1 > hh2 and ll1 > ll2:
        return "bullish"
    elif hh1 < hh2 and ll1 < ll2:
        return "bearish"
    elif hh1 > hh2 and ll1 < ll2:
        return "choch_bullish"
    elif hh1 < hh2 and ll1 > ll2:
        return "choch_bearish"
    return None

# === ORDER BLOCK + FVG ===
def has_fvg(df, i):
    if i < 2 or i + 1 >= len(df):
        return False
    prev = df.iloc[i - 1]
    next_candle = df.iloc[i + 1]
    return next_candle['low'] > prev['high'] or next_candle['high'] < prev['low']

def detect_order_block(df):
    for i in range(len(df) - 3, 2, -1):
        c = df.iloc[i]
        next_c = df.iloc[i + 1]
        if c['close'] < c['open'] and next_c['close'] > next_c['open'] and has_fvg(df, i):
            return ('bullish', c['low'], c['high'], c['time'])
        if c['close'] > c['open'] and next_c['close'] < next_c['open'] and has_fvg(df, i):
            return ('bearish', c['low'], c['high'], c['time'])
    return None

# === SETUPS ===
def detect_turtle_soup(df):
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

def detect_sh_bms_rto(df):
    if len(df) < 10:
        return None
    prev = df.iloc[-2]
    last = df.iloc[-1]
    if prev['low'] < df['low'][-10:-2].min() and last['close'] > prev['high']:
        return "buy"
    elif prev['high'] > df['high'][-10:-2].max() and last['close'] < prev['low']:
        return "sell"
    return None

def detect_sms_bms_rto(df):
    highs = df['high']
    lows = df['low']
    prev = df.iloc[-2]
    last = df.iloc[-1]
    if prev['high'] > highs[-10:-2].max() and last['close'] < prev['low']:
        return "sell"
    elif prev['low'] < lows[-10:-2].min() and last['close'] > prev['high']:
        return "buy"
    return None

def detect_stop_hunt(df):
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

def detect_retail_trap(df):
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

# === PLACE ORDER ===
def place_order(symbol, direction, ob_zone, df):
    tick = mt5.symbol_info_tick(symbol)
    info = mt5.symbol_info(symbol)
    if not tick or info is None:
        return
    pip = get_pip(symbol)
    ob_low, ob_high = ob_zone[1], ob_zone[2]
    entry = round(ob_low + pip, info.digits) if direction == "buy" else round(ob_high - pip, info.digits)
    sl = round(ob_low - 2 * pip, info.digits) if direction == "buy" else round(ob_high + 2 * pip, info.digits)
    tp = round(df['high'][-20:-1].max(), info.digits) if direction == "buy" else round(df['low'][-20:-1].min(), info.digits)
    lot = 0.01
    order_type = mt5.ORDER_TYPE_BUY_LIMIT if direction == "buy" else mt5.ORDER_TYPE_SELL_LIMIT
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
    result = mt5.order_send(request)
    if result and result.retcode == mt5.TRADE_RETCODE_DONE:
        print(f"✅ ORDER {direction.upper()} {symbol} @ {entry} | SL: {sl} | TP: {tp}")
    else:
        print(f"❌ ORDER FAILED for {symbol}: {result}")

# === RUN BOT ===
def run_bot(symbols, session):
    timeframe = mt5.TIMEFRAME_M5
    while True:
        for symbol in symbols:
            df = get_data(symbol, timeframe)
            if df is None or len(df) < 30:
                continue
            sentiment = get_sentiment(session, symbol)
            if not sentiment:
                continue

            contrarian = None
            if sentiment['long'] >= 60:
                contrarian = "sell"
            elif sentiment['short'] >= 60:
                contrarian = "buy"

            if not contrarian:
                print(f"⚠️ {symbol} skipped (neutral sentiment)")
                continue

            bias = get_htf_bias(symbol)
            choch = bias.startswith("choch") if bias else False
            setup = direction = None

            for func in [
                detect_turtle_soup,
                detect_sh_bms_rto,
                detect_sms_bms_rto,
                detect_stop_hunt,
                detect_retail_trap
            ]:
                result = func(df)
                if result:
                    direction = result
                    setup = func.__name__
                    break

            if not direction or direction != contrarian:
                print(f"❌ {symbol} no valid setup or sentiment mismatch")
                continue

            ob = detect_order_block(df)
            if not ob:
                print(f"⛔ {symbol} no OB found")
                continue

            valid = (
                (direction == "buy" and ob[0] == "bullish" and "bullish" in bias) or
                (direction == "sell" and ob[0] == "bearish" and "bearish" in bias) or
                choch
            )

            if valid:
                print(f"🎯 {symbol} | Setup: {setup} | Direction: {direction.upper()} | Bias: {bias}")
                place_order(symbol, direction, ob, df)
            else:
                print(f"❌ {symbol} | OB/Bias mismatch")

        t.sleep(60)

# === START ===
if __name__ == "__main__":
    session = login_myfxbook_direct()
    if session and connect():
        run_bot(["GBPUSD", "USDJPY", "GBPJPY"], session)

