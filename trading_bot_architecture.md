# Muundo wa Usanifu wa Trading Bot

## 1. Muhtasari wa Usanifu

Bot ya biashara ya forex iliyoboreshwa imeundwa kwa kutumia usanifu wa modular ambao unatenganisha majukumu mbalimbali katika vipengele tofauti. Usanifu huu unaruhusu urahisi wa matengenezo, upanuzi, na upimaji.

### 1.1 Malengo ya Usanifu

- **Utenganishaji wa Majukumu**: Kila kipengele kina jukumu maalum
- **Usanidi Rahisi**: Mabadiliko ya usanidi yanaweza kufanywa bila kubadilisha code
- **Usimamizi wa Hatari**: Usimamizi wa hatari uliojumuishwa kwa ajili ya usalama wa mtaji
- **Ufuatiliaji wa Utendaji**: Kufuatilia na kuhifadhi takwimu za utendaji
- **Urahisi wa Upanuzi**: Rahisi kuongeza mikakati mipya ya biashara

## 2. Muundo wa Jumla

Bot imeundwa kwa kutumia usanifu wa object-oriented na ina vipengele vikuu vifuatavyo:

```
+----------------+      +----------------+      +----------------+
|                |      |                |      |                |
|  TradingBot    |----->|  MT5Handler    |----->|  MetaTrader5   |
|                |      |                |      |                |
+----------------+      +----------------+      +----------------+
        |                      ^
        |                      |
        v                      |
+----------------+      +----------------+      +----------------+
|                |      |                |      |                |
|  MyfxbookAPI   |----->|  Requests      |----->|  Myfxbook      |
|                |      |                |      |                |
+----------------+      +----------------+      +----------------+
        |
        |
        v
+----------------+      +----------------+
|                |      |                |
|  Config        |<-----|  .env / JSON   |
|                |      |                |
+----------------+      +----------------+
        |
        |
        v
+----------------+      +----------------+
|                |      |                |
|  Performance   |----->|  JSON File     |
|  Tracker       |      |                |
+----------------+      +----------------+
        |
        |
        v
+----------------+
|                |
|  Trading       |
|  Strategies    |
|                |
+----------------+
```

## 3. Vipengele Vikuu

### 3.1 TradingBot

Kipengele kikuu kinachosimamia mzunguko wa bot na kuunganisha vipengele vingine.

**Majukumu**:
- Kuanzisha na kusimamia muunganisho na MT5 na Myfxbook
- Kusimamia mzunguko mkuu wa bot
- Kuunganisha mikakati ya biashara na utekelezaji wa amri
- Kusimamia usanidi wa bot

**Vigezo Vikuu**:
- `config`: Usanidi wa bot
- `mt5_handler`: Msimamizi wa MT5
- `myfxbook_api`: API ya Myfxbook
- `performance_tracker`: Mfuatiliaji wa utendaji

**Njia Kuu**:
- `initialize()`: Kuanzisha muunganisho na kuandaa bot
- `run()`: Kuendesha mzunguko mkuu wa bot
- `shutdown()`: Kufunga muunganisho na kusimamisha bot

### 3.2 MT5Handler

Kipengele kinachosimamia muunganisho na MetaTrader5 na kutekeleza amri za biashara.

**Majukumu**:
- Kuunganisha na MT5
- Kupata data ya bei
- Kuweka amri za biashara
- Kukokotoa saizi ya nafasi kulingana na usimamizi wa hatari

**Vigezo Vikuu**:
- `config`: Usanidi wa MT5
- `connected`: Hali ya muunganisho

**Njia Kuu**:
- `connect()`: Kuunganisha na MT5
- `disconnect()`: Kufunga muunganisho na MT5
- `get_data()`: Kupata data ya bei
- `place_order()`: Kuweka amri ya biashara
- `calculate_position_size()`: Kukokotoa saizi ya nafasi kulingana na hatari

### 3.3 MyfxbookAPI

Kipengele kinachosimamia muunganisho na Myfxbook na kupata data ya hisia za soko.

**Majukumu**:
- Kuingia kwenye Myfxbook
- Kupata data ya hisia za soko

**Vigezo Vikuu**:
- `config`: Usanidi wa Myfxbook
- `session_id`: Kitambulisho cha kikao cha Myfxbook

**Njia Kuu**:
- `login()`: Kuingia kwenye Myfxbook
- `get_sentiment()`: Kupata data ya hisia za soko kwa jozi ya sarafu

### 3.4 Config

Kipengele kinachosimamia usanidi wa bot kutoka kwa faili ya `.env` au JSON.

**Majukumu**:
- Kupakia usanidi kutoka kwa faili ya `.env`
- Kupakia usanidi kutoka kwa faili ya JSON
- Kutoa usanidi kwa vipengele vingine

**Vigezo Vikuu**:
- `config`: Kamusi ya usanidi

**Njia Kuu**:
- `get()`: Kupata thamani ya usanidi
- `_update_dict()`: Kusasisha kamusi ya usanidi

