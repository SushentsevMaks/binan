import time

import ccxt
import pandas as pd
import pymysql
import telebot
import keys


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

def equal(crypto: str, all_profit: float, profit_deal: float):
    try:
        values = (crypto, all_profit, profit_deal)

        try:
            connection = pymysql.connect(host='127.0.0.1', port=3306, user='banan_user', password='warlight123',
                                             database='banans',
                                             cursorclass=pymysql.cursors.DictCursor)
            try:
                with connection.cursor() as cursor:
                    insert_query = "INSERT INTO `check` (crypto, all_profit, profit_deal) " \
                                   "VALUES (%s, %s, %s)"
                    cursor.execute(insert_query, (values))
                    connection.commit()
            finally:
                connection.close()

        except Exception as e:
            telebot.TeleBot(telega_token).send_message(-695765690, f"SQL ERROR equal connect k bd: {e}\n")

    except Exception as e:
        telebot.TeleBot(telega_token).send_message(-695765690, f"SQL ERROR equal: {e}\n")

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
#     holding_period = 0  # кол-во свечей с момента покупки
#
#     for i in range(1, len(df)):
#         if df['buy_signal'].iloc[i] and not position:
#             buy_price = df['close'].iloc[i]
#             position = True
#             holding_period = 0  # сброс счётчика времени
#
#         elif position:
#             holding_period += 1
#             current_return = (df['close'].iloc[i] - buy_price) / buy_price * 100
#
#             # Условия выхода
#             if current_return >= 1.15:  # Take Profit
#                 profit.append(current_return)
#                 position = False
#             elif current_return <= -5:  # Stop Loss
#                 profit.append(current_return)
#                 position = False
#             elif holding_period >= 3:  # Выход по времени (3 H4 свечи)
#                 profit.append(current_return)
#                 position = False
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

