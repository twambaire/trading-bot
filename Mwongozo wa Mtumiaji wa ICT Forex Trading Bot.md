# Mwongozo wa Mtumiaji wa ICT Forex Trading Bot

**Mwandishi**: Manus AI  
**Toleo**: 1.0  
**Tarehe**: Juni 5, 2025

## Yaliyomo

1. [Utangulizi](#utangulizi)
2. [Mahitaji ya Mfumo](#mahitaji-ya-mfumo)
3. [Usakinishaji](#usakinishaji)
4. [Usanidi](#usanidi)
5. [Matumizi](#matumizi)
6. [Mikakati ya Biashara](#mikakati-ya-biashara)
7. [Usimamizi wa Hatari](#usimamizi-wa-hatari)
8. [Ufuatiliaji wa Utendaji](#ufuatiliaji-wa-utendaji)
9. [Utatuzi wa Matatizo](#utatuzi-wa-matatizo)
10. [Maswali Yanayoulizwa Mara kwa Mara (FAQ)](#maswali-yanayoulizwa-mara-kwa-mara-faq)
11. [Marejeleo](#marejeleo)

## Utangulizi

ICT Forex Trading Bot ni programu ya kuautomate biashara ya forex inayotumia mikakati ya Institutional Candle Theory (ICT) pamoja na uchambuzi wa hisia za soko. Bot hii imeundwa kufanya biashara kiotomatiki kwa kutumia ishara za kiufundi na data ya hisia za soko kutoka kwa Myfxbook.

Bot hii ina vipengele vikuu vifuatavyo:

- **Usanidi Rahisi**: Inaweza kusanidiwa kupitia faili ya `.env` au JSON
- **Usimamizi wa Hatari**: Inakokotoa saizi ya nafasi kulingana na asilimia ya hatari
- **Mikakati Mingi**: Inatekeleza mikakati kadhaa ya ICT
- **Ufuatiliaji wa Utendaji**: Inafuatilia na kuhifadhi takwimu za biashara
- **Usalama wa Juu**: Hakuna vitambulisho vilivyowekwa moja kwa moja kwenye code

Bot hii inafanya kazi kwa:

1. Kuunganisha na MetaTrader5 na Myfxbook
2. Kupata data ya bei na hisia za soko
3. Kutambua ishara za biashara kwa kutumia mikakati ya ICT
4. Kuthibitisha ishara kwa kutumia data ya hisia za soko
5. Kuweka amri za biashara kupitia MetaTrader5
6. Kufuatilia utendaji na kuhifadhi takwimu

## Mahitaji ya Mfumo

### Mahitaji ya Programu

- Python 3.7 au zaidi
- MetaTrader5 (MT5)
- Akaunti ya Myfxbook (kwa uchambuzi wa hisia za soko)

### Mahitaji ya Maktaba

Maktaba zifuatazo za Python zinahitajika:

- MetaTrader5==5.0.45
- pandas==2.0.3
- requests==2.31.0
- python-dotenv==1.0.0
- numpy==1.24.3
- matplotlib==3.7.2

### Mahitaji ya Akaunti

- Akaunti ya MetaTrader5 (demo au halisi)
- Akaunti ya Myfxbook (kwa uchambuzi wa hisia za soko)

## Usakinishaji

### Hatua za Usakinishaji

1. **Pakua Faili za Mradi**

   Pakua faili zote za mradi kutoka kwa chanzo ulichopewa.

2. **Sakinisha MetaTrader5**

   Sakinisha MetaTrader5 kutoka kwa tovuti rasmi ya MetaTrader:
   [https://www.metatrader5.com/en/download](https://www.metatrader5.com/en/download)

3. **Tengeneza Akaunti ya MT5**

   Tengeneza akaunti ya demo au halisi kupitia broker wako unayependelea.

4. **Sakinisha Mahitaji ya Python**

   Tumia amri ifuatayo kusakinisha mahitaji yote ya Python:

   ```bash
   pip install -r requirements.txt
   ```

5. **Tengeneza Akaunti ya Myfxbook**

   Tengeneza akaunti ya Myfxbook kwa kutembelea:
   [https://www.myfxbook.com/](https://www.myfxbook.com/)

6. **Endesha Script ya Usanidi**

   Endesha script ya usanidi ili kusanidi bot:

   ```bash
   python setup.py
   ```

   Script hii itakuuliza maelezo muhimu kama vile vitambulisho vya MT5 na Myfxbook.

## Usanidi

### Faili ya .env

Bot inatumia faili ya `.env` kwa usanidi wa msingi. Faili hii inapaswa kuwa na vigezo vifuatavyo:

```
# MT5 Credentials
MT5_LOGIN=123456789
MT5_PASSWORD=your_password
MT5_SERVER=your_broker_server

# Myfxbook Credentials
MYFXBOOK_EMAIL=your_email@example.com
MYFXBOOK_PASSWORD=your_password

# Trading Parameters
SYMBOLS=EURUSD,GBPUSD,USDJPY,GBPJPY
RISK_PERCENT=1.0
MAX_SPREAD_PIPS=3.0
MIN_SENTIMENT_THRESHOLD=60.0
SCAN_INTERVAL=60
```

### Vigezo vya Usanidi

| Kigezo | Maelezo | Thamani ya Default |
|--------|---------|-------------------|
| MT5_LOGIN | Namba ya akaunti ya MT5 | - |
| MT5_PASSWORD | Nenosiri la akaunti ya MT5 | - |
| MT5_SERVER | Jina la seva ya broker ya MT5 | FBS-Demo |
| MYFXBOOK_EMAIL | Barua pepe ya akaunti ya Myfxbook | - |
| MYFXBOOK_PASSWORD | Nenosiri la akaunti ya Myfxbook | - |
| SYMBOLS | Jozi za sarafu zinazofanyiwa biashara | EURUSD,GBPUSD,USDJPY,GBPJPY |
| RISK_PERCENT | Asilimia ya mtaji inayoweza kupotea kwa biashara moja | 1.0 |
| MAX_SPREAD_PIPS | Kiwango cha juu cha spread kinachokubalika kwa pips | 3.0 |
| MIN_SENTIMENT_THRESHOLD | Kiwango cha chini cha hisia kwa ishara | 60.0 |
| SCAN_INTERVAL | Muda wa kuangalia (sekunde) | 60 |

### Usanidi wa Kina Zaidi

Kwa usanidi wa kina zaidi, unaweza kutumia faili ya JSON. Tengeneza faili ya `config.json` na muundo ufuatao:

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
    "symbols": ["EURUSD", "GBPUSD", "USDJPY", "GBPJPY"],
    "timeframe": 16,
    "htf_timeframe": 15,
    "risk_percent": 1.0,
    "max_spread_pips": 3.0,
    "min_sentiment_threshold": 60.0,
    "scan_interval": 60
  }
}
```

Kisha unaweza kuendesha bot kwa kutumia faili ya usanidi:

```bash
python improved_scalper.py --config config.json
```

## Matumizi

### Kuanza Bot

Kuanza bot, endesha amri ifuatayo:

```bash
python improved_scalper.py
```

Bot itaanza kufanya kazi na kuonyesha ujumbe wa kuanza:

```
2025-06-05 10:00:00 - INFO - Initializing trading bot...
2025-06-05 10:00:01 - INFO - Connected to MT5
2025-06-05 10:00:02 - INFO - Successfully logged in to Myfxbook
2025-06-05 10:00:02 - INFO - Trading bot initialized successfully
2025-06-05 10:00:02 - INFO - Starting trading bot main loop
2025-06-05 10:00:02 - INFO - Trading configuration: 4 symbols, 1.0% risk, 60s interval
```

### Kusimamisha Bot

Kusimamisha bot, bonyeza `Ctrl+C` kwenye terminal. Bot itaonyesha ujumbe wa kusimamisha:

```
2025-06-05 10:30:00 - INFO - Trading bot stopped by user
2025-06-05 10:30:00 - INFO - Shutting down trading bot...
2025-06-05 10:30:00 - INFO - Disconnected from MT5
2025-06-05 10:30:00 - INFO - Trading bot shutdown complete
```

### Kufuatilia Bot

Bot inahifadhi kumbukumbu za shughuli zake kwenye faili ya `trading_bot.log`. Unaweza kufuatilia shughuli za bot kwa kutumia amri ifuatayo:

```bash
tail -f trading_bot.log
```

### Kuangalia Utendaji

Bot inahifadhi takwimu za utendaji kwenye faili ya `performance.json`. Unaweza kuangalia takwimu za utendaji kwa kutumia amri ifuatayo:

```bash
cat performance.json
```

## Mikakati ya Biashara

Bot inatekeleza mikakati kadhaa ya ICT:

### 1. Turtle Soup

Mkakati huu unalenga kufanya biashara kinyume na uvunjaji wa bei. Inafanya biashara wakati bei inavunja kiwango cha juu au chini cha siku 20 na kisha inarudi.

**Ishara ya Kununua:**
- Bei inavunja kiwango cha chini cha siku 20
- Bei inarudi juu ya kiwango cha chini

**Ishara ya Kuuza:**
- Bei inavunja kiwango cha juu cha siku 20
- Bei inarudi chini ya kiwango cha juu

### 2. Stop Hunt

Mkakati huu unalenga kunasa mitego ya bei iliyowekwa na taasisi. Inafanya biashara wakati bei inavunja kiwango cha juu au chini cha hivi karibuni na kisha inarudi.

**Ishara ya Kununua:**
- Bei inavunja kiwango cha chini cha hivi karibuni
- Bei inarudi juu ya kiwango cha juu cha mshumaa uliopita

**Ishara ya Kuuza:**
- Bei inavunja kiwango cha juu cha hivi karibuni
- Bei inarudi chini ya kiwango cha chini cha mshumaa uliopita

### 3. Retail Trap

Mkakati huu unalenga kunasa wafanyabiashara wadogo wanaoingia kwa wakati mbaya. Inafanya biashara wakati bei inavunja kiwango cha juu au chini na kisha inarudi kwa nguvu.

**Ishara ya Kununua:**
- Bei inavunja kiwango cha chini
- Bei inarudi juu ya kiwango cha juu cha mshumaa uliopita

**Ishara ya Kuuza:**
- Bei inavunja kiwango cha juu
- Bei inarudi chini ya kiwango cha chini cha mshumaa uliopita

### 4. SH/BMS/RTO & SMS/BMS/RTO

Mikakati hii inalenga swing highs/lows na inafanya biashara wakati bei inavunja muundo wa soko na kisha inarudi kwenye asili.

**Ishara ya Kununua:**
- Bei inavunja kiwango cha chini cha siku 10
- Bei inarudi juu ya kiwango cha juu cha mshumaa uliopita

**Ishara ya Kuuza:**
- Bei inavunja kiwango cha juu cha siku 10
- Bei inarudi chini ya kiwango cha chini cha mshumaa uliopita

## Usimamizi wa Hatari

Bot ina mfumo wa usimamizi wa hatari uliojumuishwa:

### Kukokotoa Saizi ya Nafasi

Bot inakokotoa saizi ya nafasi kulingana na:

1. **Asilimia ya Hatari**: Asilimia ya mtaji inayoweza kupotea kwa biashara moja
2. **Umbali wa Stop-Loss**: Umbali kutoka kwa bei ya kuingia hadi kwa stop-loss
3. **Thamani ya Pip**: Thamani ya pip kwa jozi ya sarafu

Formula inayotumika ni:

```
position_size = (balance * risk_percent) / (stop_loss_pips * pip_value)
```

### Usimamizi wa Spread

Bot inachunguza spread kabla ya kuweka amri:

1. **Kiwango cha Juu cha Spread**: Kiwango cha juu cha spread kinachokubalika
2. **Kuepuka Spread Kubwa**: Bot haitaweka amri ikiwa spread ni kubwa zaidi ya kiwango cha juu

### Stop-Loss na Take-Profit

Bot inaweka stop-loss na take-profit kwa kila amri:

1. **Stop-Loss**: Inawekwa karibu na maeneo ya Order Block
2. **Take-Profit**: Inawekwa kulingana na viwango vya juu/chini vya hivi karibuni

## Ufuatiliaji wa Utendaji

Bot inafuatilia utendaji wake na kuhifadhi takwimu kwenye faili ya `performance.json`:

### Takwimu Zinazofuatiliwa

| Takwimu | Maelezo |
|---------|---------|
| total_trades | Jumla ya biashara zilizofanywa |
| winning_trades | Idadi ya biashara zilizopata faida |
| losing_trades | Idadi ya biashara zilizopata hasara |
| win_rate | Asilimia ya biashara zilizopata faida |
| profit_factor | Uwiano wa faida kwa hasara |
| total_profit | Jumla ya faida au hasara |
| max_drawdown | Upungufu mkubwa wa mtaji |

### Kumbukumbu za Biashara

Bot inahifadhi kumbukumbu za kila biashara:

```json
{
  "symbol": "EURUSD",
  "direction": "buy",
  "setup": "turtle_soup",
  "entry_time": "2025-06-05T10:00:00",
  "entry_price": 1.1000,
  "order_block": {
    "low": 1.0990,
    "high": 1.1010,
    "time": "2025-06-05T09:45:00"
  }
}
```

## Utatuzi wa Matatizo

### Matatizo ya Kawaida na Suluhisho

| Tatizo | Suluhisho |
|--------|-----------|
| Bot haiwezi kuunganisha na MT5 | - Hakikisha MT5 imefunguliwa<br>- Hakikisha vitambulisho vya MT5 ni sahihi<br>- Hakikisha seva ya broker ni sahihi |
| Bot haiwezi kuingia kwenye Myfxbook | - Hakikisha vitambulisho vya Myfxbook ni sahihi<br>- Hakikisha una muunganisho wa intaneti<br>- Jaribu kuingia kwenye tovuti ya Myfxbook mwenyewe |
| Bot haiweki amri | - Angalia kumbukumbu za bot<br>- Hakikisha spread si kubwa zaidi ya kiwango cha juu<br>- Hakikisha kuna ishara za biashara zinazothibitishwa |
| Bot inafanya biashara mbaya | - Rekebisha vigezo vya mikakati<br>- Ongeza kiwango cha hisia kinachohitajika<br>- Punguza asilimia ya hatari |

### Kumbukumbu za Bot

Kwa utatuzi wa kina zaidi, angalia faili ya `trading_bot.log`. Faili hii ina kumbukumbu za kina za shughuli zote za bot.

## Maswali Yanayoulizwa Mara kwa Mara (FAQ)

### 1. Je, bot inafanya kazi na broker wowote?

Ndiyo, bot inafanya kazi na broker yeyote anayetumia MetaTrader5. Hakikisha broker wako anaruhusu biashara ya kiotomatiki.

### 2. Je, bot inafanya kazi na jozi zote za sarafu?

Ndiyo, bot inaweza kufanya kazi na jozi zote za sarafu zinazopatikana kwenye MetaTrader5. Hata hivyo, inashauriwa kutumia jozi za sarafu zenye ukwasi mkubwa kama vile EURUSD, GBPUSD, USDJPY, na GBPJPY.

### 3. Je, ninaweza kutumia bot bila akaunti ya Myfxbook?

Ndiyo, bot inaweza kufanya kazi bila akaunti ya Myfxbook, lakini haitaweza kutumia data ya hisia za soko. Hii inaweza kupunguza ufanisi wa bot.

### 4. Je, bot inafanya kazi na akaunti ya demo?

Ndiyo, bot inafanya kazi na akaunti za demo na halisi. Inashauriwa kuanza na akaunti ya demo kabla ya kutumia akaunti halisi.

### 5. Je, ninaweza kubadilisha mikakati ya biashara?

Ndiyo, unaweza kubadilisha mikakati ya biashara kwa kuhariri faili ya `improved_scalper.py`. Angalia sehemu ya `TradingStrategies` kwa mikakati iliyotekelezwa.

### 6. Je, bot inafanya kazi wakati kompyuta yangu imezimwa?

Hapana, bot inahitaji kompyuta kuwa imewashwa na kuunganishwa na intaneti. Unaweza kutumia seva ya wingu au VPS kufanya bot ifanye kazi 24/7.

### 7. Je, ni hatari gani za kutumia bot?

Biashara ya forex ina hatari kubwa ya kupoteza mtaji. Bot inaweza kupunguza hatari kwa kutumia usimamizi wa hatari, lakini haiwezi kuondoa hatari kabisa. Hakikisha unaelewa hatari kabla ya kutumia bot na pesa halisi.

### 8. Je, ninaweza kutumia bot kwa biashara ya hisa au cryptocurrency?

Bot imeundwa kwa ajili ya biashara ya forex, lakini inaweza kuboreshwa kwa ajili ya biashara ya hisa au cryptocurrency. Hii itahitaji mabadiliko kwenye code.

## Marejeleo

1. [MetaTrader5 Documentation](https://www.mql5.com/en/docs/integration/python_metatrader5)
2. [Myfxbook API Documentation](https://www.myfxbook.com/api)
3. [Institutional Candle Theory (ICT)](https://www.youtube.com/c/InnerCircleTrader)
4. [Python Documentation](https://docs.python.org/3/)
5. [Pandas Documentation](https://pandas.pydata.org/docs/)
6. [Requests Documentation](https://docs.python-requests.org/en/latest/)
7. [Python-dotenv Documentation](https://github.com/theskumar/python-dotenv)

---

© 2025 Manus AI. Haki zote zimehifadhiwa.