### 3.5 TradingStrategies

Kipengele kinachotekeleza mikakati mbalimbali ya biashara.

**Majukumu**:
- Kutekeleza mikakati ya biashara
- Kutambua ishara za biashara

**Njia Kuu**:
- `get_htf_bias()`: Kupata mwelekeo wa muda mrefu
- `detect_order_block()`: Kutambua maeneo ya order block
- `detect_turtle_soup()`: Kutambua mkakati wa turtle soup
- `detect_stop_hunt()`: Kutambua mkakati wa stop hunt
- `detect_retail_trap()`: Kutambua mkakati wa retail trap
- `detect_sh_bms_rto()`: Kutambua mkakati wa swing high break market structure return to origin
- `detect_sms_bms_rto()`: Kutambua mkakati wa swing market structure break market structure return to origin

### 3.6 PerformanceTracker

Kipengele kinachofuatilia na kuhifadhi takwimu za utendaji wa bot.

**Majukumu**:
- Kuhifadhi takwimu za biashara
- Kukokotoa takwimu za utendaji
- Kuhifadhi takwimu kwenye faili

**Vigezo Vikuu**:
- `file_path`: Njia ya faili ya takwimu
- `data`: Takwimu za utendaji

**Njia Kuu**:
- `add_trade()`: Kuongeza biashara mpya
- `_update_stats()`: Kusasisha takwimu za utendaji
- `_save_data()`: Kuhifadhi takwimu kwenye faili
- `_load_data()`: Kupakia takwimu kutoka kwa faili

## 4. Mtiririko wa Data

### 4.1 Mtiririko wa Msingi

1. **Usanidi**:
   - Bot inapakia usanidi kutoka kwa faili ya `.env` au JSON
   - Usanidi unatumika kuunganisha na MT5 na Myfxbook

2. **Uchambuzi wa Soko**:
   - Bot inapata data ya bei kutoka kwa MT5
   - Bot inapata data ya hisia za soko kutoka kwa Myfxbook
   - Bot inachambuza data kwa kutumia mikakati ya biashara

3. **Maamuzi ya Biashara**:
   - Bot inaamua kufanya biashara kulingana na ishara za mikakati
   - Bot inakokotoa saizi ya nafasi kulingana na usimamizi wa hatari
   - Bot inaweka amri ya biashara kupitia MT5

4. **Ufuatiliaji wa Utendaji**:
   - Bot inahifadhi takwimu za biashara
   - Bot inakokotoa takwimu za utendaji
   - Bot inahifadhi takwimu kwenye faili

### 4.2 Mtiririko wa Maamuzi ya Biashara

```
+----------------+      +----------------+      +----------------+
|                |      |                |      |                |
|  Sentiment     |----->|  HTF Bias      |----->|  Setup         |
|  Analysis      |      |  Analysis      |      |  Detection     |
|                |      |                |      |                |
+----------------+      +----------------+      +----------------+
                                                       |
                                                       |
                                                       v
+----------------+      +----------------+      +----------------+
|                |      |                |      |                |
|  Order         |<-----|  Validation    |<-----|  Order Block   |
|  Execution     |      |                |      |  Detection     |
|                |      |                |      |                |
+----------------+      +----------------+      +----------------+
```

1. **Uchambuzi wa Hisia**:
   - Kupata hisia za soko kutoka kwa Myfxbook
   - Kuamua mwelekeo wa kinyume (contrarian direction)

2. **Uchambuzi wa HTF Bias**:
   - Kupata mwelekeo wa muda mrefu
   - Kutambua mabadiliko ya muundo wa soko

3. **Utambuzi wa Setup**:
   - Kutumia mikakati mbalimbali kutambua ishara za biashara
   - Kuamua mwelekeo wa biashara

4. **Utambuzi wa Order Block**:
   - Kutambua maeneo ya order block
   - Kuamua bei ya kuingia, stop-loss, na take-profit

5. **Uthibitishaji**:
   - Kuthibitisha kuwa mwelekeo wa biashara unalingana na mwelekeo wa kinyume
   - Kuthibitisha kuwa order block inaendana na mwelekeo wa biashara
   - Kuthibitisha kuwa mwelekeo wa biashara unaendana na HTF bias

6. **Utekelezaji wa Amri**:
   - Kukokotoa saizi ya nafasi kulingana na usimamizi wa hatari
   - Kuweka amri ya biashara kupitia MT5

## 5. Usimamizi wa Hatari

### 5.1 Kukokotoa Saizi ya Nafasi

Bot inakokotoa saizi ya nafasi kulingana na:

1. **Asilimia ya Hatari**:
   - Asilimia ya mtaji inayoweza kupotea kwa biashara moja
   - Inaweza kubadilishwa kupitia usanidi

2. **Umbali wa Stop-Loss**:
   - Umbali kutoka kwa bei ya kuingia hadi kwa stop-loss
   - Inakokotolewa kulingana na order block

3. **Thamani ya Pip**:
   - Thamani ya pip kwa jozi ya sarafu
   - Inakokotolewa kulingana na digits za jozi ya sarafu