x = [['NEOUSDT', -28.43], ['LTCUSDT', 0.48], ['QTUMUSDT', -5.26], ['ADAUSDT', -0.63], ['XRPUSDT', -1.98], ['EOSUSDT', -4.15], ['IOTAUSDT', -23.71], ['XLMUSDT', -2.7], ['ONTUSDT', 2.13], ['TRXUSDT', 20.26], ['ETCUSDT', 3.35], ['ICXUSDT', -19.23], ['DASHUSDT', 1.51], ['THETAUSDT', -7.95], ['ENJUSDT', -13.93], ['ATOMUSDT', 4.9], ['TFUELUSDT', -8.62], ['ONEUSDT', -22.73], ['FTMUSDT', -2.32], ['ALGOUSDT', -13.36], ['DOGEUSDT', -13.56], ['DUSKUSDT', -19.95], ['ANKRUSDT', -12.94], ['RVNUSDT', 55.73], ['HBARUSDT', 16.22], ['NKNUSDT', -19.79], ['STXUSDT', -13.97], ['KAVAUSDT', 29.93], ['ARPAUSDT', 12.85], ['IOTXUSDT', -10.63], ['RLCUSDT', -21.45], ['CTXCUSDT', -9.45], ['BCHUSDT', -9.27], ['TROYUSDT', -67.52], ['VITEUSDT', -107.97], ['HIVEUSDT', -30.57], ['CHRUSDT', -3.65], ['ARDRUSDT', -19.16], ['MDTUSDT', 0.89], ['STMXUSDT', 88.75], ['KNCUSDT', -9.34], ['LRCUSDT', -2.92], ['COMPUSDT', -30.7], ['SCUSDT', -12.32], ['ZENUSDT', -5.22], ['SNXUSDT', -34.68], ['VTHOUSDT', -30.64], ['CATIUSDT', 0.92], ['CRVUSDT', 4.89], ['SANDUSDT', -15.56], ['NMRUSDT', -35.82], ['DOTUSDT', 3.54], ['LUNAUSDT', -10.82], ['RSRUSDT', -2.21], ['TRBUSDT', 11.81], ['SUSHIUSDT', -11.47], ['KSMUSDT', -20.21], ['EGLDUSDT', -1.35], ['DIAUSDT', 3.15], ['RUNEUSDT', -11.25], ['ALPHAUSDT', 7.58], ['AAVEUSDT', 23.83], ['NEARUSDT', -2.64], ['FILUSDT', 22.37], ['INJUSDT', -14.23], ['AUDIOUSDT', -31.45], ['CTKUSDT', -28.48], ['AKROUSDT', -64.74], ['AXSUSDT', 4.78], ['HARDUSDT', -132.22], ['STRAXUSDT', -0.45], ['UNFIUSDT', 28.06], ['RIFUSDT', 6.39], ['TRUUSDT', -24.37], ['CKBUSDT', -4.08], ['TWTUSDT', -5.93], ['FIROUSDT', 23.91], ['LITUSDT', 69.24], ['SFPUSDT', 12.62], ['DODOUSDT', -23.67], ['CAKEUSDT', -5.17], ['ACMUSDT', -22.47], ['BADGERUSDT', 18.86], ['FISUSDT', -44.74], ['BNSOLUSDT', -18.21], ['FORTHUSDT', 26.82], ['BAKEUSDT', -40.18], ['BURGERUSDT', -114.99], ['SLPUSDT', -19.9], ['SHIBUSDT', -18.05], ['ICPUSDT', -8.28], ['ARUSDT', -29.32], ['MASKUSDT', 1.62], ['LPTUSDT', -45.58], ['XVGUSDT', 6.4], ['ATAUSDT', -24.45], ['GTCUSDT', -36.44], ['ALPACAUSDT', 287.97], ['QUICKUSDT', 42.53], ['MBOXUSDT', -8.02], ['REQUSDT', 13.7], ['GHSTUSDT', -0.91], ['WAXPUSDT', 0.16], ['GNOUSDT', -4.99], ['XECUSDT', -8.78], ['ELFUSDT', -4.14], ['DYDXUSDT', -21.95], ['IDEXUSDT', 29.61], ['RAREUSDT', 9.48], ['LAZIOUSDT', 13.94], ['CHESSUSDT', -61.59], ['ADXUSDT', -13.32], ['AUCTIONUSDT', -19.75], ['DARUSDT', 22.84], ['BNXUSDT', 61.58], ['MOVRUSDT', -14.61], ['CITYUSDT', -2.71], ['ENSUSDT', 6.71], ['QIUSDT', 21.71], ['HIGHUSDT', -34.39], ['CVXUSDT', -0.48], ['PEOPLEUSDT', -64.16], ['SPELLUSDT', -0.49], ['JOEUSDT', -19.14], ['DOGSUSDT', -72.21], ['ACHUSDT', -44.41], ['IMXUSDT', -2.93], ['GLMRUSDT', 10.0], ['LOKAUSDT', -37.64], ['SCRTUSDT', -23.44], ['API3USDT', -16.07], ['STEEMUSDT', 2.75], ['NEXOUSDT', 12.74], ['REIUSDT', -10.61], ['LDOUSDT', -29.63], ['OPUSDT', -5.35], ['RENDERUSDT', 12.12], ['LEVERUSDT', -7.9], ['STGUSDT', -14.67], ['LUNCUSDT', -1.66], ['GMXUSDT', 30.63], ['POLYXUSDT', -23.93], ['APTUSDT', -17.17], ['BANANAUSDT', 8.16], ['LUMIAUSDT', -64.28], ['LQTYUSDT', -47.95], ['AMBUSDT', -77.75], ['USTCUSDT', 0.88], ['GASUSDT', 14.76], ['BOMEUSDT', -45.2], ['GLMUSDT', -8.54], ['PROMUSDT', -8.65], ['LISTAUSDT', -27.66], ['QKCUSDT', -7.57], ['UFTUSDT', -55.8], ['IDUSDT', -25.17], ['ARBUSDT', -4.84], ['OAXUSDT', -83.53], ['ZKUSDT', 6.72], ['ARKMUSDT', -51.02], ['WBETHUSDT', 8.52], ['WLDUSDT', -14.58], ['SEIUSDT', -28.78], ['CYBERUSDT', -11.72], ['ARKUSDT', 35.85], ['BBUSDT', -17.76], ['CREAMUSDT', 102.27], ['HMSTRUSDT', -21.86], ['GFTUSDT', -34.37], ['IQUSDT', -26.13], ['NTRNUSDT', -23.26], ['TIAUSDT', -17.3], ['MEMEUSDT', -46.86], ['REZUSDT', 25.33], ['XAIUSDT', -34.84], ['MANTAUSDT', -31.61], ['ALTUSDT', -36.06], ['JUPUSDT', -9.27], ['PYTHUSDT', -52.49], ['RONINUSDT', 6.42], ['SAGAUSDT', -40.95], ['DYMUSDT', -29.39], ['PIXELUSDT', -69.75], ['STRKUSDT', 14.21], ['PORTALUSDT', -43.86], ['PDAUSDT', -7.78], ['AXLUSDT', 13.43], ['TNSRUSDT', -11.12], ['NULSUSDT', 22.11], ['VETUSDT', -11.71], ['LINKUSDT', -10.28], ['ONGUSDT', 33.08], ['HOTUSDT', -12.39], ['ZILUSDT', -2.43], ['ZRXUSDT', -16.1], ['FETUSDT', 3.06], ['BATUSDT', 4.52], ['ZECUSDT', 5.72], ['IOSTUSDT', -17.7], ['CELRUSDT', -28.45], ['WINUSDT', -12.89], ['COSUSDT', -0.05], ['MTLUSDT', -0.51], ['DENTUSDT', -0.87], ['KEYUSDT', -21.84], ['WANUSDT', -5.47], ['FUNUSDT', -19.05], ['CVCUSDT', -10.36], ['CHZUSDT', 11.32], ['BANDUSDT', -4.85], ['XTZUSDT', 6.88], ['RENUSDT', 48.68], ['FTTUSDT', 22.99], ['OGNUSDT', -18.4], ['WRXUSDT', -63.0], ['LSKUSDT', -4.6], ['BNTUSDT', -9.9], ['LTOUSDT', -22.14], ['MBLUSDT', -6.41], ['COTIUSDT', 15.14], ['STPTUSDT', 32.87], ['DATAUSDT', 12.84], ['SOLUSDT', -8.54], ['CTSIUSDT', -3.05], ['DGBUSDT', 38.08], ['SXPUSDT', -5.72], ['MKRUSDT', 15.39], ['DCRUSDT', 1.04], ['STORJUSDT', -4.44], ['MANAUSDT', -0.74], ['YFIUSDT', 25.72], ['BALUSDT', 32.8], ['BLZUSDT', 51.62], ['IRISUSDT', 16.08], ['KMDUSDT', 2.24], ['JSTUSDT', -0.59], ['FIOUSDT', -6.04], ['UMAUSDT', 12.94], ['BELUSDT', 10.68], ['WINGUSDT', -88.54], ['UNIUSDT', -17.58], ['OXTUSDT', -3.4], ['SUNUSDT', 23.55], ['AVAXUSDT', -8.22], ['FLMUSDT', -55.8], ['ORNUSDT', 17.1], ['UTKUSDT', 45.07], ['XVSUSDT', -26.47], ['EIGENUSDT', -24.18], ['ROSEUSDT', -16.68], ['AVAUSDT', -9.33], ['SKLUSDT', 21.81], ['GRTUSDT', -24.63], ['JUVUSDT', -13.73], ['PSGUSDT', 20.06], ['1INCHUSDT', 4.09], ['OGUSDT', -5.83], ['ATMUSDT', -13.88], ['ASRUSDT', 9.94], ['CELOUSDT', 10.91], ['TURBOUSDT', 0.46], ['SCRUSDT', 29.62], ['OMUSDT', 104.57], ['PONDUSDT', -2.54], ['DEGOUSDT', 24.3], ['ALICEUSDT', -23.27], ['LINAUSDT', -91.42], ['PERPUSDT', -82.15], ['SUPERUSDT', -18.95], ['CFXUSDT', 27.42], ['TKOUSDT', 25.74], ['PUNDIXUSDT', 8.11], ['TLMUSDT', -7.55], ['BARUSDT', -7.88], ['ERNUSDT', 55.3], ['KLAYUSDT', 11.48], ['PHAUSDT', -77.59], ['MLNUSDT', 61.33], ['DEXEUSDT', 51.0], ['C98USDT', -11.62], ['CLVUSDT', 144.11], ['QNTUSDT', -3.58], ['FLOWUSDT', 4.34], ['MINAUSDT', -4.39], ['RAYUSDT', -10.24], ['FARMUSDT', -11.86], ['VIDTUSDT', 30.25], ['GALAUSDT', -5.98], ['ILVUSDT', -10.49], ['YGGUSDT', -22.95], ['SYSUSDT', -3.71], ['DFUSDT', 8.88], ['FIDAUSDT', -32.53], ['AGLDUSDT', 8.22], ['RADUSDT', -11.66], ['BETAUSDT', -98.1], ['PORTOUSDT', 32.96], ['POWRUSDT', 8.97], ['JASMYUSDT', 11.64], ['AMPUSDT', -51.59], ['PYRUSDT', -0.83], ['ALCXUSDT', -16.59], ['SANTOSUSDT', 39.45], ['BICOUSDT', -41.69], ['FLUXUSDT', -16.86], ['FXSUSDT', -40.09], ['VOXELUSDT', -34.42], ['1MBABYDOGEUSDT', -55.75], ['BTTCUSDT', 10.75], ['ACAUSDT', -37.89], ['XNOUSDT', 5.57], ['WOOUSDT', -31.24], ['ALPINEUSDT', -6.24], ['TUSDT', 10.72], ['ASTRUSDT', -1.54], ['GMTUSDT', -12.92], ['KDAUSDT', -7.43], ['APEUSDT', -9.0], ['BSWUSDT', -59.32], ['BIFIUSDT', 2.03], ['TONUSDT', -17.92], ['OSMOUSDT', 9.83], ['HFTUSDT', -29.42], ['PHBUSDT', -44.26], ['HOOKUSDT', -17.59], ['MAGICUSDT', -27.33], ['HIFIUSDT', -38.93], ['GUSDT', 9.47], ['RPLUSDT', -12.09], ['PROSUSDT', 43.2], ['GNSUSDT', -15.05], ['SYNUSDT', -11.86], ['VIBUSDT', -50.51], ['SSVUSDT', -7.54], ['ZROUSDT', -77.44], ['RDNTUSDT', -17.26], ['WBTCUSDT', 8.63], ['EDUUSDT', -7.75], ['SUIUSDT', -27.18], ['AERGOUSDT', 41.34], ['PEPEUSDT', -24.41], ['IOUSDT', 25.99], ['FLOKIUSDT', -28.46], ['ASTUSDT', -29.82], ['SNTUSDT', 0.24], ['COMBOUSDT', -81.48], ['MAVUSDT', -9.39], ['PENDLEUSDT', -2.84], ['NOTUSDT', 41.3], ['ORDIUSDT', -34.38], ['BEAMXUSDT', -48.73], ['PIVXUSDT', -18.53], ['VICUSDT', 2.34], ['BLURUSDT', 14.35], ['VANRYUSDT', -44.8], ['OMNIUSDT', -2.28], ['JTOUSDT', -16.57], ['1000SATSUSDT', -0.54], ['BONKUSDT', -30.56], ['ACEUSDT', -24.55], ['NFPUSDT', -55.15], ['AIUSDT', -6.99], ['TAOUSDT', -32.63], ['WIFUSDT', -56.27], ['METISUSDT', -6.33], ['AEVOUSDT', -6.81], ['ETHFIUSDT', 1.09], ['ENAUSDT', -5.0], ['WUSDT', -35.75], ['NEIROUSDT', -72.18], ['PROMUSDT', -8.65], ['COOKIEUSDT', 5.63], ['BIOUSDT', -55.21], ['HYPEUSDT', 2.95], ['SOPHUSDT', 29.69], ['AUSDT', 7.58], ['HUMAUSDT', -38.25]]

