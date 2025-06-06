# Mchoro wa Mtiririko wa Data wa Trading Bot

## 1. Mtiririko wa Jumla

```
+-------------+     +-------------+     +-------------+
|             |     |             |     |             |
|  Config     |---->|  TradingBot |---->| Performance |
|  Files      |     |             |     | Tracker     |
|             |     |             |     |             |
+-------------+     +------+------+     +-------------+
                           |
                           |
                           v
          +----------------+----------------+
          |                                 |
          |                                 |
          v                                 v
+-------------+                      +-------------+
|             |                      |             |
| MetaTrader5 |<-------------------->| Myfxbook    |
|             |                      |             |
+-------------+                      +-------------+
```

## 2. Mtiririko wa Usanidi

```
+-------------+     +-------------+     +-------------+
|             |     |             |     |             |
|  .env File  |---->|  Config     |---->| TradingBot  |
|             |     |  Class      |     |             |
+-------------+     +-------------+     +-------------+
                           ^
                           |
+-------------+            |
|             |            |
|  JSON File  |------------+
|             |
+-------------+
```

## 3. Mtiririko wa Data ya Soko

```
+-------------+     +-------------+     +-------------+
|             |     |             |     |             |
| MetaTrader5 |---->| MT5Handler  |---->| TradingBot  |
|             |     |             |     |             |
+-------------+     +-------------+     +-------------+
                                              |
                                              |
                                              v
+-------------+     +-------------+     +-------------+
|             |     |             |     |             |
|  Myfxbook   |---->| MyfxbookAPI |---->| TradingBot  |
|             |     |             |     |             |
+-------------+     +-------------+     +-------------+
```

## 4. Mtiririko wa Maamuzi ya Biashara

```
+-------------+     +-------------+     +-------------+
|             |     |             |     |             |
| Price Data  |---->| Trading     |---->| Signal      |
|             |     | Strategies  |     | Detection   |
+-------------+     +-------------+     +-------------+
                                              |
                                              |
                                              v
+-------------+     +-------------+     +-------------+
|             |     |             |     |             |
| Sentiment   |---->| Validation  |---->| Order       |
| Data        |     | Logic       |     | Execution   |
+-------------+     +-------------+     +-------------+
```

## 5. Mtiririko wa Usimamizi wa Hatari

```
+-------------+     +-------------+     +-------------+
|             |     |             |     |             |
| Account     |---->| Risk        |---->| Position    |
| Balance     |     | Percentage  |     | Size        |
+-------------+     +-------------+     +-------------+
                                              |
                                              |
                                              v
+-------------+     +-------------+     +-------------+
|             |     |             |     |             |
| Stop Loss   |---->| Pip Value   |---->| Order       |
| Distance    |     | Calculation |     | Parameters  |
+-------------+     +-------------+     +-------------+
```

## 6. Mtiririko wa Ufuatiliaji wa Utendaji

```
+-------------+     +-------------+     +-------------+
|             |     |             |     |             |
| Trade       |---->| Performance |---->| Statistics  |
| Results     |     | Tracker     |     | Calculation |
+-------------+     +-------------+     +-------------+
                                              |
                                              |
                                              v
                                        +-------------+
                                        |             |
                                        | JSON File   |
                                        | Storage     |
                                        |             |
                                        +-------------+
```

## 7. Mtiririko wa Logging

```
+-------------+     +-------------+     +-------------+
|             |     |             |     |             |
| Bot         |---->| Logging     |---->| Log File    |
| Activities  |     | System      |     |             |
+-------------+     +-------------+     +-------------+
                           |
                           |
                           v
                    +-------------+
                    |             |
                    | Console     |
                    | Output      |
                    |             |
                    +-------------+
```

## 8. Mtiririko wa Amri za Biashara

```
+-------------+     +-------------+     +-------------+
|             |     |             |     |             |
| Trading     |---->| MT5Handler  |---->| MetaTrader5 |
| Signal      |     |             |     |             |
+-------------+     +-------------+     +-------------+
      ^                    ^                   |
      |                    |                   |
      |                    |                   v
+-------------+     +-------------+     +-------------+
|             |     |             |     |             |
| Risk        |---->| Order       |---->| Broker      |
| Management  |     | Parameters  |     |             |
+-------------+     +-------------+     +-------------+
```

## 9. Mtiririko wa Mzunguko Kamili

```
+-------------+     +-------------+     +-------------+
|             |     |             |     |             |
| Config      |---->| TradingBot  |---->| MT5Handler  |
| Files       |     | Initialize  |     | Connect     |
+-------------+     +-------------+     +-------------+
                                              |
                                              |
                                              v
+-------------+     +-------------+     +-------------+
|             |     |             |     |             |
| MyfxbookAPI |<----| TradingBot  |<----| MT5Handler  |
| Login       |     | Run Loop    |     | Get Data    |
+-------------+     +-------------+     +-------------+
      |                    |                   ^
      |                    |                   |
      v                    v                   |
+-------------+     +-------------+     +-------------+
|             |     |             |     |             |
| Get         |---->| Trading     |---->| Signal      |
| Sentiment   |     | Strategies  |     | Validation  |
+-------------+     +-------------+     +-------------+
                                              |
                                              |
                                              v
+-------------+     +-------------+     +-------------+
|             |     |             |     |             |
| Risk        |---->| Order       |---->| Performance |
| Management  |     | Execution   |     | Tracking    |
+-------------+     +-------------+     +-------------+
```

## Maelezo ya Mtiririko wa Data

### 1. Mtiririko wa Usanidi
- Faili za usanidi (`.env` au JSON) zinasomwa na darasa la `Config`
- Usanidi unapitishwa kwa vipengele vingine vya bot

### 2. Mtiririko wa Data ya Soko
- `MT5Handler` inapata data ya bei kutoka kwa MetaTrader5
- `MyfxbookAPI` inapata data ya hisia za soko kutoka kwa Myfxbook
- Data zote zinapitishwa kwa `TradingBot` kwa uchambuzi

### 3. Mtiririko wa Maamuzi ya Biashara
- Data ya bei inapitishwa kwa `TradingStrategies` kwa uchambuzi
- Mikakati inatambua ishara za biashara
- Ishara zinathibitishwa kwa kutumia data ya hisia za soko
- Amri zinatekelezwa kupitia `MT5Handler`

### 4. Mtiririko wa Usimamizi wa Hatari
- Saizi ya nafasi inakokotolewa kulingana na salio la akaunti na asilimia ya hatari
- Umbali wa stop-loss unakokotolewa kulingana na order block
- Thamani ya pip inakokotolewa kulingana na jozi ya sarafu
- Parameters za amri zinatengenezwa na kupitishwa kwa `MT5Handler`

### 5. Mtiririko wa Ufuatiliaji wa Utendaji
- Matokeo ya biashara yanapitishwa kwa `PerformanceTracker`
- Takwimu zinakokotolewa na kuhifadhiwa kwenye faili ya JSON

### 6. Mtiririko wa Logging
- Shughuli za bot zinapitishwa kwa mfumo wa logging
- Kumbukumbu zinahifadhiwa kwenye faili na kuonyeshwa kwenye console

