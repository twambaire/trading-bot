# Mchoro wa Madarasa ya Trading Bot

```
+------------------------+
|       TradingBot       |
+------------------------+
| - config: Config       |
| - mt5_handler: MT5Handler |
| - myfxbook_api: MyfxbookAPI |
| - performance_tracker: PerformanceTracker |
| - running: bool        |
+------------------------+
| + initialize(): bool   |
| + shutdown(): void     |
| + run(): void          |
+------------------------+
           ^
           |
           | uses
           |
+------------------------+     +------------------------+
|        Config          |     |     MT5Handler         |
+------------------------+     +------------------------+
| - config: dict         |     | - config: Config       |
+------------------------+     | - connected: bool      |
| + __init__(config_file)|     +------------------------+
| + get(section, key)    |     | + connect(): bool      |
| + _update_dict(d, u)   |     | + disconnect(): void   |
+------------------------+     | + get_account_info()   |
                               | + get_pip(symbol)      |
                               | + get_data(symbol, timeframe) |
                               | + calculate_position_size() |
                               | + check_spread()       |
                               | + place_order()        |
                               +------------------------+
                                          ^
                                          |
                                          | uses
                                          |
+------------------------+     +------------------------+
|     MyfxbookAPI        |     |   TradingStrategies   |
+------------------------+     +------------------------+
| - config: Config       |     | + get_htf_bias()      |
| - session_id: str      |     | + has_fvg()           |
+------------------------+     | + detect_order_block() |
| + login(): bool        |     | + detect_turtle_soup()|
| + get_sentiment(symbol)|     | + detect_sh_bms_rto() |
+------------------------+     | + detect_sms_bms_rto()|
                               | + detect_stop_hunt()  |
                               | + detect_retail_trap()|
                               +------------------------+
                                          ^
                                          |
                                          | uses
                                          |
+------------------------+
|  PerformanceTracker    |
+------------------------+
| - file_path: str       |
| - data: dict           |
+------------------------+
| + add_trade(trade_info)|
| + _update_stats()      |
| + _save_data()         |
| + _load_data()         |
+------------------------+
```

## Maelezo ya Madarasa

### 1. TradingBot
Darasa kuu linalosimamia mzunguko wa bot na kuunganisha vipengele vingine.

### 2. Config
Darasa linalosimamia usanidi wa bot kutoka kwa faili ya `.env` au JSON.

### 3. MT5Handler
Darasa linalosimamia muunganisho na MetaTrader5 na kutekeleza amri za biashara.

### 4. MyfxbookAPI
Darasa linalosimamia muunganisho na Myfxbook na kupata data ya hisia za soko.

### 5. TradingStrategies
Darasa linalotekeleza mikakati mbalimbali ya biashara. Limeundwa kama darasa la static methods.

### 6. PerformanceTracker
Darasa linalofuatilia na kuhifadhi takwimu za utendaji wa bot.

## Mahusiano ya Madarasa

1. **TradingBot** inatumia:
   - **Config** kwa usanidi
   - **MT5Handler** kwa muunganisho na MT5
   - **MyfxbookAPI** kwa data ya hisia za soko
   - **TradingStrategies** kwa mikakati ya biashara
   - **PerformanceTracker** kwa ufuatiliaji wa utendaji

2. **MT5Handler** inatumia:
   - **Config** kwa usanidi wa MT5
   - **TradingStrategies** kwa utambuzi wa ishara za biashara

3. **MyfxbookAPI** inatumia:
   - **Config** kwa usanidi wa Myfxbook

4. **PerformanceTracker** inatumia:
   - Faili ya JSON kwa kuhifadhi takwimu