4. **Saizi ya Nafasi**:
   - Inakokotolewa kwa kutumia formula:
     ```
     position_size = (balance * risk_percent) / (stop_loss_pips * pip_value)
     ```

### 5.2 Usimamizi wa Spread

Bot inachunguza spread kabla ya kuweka amri:

1. **Kiwango cha Juu cha Spread**:
   - Kiwango cha juu cha spread kinachokubalika
   - Inaweza kubadilishwa kupitia usanidi

2. **Kuepuka Spread Kubwa**:
   - Bot haitaweka amri ikiwa spread ni kubwa zaidi ya kiwango cha juu
   - Inasaidia kuepuka gharama kubwa za biashara

## 6. Mifumo ya Usanidi

### 6.1 Faili ya .env

Bot inatumia faili ya `.env` kwa usanidi wa msingi:

```
# MT5 Credentials
MT5_LOGIN=123456789
MT5_PASSWORD=your_password
MT5_SERVER=your_broker_server

# Myfxbook Credentials
MYFXBOOK_EMAIL=your_email@example.com
MYFXBOOK_PASSWORD=your_password

# Trading Parameters
SYMBOLS=GBPUSD,USDJPY,GBPJPY,EURUSD
RISK_PERCENT=1.0
MAX_SPREAD_PIPS=3.0
MIN_SENTIMENT_THRESHOLD=60.0
SCAN_INTERVAL=60
```

### 6.2 Faili ya JSON

Bot inaweza pia kutumia faili ya JSON kwa usanidi wa kina zaidi:

```json
{
  "mt5": {
    "login": 123456789,
    "password": "your_password",
    "server": "your_broker_server"
  },
  "myfxbook": {
    "email": "your_email@example.com",
    "password": "your_password"
  },
  "trading": {
    "symbols": ["GBPUSD", "USDJPY", "GBPJPY", "EURUSD"],
    "timeframe": 16,
    "htf_timeframe": 15,
    "risk_percent": 1.0,
    "max_spread_pips": 3.0,
    "min_sentiment_threshold": 60.0,
    "scan_interval": 60
  }
}
```

## 7. Mifumo ya Logging na Ufuatiliaji

### 7.1 Logging

Bot inatumia mfumo wa logging wa Python kwa ajili ya kumbukumbu:

```python
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("trading_bot.log"),
        logging.StreamHandler()
    ]
)
```

### 7.2 Ufuatiliaji wa Utendaji

Bot inahifadhi takwimu za utendaji kwenye faili ya JSON:

```json
{
  "trades": [
    {
      "symbol": "GBPUSD",
      "direction": "buy",
      "setup": "detect_turtle_soup",
      "entry_time": "2025-06-05T10:30:00",
      "entry_price": 1.2345,
      "order_block": {
        "low": 1.2340,
        "high": 1.2350,
        "time": "2025-06-05T10:15:00"
      }
    }
  ],
  "stats": {
    "total_trades": 1,
    "winning_trades": 1,
    "losing_trades": 0,
    "win_rate": 100.0,
    "profit_factor": 2.5,
    "total_profit": 50.0,
    "max_drawdown": 0.0
  }
}
```

## 8. Maktaba na Vitegemezi

Bot inategemea maktaba zifuatazo:

1. **MetaTrader5**: Kwa ajili ya muunganisho na MT5 na utekelezaji wa amri
2. **pandas**: Kwa ajili ya uchambuzi wa data
3. **requests**: Kwa ajili ya mawasiliano na API ya Myfxbook
4. **python-dotenv**: Kwa ajili ya kupakia usanidi kutoka kwa faili ya `.env`
5. **numpy**: Kwa ajili ya uchambuzi wa data
6. **matplotlib**: Kwa ajili ya kuchora grafu za utendaji

## 9. Uboreshaji wa Baadaye

### 9.1 Mikakati Zaidi ya Biashara

- Kuongeza mikakati zaidi ya ICT
- Kuongeza mikakati ya machine learning
- Kuongeza mikakati za uchambuzi wa msingi

### 9.2 Dashboard ya Utendaji

- Kutengeneza dashboard ya kuonyesha utendaji wa bot
- Kuonyesha grafu za utendaji
- Kuonyesha takwimu za biashara

### 9.3 Backtesting

- Kuongeza uwezo wa kupima mikakati dhidi ya data ya kihistoria
- Kuonyesha takwimu za backtesting
- Kuruhusu optimization ya parameters

### 9.4 Arifa

- Kuongeza uwezo wa kutuma arifa kupitia Telegram
- Kuongeza uwezo wa kutuma arifa kupitia barua pepe
- Kuongeza uwezo wa kutuma arifa kupitia SMS

## 10. Hitimisho

Usanifu wa bot umeundwa kuwa modular, rahisi kupanua, na rahisi kutumia. Bot inatekeleza mikakati kadhaa ya biashara ya ICT na inaweza kuboreshwa zaidi kulingana na mahitaji ya mtumiaji.