y = ['LTCUSDT', 'QTUMUSDT', 'ADAUSDT', 'XRPUSDT', 'EOSUSDT', 'XLMUSDT', 'ONTUSDT', 'TRXUSDT', 'ETCUSDT', 'DASHUSDT', 'THETAUSDT', 'ATOMUSDT', 'TFUELUSDT', 'FTMUSDT', 'RVNUSDT', 'HBARUSDT', 'KAVAUSDT', 'ARPAUSDT', 'CTXCUSDT', 'BCHUSDT', 'CHRUSDT', 'MDTUSDT', 'STMXUSDT', 'KNCUSDT', 'LRCUSDT', 'ZENUSDT', 'CATIUSDT', 'CRVUSDT', 'DOTUSDT', 'RSRUSDT', 'TRBUSDT', 'EGLDUSDT', 'DIAUSDT', 'ALPHAUSDT', 'AAVEUSDT', 'NEARUSDT', 'FILUSDT', 'AXSUSDT', 'STRAXUSDT', 'UNFIUSDT', 'RIFUSDT', 'CKBUSDT', 'TWTUSDT', 'FIROUSDT', 'LITUSDT', 'SFPUSDT', 'CAKEUSDT', 'BADGERUSDT', 'FORTHUSDT', 'ICPUSDT', 'MASKUSDT', 'XVGUSDT', 'ALPACAUSDT', 'QUICKUSDT', 'MBOXUSDT', 'REQUSDT', 'GHSTUSDT', 'WAXPUSDT', 'GNOUSDT', 'XECUSDT', 'ELFUSDT', 'IDEXUSDT', 'RAREUSDT', 'LAZIOUSDT', 'DARUSDT', 'BNXUSDT', 'CITYUSDT', 'ENSUSDT', 'QIUSDT', 'CVXUSDT', 'SPELLUSDT', 'IMXUSDT', 'GLMRUSDT', 'STEEMUSDT', 'NEXOUSDT', 'OPUSDT', 'RENDERUSDT', 'LEVERUSDT', 'LUNCUSDT', 'GMXUSDT', 'BANANAUSDT', 'USTCUSDT', 'GASUSDT', 'GLMUSDT', 'PROMUSDT', 'QKCUSDT', 'ARBUSDT', 'ZKUSDT', 'WBETHUSDT', 'ARKUSDT', 'CREAMUSDT', 'REZUSDT', 'JUPUSDT', 'RONINUSDT', 'STRKUSDT', 'PDAUSDT', 'AXLUSDT', 'NULSUSDT', 'ONGUSDT', 'ZILUSDT', 'FETUSDT', 'BATUSDT', 'ZECUSDT', 'COSUSDT', 'MTLUSDT', 'DENTUSDT', 'WANUSDT', 'CHZUSDT', 'BANDUSDT', 'XTZUSDT', 'RENUSDT', 'FTTUSDT', 'LSKUSDT', 'BNTUSDT', 'MBLUSDT', 'COTIUSDT', 'STPTUSDT', 'DATAUSDT', 'SOLUSDT', 'CTSIUSDT', 'DGBUSDT', 'SXPUSDT', 'MKRUSDT', 'DCRUSDT', 'STORJUSDT', 'MANAUSDT', 'YFIUSDT', 'BALUSDT', 'BLZUSDT', 'IRISUSDT', 'KMDUSDT', 'JSTUSDT', 'FIOUSDT', 'UMAUSDT', 'BELUSDT', 'OXTUSDT', 'SUNUSDT', 'AVAXUSDT', 'ORNUSDT', 'UTKUSDT', 'AVAUSDT', 'SKLUSDT', 'PSGUSDT', '1INCHUSDT', 'OGUSDT', 'ASRUSDT', 'CELOUSDT', 'TURBOUSDT', 'SCRUSDT', 'OMUSDT', 'PONDUSDT', 'DEGOUSDT', 'CFXUSDT', 'TKOUSDT', 'PUNDIXUSDT', 'TLMUSDT', 'BARUSDT', 'ERNUSDT', 'KLAYUSDT', 'MLNUSDT', 'DEXEUSDT', 'CLVUSDT', 'QNTUSDT', 'FLOWUSDT', 'MINAUSDT', 'VIDTUSDT', 'GALAUSDT', 'SYSUSDT', 'DFUSDT', 'AGLDUSDT', 'PORTOUSDT', 'POWRUSDT', 'JASMYUSDT', 'PYRUSDT', 'SANTOSUSDT', 'BTTCUSDT', 'XNOUSDT', 'ALPINEUSDT', 'TUSDT', 'ASTRUSDT', 'KDAUSDT', 'APEUSDT', 'BIFIUSDT', 'OSMOUSDT', 'GUSDT', 'PROSUSDT', 'SSVUSDT', 'WBTCUSDT', 'EDUUSDT', 'AERGOUSDT', 'IOUSDT', 'SNTUSDT', 'MAVUSDT', 'PENDLEUSDT', 'NOTUSDT', 'VICUSDT', 'BLURUSDT', 'OMNIUSDT', '1000SATSUSDT', 'AIUSDT', 'METISUSDT', 'AEVOUSDT', 'ETHFIUSDT', 'ENAUSDT', 'PROMUSDT', 'COOKIEUSDT', 'HYPEUSDT', 'SOPHUSDT', 'AUSDT']

