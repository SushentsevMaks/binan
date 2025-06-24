import time

import ccxt
import pandas as pd
import pymysql
import telebot
import keys
from binan.banan.sql_request import equal, sql_del

telega_token = "5926919919:AAFCHFocMt_pdnlAgDo-13wLe4h_tHO0-GE"

one = ['NEOUSDT', 'LTCUSDT', 'QTUMUSDT', 'ADAUSDT', 'XRPUSDT', 'EOSUSDT', 'IOTAUSDT', 'XLMUSDT', 'ONTUSDT', 'TRXUSDT', 'ETCUSDT', 'ICXUSDT']

onedop = ['NULSUSDT', 'VETUSDT', 'LINKUSDT', 'ONGUSDT', 'HOTUSDT', 'ZILUSDT', 'ZRXUSDT', 'FETUSDT', 'BATUSDT', 'ZECUSDT', 'IOSTUSDT', 'CELRUSDT']

two = ['DASHUSDT', 'THETAUSDT', 'ENJUSDT', 'ATOMUSDT', 'TFUELUSDT', 'ONEUSDT', 'FTMUSDT', 'ALGOUSDT', 'DOGEUSDT', 'DUSKUSDT', 'ANKRUSDT']

twodop = ['WINUSDT', 'COSUSDT', 'MTLUSDT', 'DENTUSDT', 'KEYUSDT', 'WANUSDT', 'FUNUSDT', 'CVCUSDT', 'CHZUSDT', 'BANDUSDT', 'XTZUSDT', 'RENUSDT']

three = ['RVNUSDT', 'HBARUSDT', 'NKNUSDT', 'STXUSDT', 'KAVAUSDT', 'ARPAUSDT', 'IOTXUSDT', 'RLCUSDT', 'CTXCUSDT', 'BCHUSDT', 'TROYUSDT', 'VITEUSDT']

threedop = ['FTTUSDT', 'OGNUSDT', 'WRXUSDT', 'LSKUSDT', 'BNTUSDT', 'LTOUSDT', 'MBLUSDT', 'COTIUSDT', 'STPTUSDT', 'DATAUSDT', 'SOLUSDT', 'CTSIUSDT']

four = ['HIVEUSDT', 'CHRUSDT', 'ARDRUSDT', 'MDTUSDT', 'STMXUSDT', 'KNCUSDT', 'LRCUSDT', 'COMPUSDT', 'SCUSDT', 'ZENUSDT', 'SNXUSDT', 'VTHOUSDT']

fourdop = ['DGBUSDT', 'SXPUSDT', 'MKRUSDT', 'DCRUSDT', 'STORJUSDT', 'MANAUSDT', 'YFIUSDT', 'BALUSDT', 'BLZUSDT', 'IRISUSDT', 'KMDUSDT', 'JSTUSDT']

five = ['CATIUSDT', 'CRVUSDT', 'SANDUSDT', 'NMRUSDT', 'DOTUSDT', 'LUNAUSDT', 'RSRUSDT', 'TRBUSDT', 'SUSHIUSDT', 'KSMUSDT', 'EGLDUSDT', 'DIAUSDT', 'RUNEUSDT']

fivedop = ['FIOUSDT', 'UMAUSDT', 'BELUSDT', 'WINGUSDT', 'UNIUSDT', 'OXTUSDT', 'SUNUSDT', 'AVAXUSDT', 'FLMUSDT', 'ORNUSDT', 'UTKUSDT', 'XVSUSDT']

six = ['ALPHAUSDT', 'AAVEUSDT', 'NEARUSDT', 'FILUSDT', 'INJUSDT', 'AUDIOUSDT', 'CTKUSDT', 'AKROUSDT', 'AXSUSDT', 'HARDUSDT', 'STRAXUSDT', 'UNFIUSDT']

sixdop = ['EIGENUSDT', 'ROSEUSDT', 'AVAUSDT', 'SKLUSDT', 'GRTUSDT', 'JUVUSDT', 'PSGUSDT', '1INCHUSDT', 'OGUSDT', 'ATMUSDT', 'ASRUSDT', 'CELOUSDT']

seven = ['RIFUSDT', 'TRUUSDT', 'CKBUSDT', 'TWTUSDT', 'FIROUSDT', 'LITUSDT', 'SFPUSDT', 'DODOUSDT', 'CAKEUSDT', 'ACMUSDT', 'BADGERUSDT', 'FISUSDT']

sevendop = ['TURBOUSDT', 'SCRUSDT', 'OMUSDT', 'PONDUSDT', 'DEGOUSDT', 'ALICEUSDT', 'LINAUSDT', 'PERPUSDT', 'SUPERUSDT', 'CFXUSDT', 'TKOUSDT', 'PUNDIXUSDT', 'TLMUSDT', 'BARUSDT']

eight = ['BNSOLUSDT', 'FORTHUSDT', 'BAKEUSDT', 'BURGERUSDT', 'SLPUSDT', 'SHIBUSDT', 'ICPUSDT', 'ARUSDT', 'MASKUSDT', 'LPTUSDT', 'XVGUSDT', 'ATAUSDT', 'GTCUSDT']

