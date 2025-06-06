# ICT Forex Trading Bot

Bot ya biashara ya forex iliyoboreshwa inayotumia mikakati ya Institutional Candle Theory (ICT) na uchambuzi wa hisia za soko.

## Vipengele

- **Usalama wa Juu**: Hakuna vitambulisho vilivyowekwa moja kwa moja kwenye code
- **Usimamizi wa Hatari**: Ukokotoaji wa saizi ya nafasi kulingana na asilimia ya hatari
- **Usanidi wa Nje**: Faili ya `.env` kwa ajili ya usanidi rahisi
- **Ufuatiliaji wa Utendaji**: Kufuatilia na kuhifadhi takwimu za biashara
- **Uboreshaji wa Mikakati**: Mikakati kadhaa ya ICT iliyotekelezwa
- **Logging**: Kumbukumbu kamili za shughuli za bot

## Mikakati ya Biashara Iliyotekelezwa

1. **Turtle Soup**: Inalenga kufanya biashara kinyume na uvunjaji wa bei
2. **Stop Hunt**: Inalenga kunasa mitego ya bei iliyowekwa na taasisi
3. **Retail Trap**: Inalenga kunasa wafanyabiashara wadogo wanaoingia kwa wakati mbaya
4. **SH/BMS/RTO & SMS/BMS/RTO**: Mikakati ya ICT inayolenga swing highs/lows

## Mahitaji

```
MetaTrader5==5.0.45
pandas==2.0.3
requests==2.31.0
python-dotenv==1.0.0
numpy==1.24.3
matplotlib==3.7.2
```

## Usakinishaji

1. Sakinisha mahitaji:

```bash
pip install -r requirements.txt
```

2. Rekebisha faili ya `.env` na vitambulisho vyako:

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

## Matumizi

Endesha bot:

```bash
python improved_scalper.py
```

## Muundo wa Bot

Bot ina vipengele vikuu vifuatavyo:

### 1. Config
Husimamia usanidi wa bot kutoka kwa faili ya `.env` au faili ya JSON.

### 2. MyfxbookAPI
Huwasiliana na API ya Myfxbook kupata data ya hisia za soko.

### 3. MT5Handler
Husimamia muunganisho na MetaTrader5, kupata data ya bei, na kuweka amri.

### 4. TradingStrategies
Hutekeleza mikakati mbalimbali ya biashara ya ICT.

### 5. PerformanceTracker
Hufuatilia na kuhifadhi takwimu za utendaji wa bot.

### 6. TradingBot
Husimamia mzunguko mkuu wa bot na kuunganisha vipengele vyote.

## Usimamizi wa Hatari

Bot inakokotoa saizi ya nafasi kulingana na:
- Asilimia ya hatari iliyowekwa
- Sarafu ya akaunti
- Umbali wa stop-loss
- Thamani ya pip kwa jozi ya sarafu

## Kumbukumbu na Ufuatiliaji

Bot inahifadhi kumbukumbu za shughuli zake katika faili ya `trading_bot.log` na takwimu za utendaji katika `performance.json`.

## Uboreshaji wa Baadaye

- Kuongeza mikakati zaidi ya biashara
- Kuongeza dashboard ya kuonyesha utendaji
- Kuongeza uwezo wa backtesting
- Kuongeza uwezo wa kutuma arifa kupitia Telegram au barua pepe

## Tahadhari

Bot hii ni kwa madhumuni ya elimu tu. Biashara ya forex ina hatari kubwa ya kupoteza mtaji. Hakikisha unaelewa kikamilifu jinsi bot inafanya kazi kabla ya kuitumia na pesa halisi.

