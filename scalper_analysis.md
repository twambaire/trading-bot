# Uchambuzi wa Scalper Bot

## Muhtasari
Faili ya `scalper.py` ni bot ya biashara ya forex inayotumia MetaTrader5 (MT5) na Myfxbook. Bot hii inatekeleza mikakati kadhaa ya scalping kulingana na Institutional Candle Theory (ICT) na inafanya maamuzi ya biashara kwa kuchanganya uchambuzi wa hisia za soko na ishara za kiufundi.

## Vipengele Vikuu

### 1. Muunganisho na Huduma za Nje
- **Myfxbook**: Inatumika kupata data ya hisia za soko (sentiment data)
- **MetaTrader5**: Platform ya biashara inayotumika kutekeleza amri

### 2. Mikakati ya Biashara
Bot inatekeleza mikakati kadhaa ya ICT:
- **Turtle Soup**: Inalenga kufanya biashara kinyume na uvunjaji wa bei
- **Stop Hunt**: Inalenga kunasa mitego ya bei iliyowekwa na taasisi
- **Retail Trap**: Inalenga kunasa wafanyabiashara wadogo wanaoingia kwa wakati mbaya
- **SH/BMS/RTO & SMS/BMS/RTO**: Mikakati ya ICT inayolenga swing highs/lows

### 3. Uchambuzi wa Kiufundi
- **Higher Timeframe (HTF) Bias**: Inatambua mwelekeo wa muda mrefu
- **Order Blocks**: Inatambua maeneo muhimu ya kununua/kuuza
- **Fair Value Gaps (FVG)**: Inatambua mianya ya bei ambayo inaweza kujazwa

### 4. Usimamizi wa Hatari
- Inaweka stop-loss karibu na maeneo ya Order Block
- Inaweka take-profit kulingana na viwango vya juu/chini vya hivi karibuni

### 5. Maamuzi ya Biashara
Bot inafanya maamuzi ya biashara kwa:
1. Kupata hisia za soko kutoka Myfxbook
2. Kutafuta ishara za kiufundi kutoka kwa mikakati iliyoprogramiwa
3. Kuthibitisha mwelekeo na Order Blocks
4. Kuweka amri za biashara zenye stop-loss na take-profit

## Changamoto na Mapendekezo

### Changamoto
1. **Usalama**: Faili ina vitambulisho vya kuingia (login credentials) ambavyo vinapaswa kuondolewa
2. **Usimamizi wa Hatari**: Inaweka saizi ya lot ya kudumu (0.01) bila kuzingatia ukubwa wa akaunti
3. **Uthibitishaji wa Ishara**: Inategemea ishara moja tu kwa kila mkakati
4. **Utumiaji wa Rasilimali**: Inachunguza jozi 3 tu za sarafu

### Mapendekezo ya Uboreshaji
1. **Ondoa Vitambulisho vya Kuingia**: Tumia faili ya config au variables za mazingira
2. **Boresha Usimamizi wa Hatari**: Ongeza usimamizi wa mtaji unaozingatia ukubwa wa akaunti
3. **Ongeza Uthibitishaji wa Ishara**: Hitaji uthibitishaji zaidi kabla ya kuweka amri
4. **Ongeza Jozi za Sarafu**: Ruhusu orodha inayoweza kubadilishwa ya jozi za sarafu
5. **Ongeza Ufuatiliaji**: Ongeza uwezo wa kuripoti utendaji na takwimu
6. **Ongeza Backtesting**: Ongeza uwezo wa kupima mikakati dhidi ya data ya kihistoria

## Teknolojia Zilizotumika
- **Python**: Lugha ya programu
- **MetaTrader5**: API ya biashara
- **Pandas**: Uchambuzi wa data
- **Requests**: Mawasiliano ya API ya Myfxbook

## Hitimisho
Bot hii ni mfano mzuri wa trading bot ya forex inayotumia mikakati ya ICT. Ina muundo mzuri na inatekeleza mikakati kadhaa ya biashara, lakini inaweza kuboreshwa zaidi kwa kuongeza usimamizi bora wa hatari na kuondoa vitambulisho vya kuingia vilivyowekwa moja kwa moja kwenye code.