eightdop = ['ERNUSDT', 'KLAYUSDT', 'PHAUSDT', 'MLNUSDT', 'DEXEUSDT', 'C98USDT', 'CLVUSDT', 'QNTUSDT', 'FLOWUSDT', 'MINAUSDT', 'RAYUSDT', 'FARMUSDT']

nine = ['ALPACAUSDT', 'QUICKUSDT', 'MBOXUSDT', 'REQUSDT', 'GHSTUSDT', 'WAXPUSDT', 'GNOUSDT', 'XECUSDT', 'ELFUSDT', 'DYDXUSDT', 'IDEXUSDT']

ninedop = ['VIDTUSDT', 'GALAUSDT', 'ILVUSDT', 'YGGUSDT', 'SYSUSDT', 'DFUSDT', 'FIDAUSDT', 'AGLDUSDT', 'RADUSDT', 'BETAUSDT']

ten = ['RAREUSDT', 'LAZIOUSDT', 'CHESSUSDT', 'ADXUSDT', 'AUCTIONUSDT', 'DARUSDT', 'BNXUSDT', 'MOVRUSDT', 'CITYUSDT', 'ENSUSDT', 'QIUSDT']

tendop = ['PORTOUSDT', 'POWRUSDT', 'JASMYUSDT', 'AMPUSDT', 'PYRUSDT', 'ALCXUSDT', 'SANTOSUSDT', 'BICOUSDT', 'FLUXUSDT', 'FXSUSDT', 'VOXELUSDT']

eleven = ['HIGHUSDT', 'CVXUSDT', 'PEOPLEUSDT', 'SPELLUSDT', 'JOEUSDT', "DOGSUSDT", 'ACHUSDT', 'IMXUSDT', 'GLMRUSDT', 'LOKAUSDT', 'SCRTUSDT', 'API3USDT']

elevendop = ['1MBABYDOGEUSDT', 'BTTCUSDT', 'ACAUSDT', 'XNOUSDT', 'WOOUSDT', 'ALPINEUSDT', 'TUSDT', 'ASTRUSDT', 'GMTUSDT', 'KDAUSDT', 'APEUSDT', 'BSWUSDT', 'BIFIUSDT', 'TONUSDT']

twelve = ['STEEMUSDT', 'NEXOUSDT', 'REIUSDT', 'LDOUSDT', 'OPUSDT', 'RENDERUSDT', 'LEVERUSDT', 'STGUSDT', 'LUNCUSDT', 'GMXUSDT', 'POLYXUSDT', 'APTUSDT', 'BANANAUSDT']

twelvedop = ['OSMOUSDT', 'HFTUSDT', 'PHBUSDT', 'HOOKUSDT', 'MAGICUSDT', 'HIFIUSDT', 'GUSDT', 'RPLUSDT', 'PROSUSDT', 'GNSUSDT', 'SYNUSDT', 'VIBUSDT', 'SSVUSDT', 'ZROUSDT']

thirteenth = ['LUMIAUSDT', 'LQTYUSDT', 'AMBUSDT', 'USTCUSDT', 'GASUSDT', 'BOMEUSDT', 'GLMUSDT', 'PROMUSDT', 'LISTAUSDT', 'QKCUSDT', 'UFTUSDT', 'IDUSDT', 'ARBUSDT', 'OAXUSDT', 'ZKUSDT']

thirteenthdop = ['RDNTUSDT', 'WBTCUSDT', 'EDUUSDT', 'SUIUSDT', 'AERGOUSDT', 'PEPEUSDT', 'IOUSDT', 'FLOKIUSDT', 'ASTUSDT', 'SNTUSDT', 'COMBOUSDT', 'MAVUSDT', 'PENDLEUSDT', 'NOTUSDT']

fourteenth = ['ARKMUSDT', 'WBETHUSDT', 'WLDUSDT', 'SEIUSDT', 'CYBERUSDT', 'ARKUSDT', 'BBUSDT', 'CREAMUSDT', "HMSTRUSDT", 'GFTUSDT', 'IQUSDT', 'NTRNUSDT', 'TIAUSDT', 'MEMEUSDT', 'REZUSDT']

fourteenthdop = ['ORDIUSDT', 'BEAMXUSDT', 'PIVXUSDT', 'VICUSDT', 'BLURUSDT', 'VANRYUSDT', 'OMNIUSDT', 'JTOUSDT', '1000SATSUSDT', 'BONKUSDT', 'ACEUSDT', 'NFPUSDT', 'AIUSDT', 'TAOUSDT']

fifteenth = ['XAIUSDT', 'MANTAUSDT', 'ALTUSDT', 'JUPUSDT', 'PYTHUSDT', 'RONINUSDT', 'SAGAUSDT', 'DYMUSDT', 'PIXELUSDT', 'STRKUSDT', 'PORTALUSDT', 'PDAUSDT', 'AXLUSDT', 'TNSRUSDT']

fifteenthdop = ['WIFUSDT', 'METISUSDT', 'AEVOUSDT', 'ETHFIUSDT', 'ENAUSDT', 'WUSDT', 'NEIROUSDT', 'PROMUSDT', 'COOKIEUSDT', 'BIOUSDT', 'HYPEUSDT', 'SOPHUSDT', 'AUSDT', 'HUMAUSDT']

izg = []

all_cripts_workss = one + two + three + four + five + six + seven + eight + nine + ten + eleven + twelve + thirteenth + fourteenth + fifteenth + izg + \
    onedop + twodop + threedop + fourdop + fivedop + sixdop + sevendop + eightdop + ninedop + tendop + elevendop + twelvedop + \
    thirteenthdop + fourteenthdop + fifteenthdop

exchange = ccxt.binance()

# def equal(crypto: str, all_profit: float, profit_deal: float):
#     try:
#         values = (crypto, all_profit, profit_deal)
#
#         try:
#             connection = pymysql.connect(host='127.0.0.1', port=3306, user='banan_user', password='warlight123',
#                                              database='banans',
#                                              cursorclass=pymysql.cursors.DictCursor)
#             try:
#                 with connection.cursor() as cursor:
#                     insert_query = "INSERT INTO `check` (crypto, all_profit, profit_deal) " \
#                                    "VALUES (%s, %s, %s)"
#                     cursor.execute(insert_query, (values))
#                     connection.commit()
#             finally:
#                 connection.close()
#
#         except Exception as e:
#             telebot.TeleBot(telega_token).send_message(-695765690, f"SQL ERROR equal connect k bd: {e}\n")
#
#     except Exception as e:
#         telebot.TeleBot(telega_token).send_message(-695765690, f"SQL ERROR equal: {e}\n")

x = []

# for crypto in all_cripts_workss:
#     symbol = f'{crypto[:-4]}/USDT'
#     timeframe = '4h'
#     limit = 1000  # количество свечей для загрузки (~4 года данных при H4)
#
#     try:
#         ohlc = exchange.fetch_ohlcv(symbol, timeframe=timeframe, limit=limit)
#     except Exception as e:
#         print(f"Ошибка загрузки данных для {symbol}: {e}")
#         continue
#
#     df = pd.DataFrame(ohlc, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
#     df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
#
#     # Рассчитываем процентное изменение закрытия за свечу
#     df['change_percent'] = ((df['close'] - df['open']) / df['open']) * 100
#
#     # Условие входа: цена упала больше чем на 4.1%
#     df['buy_signal'] = df['change_percent'] <= -4.2
#
#     position = False
#     buy_price = 0
#     profit = []
#     holding_period = 0
#
#     for i in range(1, len(df)):
#         if df['buy_signal'].iloc[i] and not position:
#             buy_price = df['close'].iloc[i]
#             position = True
#             holding_period = 0
#
#         elif position:
#             holding_period += 1
#
#             # Проверяем минимальную цену (low) свечи — может быть срабатывание Stop Loss
#             current_low_return = (df['low'].iloc[i] - buy_price) / buy_price * 100
#
#             if current_low_return <= -5:  # Стоп-лосс по минимальной цене
#                 profit.append(-5.0)  # Фиксируем убыток -5%
#                 position = False
#
#             else:
#                 current_close_return = (df['close'].iloc[i] - buy_price) / buy_price * 100
#
#                 # Take Profit
#                 if current_close_return >= 1.15:
#                     profit.append(current_close_return)
#                     position = False
#
#                 # Выход по времени (3 свечи H4)
#                 elif holding_period >= 3:
#                     profit.append(current_close_return)
#                     position = False
#
#     total_profit = sum(profit)
#     win_rate = len([x for x in profit if x > 0]) / len(profit) * 100 if profit else 0
#     print(f"{crypto}")
#     print(f"Общая прибыль: {total_profit:.2f}%")
#     print(f"Процент прибыльных сделок: {win_rate:.2f}%")
#     print(f"Всего сделок: {len(profit)}")
#     x.append([crypto, float(f"{total_profit:.2f}")])
#     #equal(crypto, float(f"{total_profit:.2f}"), float(f"{win_rate:.2f}"))
#     time.sleep(0.5)


x = [['NEOUSDT', -9.74], ['LTCUSDT', 5.3], ['QTUMUSDT', 16.94], ['ADAUSDT', 12.91], ['XRPUSDT', 6.06], ['EOSUSDT', -1.2], ['IOTAUSDT', 5.43], ['XLMUSDT', 0.33], ['ONTUSDT', 12.3], ['TRXUSDT', 20.26], ['ETCUSDT', 20.07], ['ICXUSDT', -1.77], ['DASHUSDT', 15.05], ['THETAUSDT', 24.8], ['ENJUSDT', 12.13], ['ATOMUSDT', 6.95], ['TFUELUSDT', -4.21], ['ONEUSDT', 3.82], ['FTMUSDT', -34.59], ['ALGOUSDT', 2.34], ['DOGEUSDT', -11.15], ['DUSKUSDT', -13.48], ['ANKRUSDT', 6.07], ['RVNUSDT', 32.26], ['HBARUSDT', 23.7], ['NKNUSDT', 24.45], ['STXUSDT', 20.47], ['KAVAUSDT', 21.94], ['ARPAUSDT', 25.11], ['IOTXUSDT', -19.53], ['RLCUSDT', 0.89], ['CTXCUSDT', 16.61], ['BCHUSDT', 16.03], ['TROYUSDT', -5.48], ['VITEUSDT', -89.53], ['HIVEUSDT', -5.13], ['CHRUSDT', 16.0], ['ARDRUSDT', 8.38], ['MDTUSDT', 13.98], ['STMXUSDT', 108.55], ['KNCUSDT', 14.96], ['LRCUSDT', 7.91], ['COMPUSDT', -6.91], ['SCUSDT', 5.89], ['ZENUSDT', 16.44], ['SNXUSDT', -19.09], ['VTHOUSDT', -37.36], ['CATIUSDT', 70.56], ['CRVUSDT', 13.18], ['SANDUSDT', 14.39], ['NMRUSDT', -33.66], ['DOTUSDT', 16.14], ['LUNAUSDT', 5.02], ['RSRUSDT', 15.55], ['TRBUSDT', 0.29], ['SUSHIUSDT', 12.71], ['KSMUSDT', -7.0], ['EGLDUSDT', 22.6], ['DIAUSDT', 27.61], ['RUNEUSDT', -9.64], ['ALPHAUSDT', 13.07], ['AAVEUSDT', 46.92], ['NEARUSDT', 26.03], ['FILUSDT', 23.16], ['INJUSDT', -6.22], ['AUDIOUSDT', -6.74], ['CTKUSDT', -18.41], ['AKROUSDT', -1.54], ['AXSUSDT', 21.55], ['HARDUSDT', -15.6], ['STRAXUSDT', 7.39], ['UNFIUSDT', 16.02], ['RIFUSDT', 7.84], ['TRUUSDT', -11.86], ['CKBUSDT', 19.42], ['TWTUSDT', 22.26], ['FIROUSDT', 34.45], ['LITUSDT', -7.72], ['SFPUSDT', 12.62], ['DODOUSDT', 10.89], ['CAKEUSDT', 5.48], ['ACMUSDT', 4.8], ['BADGERUSDT', -9.26], ['FISUSDT', -21.2], ['BNSOLUSDT', -17.12], ['FORTHUSDT', 10.05], ['BAKEUSDT', -30.08], ['BURGERUSDT', -33.5], ['SLPUSDT', 12.18], ['SHIBUSDT', 0.52], ['ICPUSDT', 16.21], ['ARUSDT', -29.31], ['MASKUSDT', -9.35], ['LPTUSDT', -5.13], ['XVGUSDT', -7.48], ['ATAUSDT', -16.13], ['GTCUSDT', -23.83], ['ALPACAUSDT', -65.63], ['QUICKUSDT', 35.58], ['MBOXUSDT', -11.08], ['REQUSDT', 5.8], ['GHSTUSDT', 19.76], ['WAXPUSDT', 18.86], ['GNOUSDT', -2.2], ['XECUSDT', 14.98], ['ELFUSDT', 8.78], ['DYDXUSDT', -10.09], ['IDEXUSDT', 23.4], ['RAREUSDT', -0.6], ['LAZIOUSDT', 7.2], ['CHESSUSDT', -25.96], ['ADXUSDT', -16.44], ['AUCTIONUSDT', 3.15], ['DARUSDT', 23.32], ['BNXUSDT', 51.73], ['MOVRUSDT', 5.45], ['CITYUSDT', 9.79], ['ENSUSDT', 24.85], ['QIUSDT', 40.53], ['HIGHUSDT', -5.62], ['CVXUSDT', -1.24], ['PEOPLEUSDT', -52.27], ['SPELLUSDT', -3.73], ['JOEUSDT', -1.0], ['DOGSUSDT', -54.89], ['ACHUSDT', -14.43], ['IMXUSDT', 11.16], ['GLMRUSDT', 9.85], ['LOKAUSDT', -24.67], ['SCRTUSDT', -9.49], ['API3USDT', 3.97], ['STEEMUSDT', 20.06], ['NEXOUSDT', 12.73], ['REIUSDT', -3.95], ['LDOUSDT', -35.13], ['OPUSDT', 22.58], ['RENDERUSDT', 33.36], ['LEVERUSDT', 19.68], ['STGUSDT', -1.18], ['LUNCUSDT', 22.87], ['GMXUSDT', 37.03], ['POLYXUSDT', 0.86], ['APTUSDT', 16.57], ['BANANAUSDT', 32.67], ['LUMIAUSDT', -54.8], ['LQTYUSDT', -27.27], ['AMBUSDT', -54.88], ['USTCUSDT', 24.91], ['GASUSDT', -14.19], ['BOMEUSDT', -31.38], ['GLMUSDT', 16.2], ['PROMUSDT', -0.21], ['LISTAUSDT', 11.18], ['QKCUSDT', 0.94], ['UFTUSDT', -40.07], ['IDUSDT', -1.23], ['ARBUSDT', 24.71], ['OAXUSDT', -56.77], ['ZKUSDT', 23.43], ['ARKMUSDT', -16.13], ['WBETHUSDT', 5.75], ['WLDUSDT', 5.84], ['SEIUSDT', 3.19], ['CYBERUSDT', -0.88], ['ARKUSDT', 71.56], ['BBUSDT', 3.98], ['CREAMUSDT', 4.01], ['HMSTRUSDT', -3.93], ['GFTUSDT', -16.09], ['IQUSDT', -7.04], ['NTRNUSDT', -13.92], ['TIAUSDT', -13.73], ['MEMEUSDT', -17.45], ['REZUSDT', 3.16], ['XAIUSDT', -15.26], ['MANTAUSDT', -11.58], ['ALTUSDT', -18.54], ['JUPUSDT', 6.7], ['PYTHUSDT', -21.83], ['RONINUSDT', 20.38], ['SAGAUSDT', -36.42], ['DYMUSDT', -12.17], ['PIXELUSDT', -40.71], ['STRKUSDT', -4.84], ['PORTALUSDT', -60.07], ['PDAUSDT', -47.01], ['AXLUSDT', 41.61], ['TNSRUSDT', 13.42], ['NULSUSDT', 2.48], ['VETUSDT', -15.05], ['LINKUSDT', 12.5], ['ONGUSDT', 36.74], ['HOTUSDT', -17.2], ['ZILUSDT', 11.41], ['ZRXUSDT', 6.3], ['FETUSDT', 3.36], ['BATUSDT', 20.65], ['ZECUSDT', 32.26], ['IOSTUSDT', 1.37], ['CELRUSDT', -1.25], ['WINUSDT', 1.3], ['COSUSDT', 13.93], ['MTLUSDT', 12.84], ['DENTUSDT', 3.43], ['KEYUSDT', -28.85], ['WANUSDT', 13.4], ['FUNUSDT', 0.62], ['CVCUSDT', -4.37], ['CHZUSDT', 20.69], ['BANDUSDT', 5.39], ['XTZUSDT', 25.9], ['RENUSDT', 44.77], ['FTTUSDT', 21.72], ['OGNUSDT', -11.43], ['WRXUSDT', -16.93], ['LSKUSDT', 10.29], ['BNTUSDT', 10.82], ['LTOUSDT', -16.69], ['MBLUSDT', 8.01], ['COTIUSDT', 5.18], ['STPTUSDT', 44.78], ['DATAUSDT', 24.65], ['SOLUSDT', -6.77], ['CTSIUSDT', 5.85], ['DGBUSDT', 57.17], ['SXPUSDT', 11.3], ['MKRUSDT', 9.91], ['DCRUSDT', 14.71], ['STORJUSDT', 15.68], ['MANAUSDT', 17.18], ['YFIUSDT', 24.58], ['BALUSDT', 26.84], ['BLZUSDT', 23.62], ['IRISUSDT', -2.11], ['KMDUSDT', 3.76], ['JSTUSDT', 1.95], ['FIOUSDT', 19.05], ['UMAUSDT', 33.98], ['BELUSDT', 1.47], ['WINGUSDT', -57.88], ['UNIUSDT', 10.24], ['OXTUSDT', 7.8], ['SUNUSDT', 23.55], ['AVAXUSDT', 16.65], ['FLMUSDT', -11.5], ['ORNUSDT', -17.0], ['UTKUSDT', 31.83], ['XVSUSDT', -11.33], ['EIGENUSDT', -60.34], ['ROSEUSDT', 11.93], ['AVAUSDT', 9.54], ['SKLUSDT', 8.7], ['GRTUSDT', -0.3], ['JUVUSDT', -4.24], ['PSGUSDT', 22.59], ['1INCHUSDT', 23.46], ['OGUSDT', 5.06], ['ATMUSDT', 5.11], ['ASRUSDT', 27.34], ['CELOUSDT', 27.86], ['TURBOUSDT', 14.54], ['SCRUSDT', 17.87], ['OMUSDT', 83.41], ['PONDUSDT', 7.81], ['DEGOUSDT', 16.56], ['ALICEUSDT', -11.83], ['LINAUSDT', -34.39], ['PERPUSDT', -57.25], ['SUPERUSDT', -33.7], ['CFXUSDT', 8.67], ['TKOUSDT', 20.49], ['PUNDIXUSDT', 28.12], ['TLMUSDT', 0.56], ['BARUSDT', 15.58], ['ERNUSDT', 62.18], ['KLAYUSDT', -2.83], ['PHAUSDT', -40.48], ['MLNUSDT', 50.68], ['DEXEUSDT', 10.21], ['C98USDT', 0.28], ['CLVUSDT', 41.45], ['QNTUSDT', -3.22], ['FLOWUSDT', 23.45], ['MINAUSDT', 16.2], ['RAYUSDT', -35.0], ['FARMUSDT', 9.39], ['VIDTUSDT', 8.18], ['GALAUSDT', 20.31], ['ILVUSDT', 18.25], ['YGGUSDT', -19.58], ['SYSUSDT', -21.59], ['DFUSDT', 3.32], ['FIDAUSDT', -21.47], ['AGLDUSDT', 17.51], ['RADUSDT', -1.36], ['BETAUSDT', -45.68], ['PORTOUSDT', 30.88], ['POWRUSDT', 29.08], ['JASMYUSDT', 18.21], ['AMPUSDT', -28.65], ['PYRUSDT', 14.64], ['ALCXUSDT', -14.07], ['SANTOSUSDT', 39.45], ['BICOUSDT', -8.71], ['FLUXUSDT', 14.11], ['FXSUSDT', -11.51], ['VOXELUSDT', 1.81], ['1MBABYDOGEUSDT', -25.6], ['BTTCUSDT', 9.91], ['ACAUSDT', 0.56], ['XNOUSDT', 11.41], ['WOOUSDT', -0.26], ['ALPINEUSDT', -3.46], ['TUSDT', 20.15], ['ASTRUSDT', 13.06], ['GMTUSDT', 13.88], ['KDAUSDT', -4.55], ['APEUSDT', -23.13], ['BSWUSDT', -1.01], ['BIFIUSDT', 9.36], ['TONUSDT', -0.1], ['OSMOUSDT', 17.06], ['HFTUSDT', 4.38], ['PHBUSDT', -25.47], ['HOOKUSDT', -12.86], ['MAGICUSDT', -14.04], ['HIFIUSDT', -33.83], ['GUSDT', 27.03], ['RPLUSDT', -10.65], ['PROSUSDT', 104.5], ['GNSUSDT', 3.01], ['SYNUSDT', -33.37], ['VIBUSDT', -37.01], ['SSVUSDT', -26.94], ['ZROUSDT', -41.48], ['RDNTUSDT', -7.83], ['WBTCUSDT', 8.63], ['EDUUSDT', -7.44], ['SUIUSDT', 0.35], ['AERGOUSDT', 46.66], ['PEPEUSDT', -15.08], ['IOUSDT', 31.83], ['FLOKIUSDT', -8.15], ['ASTUSDT', 2.82], ['SNTUSDT', 5.1], ['COMBOUSDT', -48.51], ['MAVUSDT', 13.63], ['PENDLEUSDT', -3.06], ['NOTUSDT', 17.46], ['ORDIUSDT', -45.09], ['BEAMXUSDT', -23.91], ['PIVXUSDT', -5.41], ['VICUSDT', 18.13], ['BLURUSDT', 36.18], ['VANRYUSDT', -36.75], ['OMNIUSDT', 7.28], ['JTOUSDT', -20.39], ['1000SATSUSDT', -3.88], ['BONKUSDT', -17.35], ['ACEUSDT', 3.21], ['NFPUSDT', -29.34], ['AIUSDT', 11.77], ['TAOUSDT', -6.63], ['WIFUSDT', -48.07], ['METISUSDT', 13.3], ['AEVOUSDT', 7.86], ['ETHFIUSDT', -0.67], ['ENAUSDT', -20.28], ['WUSDT', -0.6], ['NEIROUSDT', -72.25], ['PROMUSDT', -0.21], ['COOKIEUSDT', -49.83], ['BIOUSDT', -36.7], ['HYPEUSDT', 2.95], ['SOPHUSDT', 34.91], ['AUSDT', 1.03], ['HUMAUSDT', -27.0]]


z = ['NEOUSDT', 'LTCUSDT', 'QTUMUSDT', 'ADAUSDT', 'XRPUSDT', 'EOSUSDT', 'IOTAUSDT', 'XLMUSDT', 'ONTUSDT', 'TRXUSDT', 'ETCUSDT', 'ICXUSDT', 'DASHUSDT', 'THETAUSDT', 'ENJUSDT', 'ATOMUSDT', 'TFUELUSDT', 'ONEUSDT', 'ALGOUSDT', 'ANKRUSDT', 'RVNUSDT', 'HBARUSDT', 'NKNUSDT', 'STXUSDT', 'KAVAUSDT', 'ARPAUSDT', 'RLCUSDT', 'CTXCUSDT', 'BCHUSDT', 'TROYUSDT', 'HIVEUSDT', 'CHRUSDT', 'ARDRUSDT', 'MDTUSDT', 'STMXUSDT', 'KNCUSDT', 'LRCUSDT', 'COMPUSDT', 'SCUSDT', 'ZENUSDT', 'CATIUSDT', 'CRVUSDT', 'SANDUSDT', 'DOTUSDT', 'LUNAUSDT', 'RSRUSDT', 'TRBUSDT', 'SUSHIUSDT', 'KSMUSDT', 'EGLDUSDT', 'DIAUSDT', 'RUNEUSDT', 'ALPHAUSDT', 'AAVEUSDT', 'NEARUSDT', 'FILUSDT', 'INJUSDT', 'AUDIOUSDT', 'AKROUSDT', 'AXSUSDT', 'STRAXUSDT', 'UNFIUSDT', 'RIFUSDT', 'CKBUSDT', 'TWTUSDT', 'FIROUSDT', 'LITUSDT', 'SFPUSDT', 'DODOUSDT', 'CAKEUSDT', 'ACMUSDT', 'BADGERUSDT', 'FORTHUSDT', 'SLPUSDT', 'SHIBUSDT', 'ICPUSDT', 'MASKUSDT', 'LPTUSDT', 'XVGUSDT', 'QUICKUSDT', 'REQUSDT', 'GHSTUSDT', 'WAXPUSDT', 'GNOUSDT', 'XECUSDT', 'ELFUSDT', 'IDEXUSDT', 'RAREUSDT', 'LAZIOUSDT', 'AUCTIONUSDT', 'DARUSDT', 'BNXUSDT', 'MOVRUSDT', 'CITYUSDT', 'ENSUSDT', 'QIUSDT', 'HIGHUSDT', 'CVXUSDT', 'SPELLUSDT', 'JOEUSDT', 'IMXUSDT', 'GLMRUSDT', 'SCRTUSDT', 'API3USDT', 'STEEMUSDT', 'NEXOUSDT', 'REIUSDT', 'OPUSDT', 'RENDERUSDT', 'LEVERUSDT', 'STGUSDT', 'LUNCUSDT', 'GMXUSDT', 'POLYXUSDT', 'APTUSDT', 'BANANAUSDT', 'USTCUSDT', 'GLMUSDT', 'PROMUSDT', 'LISTAUSDT', 'QKCUSDT', 'IDUSDT', 'ARBUSDT', 'ZKUSDT', 'WBETHUSDT', 'WLDUSDT', 'SEIUSDT', 'CYBERUSDT', 'ARKUSDT', 'BBUSDT', 'CREAMUSDT', 'HMSTRUSDT', 'IQUSDT', 'REZUSDT', 'JUPUSDT', 'RONINUSDT', 'STRKUSDT', 'AXLUSDT', 'TNSRUSDT', 'NULSUSDT', 'LINKUSDT', 'ONGUSDT', 'ZILUSDT', 'ZRXUSDT', 'FETUSDT', 'BATUSDT', 'ZECUSDT', 'IOSTUSDT', 'CELRUSDT', 'WINUSDT', 'COSUSDT', 'MTLUSDT', 'DENTUSDT', 'WANUSDT', 'FUNUSDT', 'CVCUSDT', 'CHZUSDT', 'BANDUSDT', 'XTZUSDT', 'RENUSDT', 'FTTUSDT', 'LSKUSDT', 'BNTUSDT', 'MBLUSDT', 'COTIUSDT', 'STPTUSDT', 'DATAUSDT', 'SOLUSDT', 'CTSIUSDT', 'DGBUSDT', 'SXPUSDT', 'MKRUSDT', 'DCRUSDT', 'STORJUSDT', 'MANAUSDT', 'YFIUSDT', 'BALUSDT', 'BLZUSDT', 'IRISUSDT', 'KMDUSDT', 'JSTUSDT', 'FIOUSDT', 'UMAUSDT', 'BELUSDT', 'UNIUSDT', 'OXTUSDT', 'SUNUSDT', 'AVAXUSDT', 'UTKUSDT', 'ROSEUSDT', 'AVAUSDT', 'SKLUSDT', 'GRTUSDT', 'JUVUSDT', 'PSGUSDT', '1INCHUSDT', 'OGUSDT', 'ATMUSDT', 'ASRUSDT', 'CELOUSDT', 'TURBOUSDT', 'SCRUSDT', 'OMUSDT', 'PONDUSDT', 'DEGOUSDT', 'CFXUSDT', 'TKOUSDT', 'PUNDIXUSDT', 'TLMUSDT', 'BARUSDT', 'ERNUSDT', 'KLAYUSDT', 'MLNUSDT', 'DEXEUSDT', 'C98USDT', 'CLVUSDT', 'QNTUSDT', 'FLOWUSDT', 'MINAUSDT', 'FARMUSDT', 'VIDTUSDT', 'GALAUSDT', 'ILVUSDT', 'DFUSDT', 'AGLDUSDT', 'RADUSDT', 'PORTOUSDT', 'POWRUSDT', 'JASMYUSDT', 'PYRUSDT', 'SANTOSUSDT', 'BICOUSDT', 'FLUXUSDT', 'VOXELUSDT', 'BTTCUSDT', 'ACAUSDT', 'XNOUSDT', 'WOOUSDT', 'ALPINEUSDT', 'TUSDT', 'ASTRUSDT', 'GMTUSDT', 'KDAUSDT', 'BSWUSDT', 'BIFIUSDT', 'TONUSDT', 'OSMOUSDT', 'HFTUSDT', 'GUSDT', 'PROSUSDT', 'GNSUSDT', 'RDNTUSDT', 'WBTCUSDT', 'EDUUSDT', 'SUIUSDT', 'AERGOUSDT', 'IOUSDT', 'FLOKIUSDT', 'ASTUSDT', 'SNTUSDT', 'MAVUSDT', 'PENDLEUSDT', 'NOTUSDT', 'PIVXUSDT', 'VICUSDT', 'BLURUSDT', 'OMNIUSDT', '1000SATSUSDT', 'ACEUSDT', 'AIUSDT', 'TAOUSDT', 'METISUSDT', 'AEVOUSDT', 'ETHFIUSDT', 'WUSDT', 'PROMUSDT', 'HYPEUSDT', 'SOPHUSDT', 'AUSDT']

y = ['LTCUSDT', 'QTUMUSDT', 'ADAUSDT', 'XRPUSDT', 'EOSUSDT', 'XLMUSDT', 'ONTUSDT', 'TRXUSDT', 'ETCUSDT', 'DASHUSDT', 'THETAUSDT', 'ATOMUSDT', 'TFUELUSDT', 'FTMUSDT', 'RVNUSDT', 'HBARUSDT', 'KAVAUSDT', 'ARPAUSDT', 'CTXCUSDT', 'BCHUSDT', 'CHRUSDT', 'MDTUSDT', 'STMXUSDT', 'KNCUSDT', 'LRCUSDT', 'ZENUSDT', 'CATIUSDT', 'CRVUSDT', 'DOTUSDT', 'RSRUSDT', 'TRBUSDT', 'EGLDUSDT', 'DIAUSDT', 'ALPHAUSDT', 'AAVEUSDT', 'NEARUSDT', 'FILUSDT', 'AXSUSDT', 'STRAXUSDT', 'UNFIUSDT', 'RIFUSDT', 'CKBUSDT', 'TWTUSDT', 'FIROUSDT', 'LITUSDT', 'SFPUSDT', 'CAKEUSDT', 'BADGERUSDT', 'FORTHUSDT', 'ICPUSDT', 'MASKUSDT', 'XVGUSDT', 'ALPACAUSDT', 'QUICKUSDT', 'MBOXUSDT', 'REQUSDT', 'GHSTUSDT', 'WAXPUSDT', 'GNOUSDT', 'XECUSDT', 'ELFUSDT', 'IDEXUSDT', 'RAREUSDT', 'LAZIOUSDT', 'DARUSDT', 'BNXUSDT', 'CITYUSDT', 'ENSUSDT', 'QIUSDT', 'CVXUSDT', 'SPELLUSDT', 'IMXUSDT', 'GLMRUSDT', 'STEEMUSDT', 'NEXOUSDT', 'OPUSDT', 'RENDERUSDT', 'LEVERUSDT', 'LUNCUSDT', 'GMXUSDT', 'BANANAUSDT', 'USTCUSDT', 'GASUSDT', 'GLMUSDT', 'PROMUSDT', 'QKCUSDT', 'ARBUSDT', 'ZKUSDT', 'WBETHUSDT', 'ARKUSDT', 'CREAMUSDT', 'REZUSDT', 'JUPUSDT', 'RONINUSDT', 'STRKUSDT', 'PDAUSDT', 'AXLUSDT', 'NULSUSDT', 'ONGUSDT', 'ZILUSDT', 'FETUSDT', 'BATUSDT', 'ZECUSDT', 'COSUSDT', 'MTLUSDT', 'DENTUSDT', 'WANUSDT', 'CHZUSDT', 'BANDUSDT', 'XTZUSDT', 'RENUSDT', 'FTTUSDT', 'LSKUSDT', 'BNTUSDT', 'MBLUSDT', 'COTIUSDT', 'STPTUSDT', 'DATAUSDT', 'SOLUSDT', 'CTSIUSDT', 'DGBUSDT', 'SXPUSDT', 'MKRUSDT', 'DCRUSDT', 'STORJUSDT', 'MANAUSDT', 'YFIUSDT', 'BALUSDT', 'BLZUSDT', 'IRISUSDT', 'KMDUSDT', 'JSTUSDT', 'FIOUSDT', 'UMAUSDT', 'BELUSDT', 'OXTUSDT', 'SUNUSDT', 'AVAXUSDT', 'ORNUSDT', 'UTKUSDT', 'AVAUSDT', 'SKLUSDT', 'PSGUSDT', '1INCHUSDT', 'OGUSDT', 'ASRUSDT', 'CELOUSDT', 'TURBOUSDT', 'SCRUSDT', 'OMUSDT', 'PONDUSDT', 'DEGOUSDT', 'CFXUSDT', 'TKOUSDT', 'PUNDIXUSDT', 'TLMUSDT', 'BARUSDT', 'ERNUSDT', 'KLAYUSDT', 'MLNUSDT', 'DEXEUSDT', 'CLVUSDT', 'QNTUSDT', 'FLOWUSDT', 'MINAUSDT', 'VIDTUSDT', 'GALAUSDT', 'SYSUSDT', 'DFUSDT', 'AGLDUSDT', 'PORTOUSDT', 'POWRUSDT', 'JASMYUSDT', 'PYRUSDT', 'SANTOSUSDT', 'BTTCUSDT', 'XNOUSDT', 'ALPINEUSDT', 'TUSDT', 'ASTRUSDT', 'KDAUSDT', 'APEUSDT', 'BIFIUSDT', 'OSMOUSDT', 'GUSDT', 'PROSUSDT', 'SSVUSDT', 'WBTCUSDT', 'EDUUSDT', 'AERGOUSDT', 'IOUSDT', 'SNTUSDT', 'MAVUSDT', 'PENDLEUSDT', 'NOTUSDT', 'VICUSDT', 'BLURUSDT', 'OMNIUSDT', '1000SATSUSDT', 'AIUSDT', 'METISUSDT', 'AEVOUSDT', 'ETHFIUSDT', 'ENAUSDT', 'PROMUSDT', 'COOKIEUSDT', 'HYPEUSDT', 'SOPHUSDT', 'AUSDT']

equal("`vision_equals_6h`", "GDFG", 2, 2, 2, 2, 2, 2)
sql_del("`vision_equals_6h`")