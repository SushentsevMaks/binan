import time
from decimal import Decimal
from datetime import datetime
from binance.client import Client
from binance.exceptions import BinanceAPIException
import keys
import pandas as pd
import telebot
from sql_request import sql_req_str2, equal, sql_del, get_crypto
from threading import Thread
from typing import NamedTuple
from tradingview_ta import TA_Handler, Interval, Exchange

telega_token = "5926919919:AAFCHFocMt_pdnlAgDo-13wLe4h_tHO0-GE"

client = Client(keys.api_key, keys.api_secret)
# futures_exchange_info = client.futures_exchange_info()
# trading_pairs = [info['symbol'] for info in futures_exchange_info['symbols'] if info['symbol'][-4:] == "USDT"]

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

all_cripts_workss = ['NEOUSDT', 'LTCUSDT', 'QTUMUSDT', 'ADAUSDT', 'XRPUSDT', 'EOSUSDT', 'IOTAUSDT', 'XLMUSDT', 'ONTUSDT', 'TRXUSDT', 'ETCUSDT', 'ICXUSDT', 'DASHUSDT', 'THETAUSDT', 'ENJUSDT', 'ATOMUSDT', 'TFUELUSDT', 'ONEUSDT', 'ALGOUSDT', 'ANKRUSDT', 'RVNUSDT', 'HBARUSDT', 'NKNUSDT', 'STXUSDT', 'KAVAUSDT', 'ARPAUSDT', 'RLCUSDT', 'CTXCUSDT', 'BCHUSDT', 'TROYUSDT', 'HIVEUSDT', 'CHRUSDT', 'ARDRUSDT', 'MDTUSDT', 'STMXUSDT', 'KNCUSDT', 'LRCUSDT', 'COMPUSDT', 'SCUSDT', 'ZENUSDT', 'CATIUSDT', 'CRVUSDT', 'SANDUSDT', 'DOTUSDT', 'LUNAUSDT', 'RSRUSDT', 'TRBUSDT', 'SUSHIUSDT', 'KSMUSDT', 'EGLDUSDT', 'DIAUSDT', 'RUNEUSDT', 'ALPHAUSDT', 'AAVEUSDT', 'NEARUSDT', 'FILUSDT', 'INJUSDT', 'AUDIOUSDT', 'AKROUSDT', 'AXSUSDT', 'STRAXUSDT', 'UNFIUSDT', 'RIFUSDT', 'CKBUSDT', 'TWTUSDT', 'FIROUSDT', 'LITUSDT', 'SFPUSDT', 'DODOUSDT', 'CAKEUSDT', 'ACMUSDT', 'BADGERUSDT', 'FORTHUSDT', 'SLPUSDT', 'SHIBUSDT', 'ICPUSDT', 'MASKUSDT', 'LPTUSDT', 'XVGUSDT', 'QUICKUSDT', 'REQUSDT', 'GHSTUSDT', 'WAXPUSDT', 'GNOUSDT', 'XECUSDT', 'ELFUSDT', 'IDEXUSDT', 'RAREUSDT', 'LAZIOUSDT', 'AUCTIONUSDT', 'DARUSDT', 'BNXUSDT', 'MOVRUSDT', 'CITYUSDT', 'ENSUSDT', 'QIUSDT', 'HIGHUSDT', 'CVXUSDT', 'SPELLUSDT', 'JOEUSDT', 'IMXUSDT', 'GLMRUSDT', 'SCRTUSDT', 'API3USDT', 'STEEMUSDT', 'NEXOUSDT', 'REIUSDT', 'OPUSDT', 'RENDERUSDT', 'LEVERUSDT', 'STGUSDT', 'LUNCUSDT', 'GMXUSDT', 'POLYXUSDT', 'APTUSDT', 'BANANAUSDT', 'USTCUSDT', 'GLMUSDT', 'PROMUSDT', 'LISTAUSDT', 'QKCUSDT', 'IDUSDT', 'ARBUSDT', 'ZKUSDT', 'WBETHUSDT', 'WLDUSDT', 'SEIUSDT', 'CYBERUSDT', 'ARKUSDT', 'BBUSDT', 'CREAMUSDT', 'HMSTRUSDT', 'IQUSDT', 'REZUSDT', 'JUPUSDT', 'RONINUSDT', 'STRKUSDT', 'AXLUSDT', 'TNSRUSDT', 'NULSUSDT', 'LINKUSDT', 'ONGUSDT', 'ZILUSDT', 'ZRXUSDT', 'FETUSDT', 'BATUSDT', 'ZECUSDT', 'IOSTUSDT', 'CELRUSDT', 'WINUSDT', 'COSUSDT', 'MTLUSDT', 'DENTUSDT', 'WANUSDT', 'FUNUSDT', 'CVCUSDT', 'CHZUSDT', 'BANDUSDT', 'XTZUSDT', 'RENUSDT', 'FTTUSDT', 'LSKUSDT', 'BNTUSDT', 'MBLUSDT', 'COTIUSDT', 'STPTUSDT', 'DATAUSDT', 'SOLUSDT', 'CTSIUSDT', 'DGBUSDT', 'SXPUSDT', 'MKRUSDT', 'DCRUSDT', 'STORJUSDT', 'MANAUSDT', 'YFIUSDT', 'BALUSDT', 'BLZUSDT', 'IRISUSDT', 'KMDUSDT', 'JSTUSDT', 'FIOUSDT', 'UMAUSDT', 'BELUSDT', 'UNIUSDT', 'OXTUSDT', 'SUNUSDT', 'AVAXUSDT', 'UTKUSDT', 'ROSEUSDT', 'AVAUSDT', 'SKLUSDT', 'GRTUSDT', 'JUVUSDT', 'PSGUSDT', '1INCHUSDT', 'OGUSDT', 'ATMUSDT', 'ASRUSDT', 'CELOUSDT', 'TURBOUSDT', 'SCRUSDT', 'OMUSDT', 'PONDUSDT', 'DEGOUSDT', 'CFXUSDT', 'TKOUSDT', 'PUNDIXUSDT', 'TLMUSDT', 'BARUSDT', 'ERNUSDT', 'KLAYUSDT', 'MLNUSDT', 'DEXEUSDT', 'C98USDT', 'CLVUSDT', 'QNTUSDT', 'FLOWUSDT', 'MINAUSDT', 'FARMUSDT', 'VIDTUSDT', 'GALAUSDT', 'ILVUSDT', 'DFUSDT', 'AGLDUSDT', 'RADUSDT', 'PORTOUSDT', 'POWRUSDT', 'JASMYUSDT', 'PYRUSDT', 'SANTOSUSDT', 'BICOUSDT', 'FLUXUSDT', 'VOXELUSDT', 'BTTCUSDT', 'ACAUSDT', 'XNOUSDT', 'WOOUSDT', 'ALPINEUSDT', 'TUSDT', 'ASTRUSDT', 'GMTUSDT', 'KDAUSDT', 'BSWUSDT', 'BIFIUSDT', 'TONUSDT', 'OSMOUSDT', 'HFTUSDT', 'GUSDT', 'PROSUSDT', 'GNSUSDT', 'RDNTUSDT', 'WBTCUSDT', 'EDUUSDT', 'SUIUSDT', 'AERGOUSDT', 'IOUSDT', 'FLOKIUSDT', 'ASTUSDT', 'SNTUSDT', 'MAVUSDT', 'PENDLEUSDT', 'NOTUSDT', 'PIVXUSDT', 'VICUSDT', 'BLURUSDT', 'OMNIUSDT', '1000SATSUSDT', 'ACEUSDT', 'AIUSDT', 'TAOUSDT', 'METISUSDT', 'AEVOUSDT', 'ETHFIUSDT', 'WUSDT', 'PROMUSDT', 'HYPEUSDT', 'SOPHUSDT', 'AUSDT']


chat_id = -695765690

keks = {}

def top_coin(trading_pairs: list):
    for name_cript_check in trading_pairs:
        try:
            # print(name_cript_check)
            # print(last_data(name_cript_check, "3m", "300"))
            '''4 ЧАСОВИК'''
            ''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
            ''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
            ''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
            time_frames = [0, 4, 8, 12, 16, 20]

            if time.localtime(time.time()).tm_min == 59 and time.localtime(time.time()).tm_hour in time_frames:

                data_token: Dataset = last_data(name_cript_check, "4h", "48000")
                volume_per_5h: float = sum([int(i * data_token.high_price[-1]) for i in data_token.volume[-6:]]) / len(
                    data_token.volume[-6:]) / 80
                res: float = round(data_token.close_price[-1] / data_token.open_price[-1] * 100 - 100, 2)
                res_2: float = round(data_token.close_price[-2] / data_token.open_price[-2] * 100 - 100, 2)
                res_3: float = round(data_token.close_price[-3] / data_token.open_price[-3] * 100 - 100, 2)
                res_4: float = round(data_token.close_price[-4] / data_token.open_price[-4] * 100 - 100, 2)
                res_5: float = round(data_token.close_price[-5] / data_token.open_price[-5] * 100 - 100, 2)
                price_change_percent_24h: float = round(((data_token.close_price[-1] / data_token.open_price[-6]) * 100) - 100, 2)
                price_change_percent_7d: float = round(((max(data_token.high_price) / data_token.close_price[-1]) * 100) - 100, 2)
                res_sum5 = round(sum(list(map(lambda x: x[0] / x[1] * 100 - 100, list(zip(data_token.high_price[-5:], data_token.low_price[-5:]))))), 2)

                pattern_ravenstva_svechei = abs(res) - res_2
                try:
                    percent_raznici_svechei = abs(pattern_ravenstva_svechei) / abs(res_2) * 100
                except:
                    percent_raznici_svechei = 80

                """Определяем было падение за последние 20 дней более чем на -30%"""
                a = list(zip(data_token.close_price, data_token.open_price))
                b = min(list(map(lambda x: round(x[0] / x[1] * 100 - 100, 2), a)))

                if -4.2 > res > -20 and percent_raznici_svechei > 15 and res_sum5 > 15 and b > -30:

                    res_before: float = round(data_token.close_price[-1] / data_token.low_price[-1] * 100 - 100, 2)
                    if res_before == 0:
                        res_k_low = 10000
                    else:
                        res_k_low = round(abs(res) / res_before * 100, 2)

                    if res_sum5 > 50:
                        sell_pr = 101.5
                    elif 25 < res_sum5 < 50:
                        sell_pr = 101.15
                    else:
                        sell_pr = 100.75

                    """Волатильность по фреймам"""
                    high_frames = list(map(lambda x: round(x[1] / x[0] * 100 - 100, 2), zip(data_token.open_price, data_token.high_price)))
                    awerage_high_frame = len([i for i in high_frames if i > sell_pr - 100])

                    MA_200 = (sum(data_token.close_price) / 200)
                    data_token: Dataset = last_data(name_cript_check, "1d", "20160")
                    x = data_token.close_price
                    changes = []
                    for i in range(1, len(x)):
                        changes.append(x[i] - x[i - 1])

                    up = [max(change, 0) for change in changes]
                    down = [abs(min(change, 0)) for change in changes]

                    ema_up = sum(up) / len(up)
                    ema_down = sum(down) / len(down)

                    rs = ema_up / ema_down
                    rsi = 100 - (100 / (1 + rs))

                    # if 30 > rsi and data_token.close_price[-1] > MA_200:
                    #     print(name_cript_check, rsi, data_token.close_price[-1], MA_200)

                    telebot.TeleBot(telega_token).send_message(chat_id, f"RABOTAEM 4 ЧАСОВИК- {name_cript_check}\n"
                                                                        f"{time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))}\n"
                                                                        f"Рост по фреймам - {len([i for i in high_frames if i > sell_pr - 100])}\n"
                                                                        f"Объемы {int(volume_per_5h)}\n"
                                                                        f"Цена упала на {res}%\n"
                                                                        f"Свечной хвостик {res_k_low}%\n"
                                                                        f"Изменение цены за сутки {price_change_percent_24h}%\n"
                                                                        f"rsi = {rsi} (должна быть меньше 30)\n"
                                                                        f"data_token.close_price[-1] = {data_token.close_price[-1]} должен быть > MA_200 = {MA_200}")

                    if name_cript_check not in [i['name_cript'] for i in get_crypto()] and volume_per_5h > 7500 and res_k_low > 200:
                        equal(name_cript_check, res, res_before, price_change_percent_24h, awerage_high_frame,
                              sell_pr, res_sum5)
        except:
            pass


class Dataset(NamedTuple):
    high_price: list
    volume: list
    close_price: list
    open_price: list
    low_price: list


def last_data(symbol: str, interval: str, lookback: str) -> Dataset:
    frame = pd.DataFrame(client.get_historical_klines(symbol, interval, lookback + 'min ago UTC'))
    frame = frame.iloc[:, :6]
    frame.columns = ['Time', 'Open', 'High', 'Low', 'Close', 'Volume']
    frame = frame.set_index('Time')
    frame.index = pd.to_datetime(frame.index, unit='ms')
    frame = frame.astype(float)

    return Dataset(high_price=[i.High for i in frame.itertuples()], volume=[i.Volume for i in frame.itertuples()],
                   close_price=[i.Close for i in frame.itertuples()], open_price=[i.Open for i in frame.itertuples()],
                   low_price=[i.Low for i in frame.itertuples()])


def btc_anal(data: last_data) -> bool:
    price_change_percent_5min = round(((data[0][-1] / data[0][0]) * 100) - 100, 2)
    if price_change_percent_5min > 2:
        bot = telebot.TeleBot(telega_token)
        message = f"БИТОК РАСТЕТ НА {price_change_percent_5min}%"
        bot.send_message(chat_id, message)
        return False
    elif price_change_percent_5min < -2:
        bot = telebot.TeleBot(telega_token)
        message = f"БИТОК ПАДАЕТ НА {abs(price_change_percent_5min)}%"
        bot.send_message(chat_id, message)
        return False

    return True


def get_recommend(i, interval):
    handler = TA_Handler(
        symbol=i,
        exchange="binance",
        screener="crypto",
        interval=interval,
        timeout=None
    )

    return handler.get_analysis().summary


while True:
    start_time_check = time.time()
    '''Заглушка для ожидания конца таймфрейма 15 мин'''

    bib = [[all_cripts_workss[i]] for i in range(0, len(all_cripts_workss))]

    while time.localtime(start_time_check).tm_min != 59 or time.localtime(start_time_check).tm_sec < 30:
        start_time_check = time.time()
        time.sleep(1)

    sql_del()

    '''Старт программы'''
    threads = [Thread(target=top_coin, args=([i])) for i in bib]

    start_threads = [i.start() for i in threads]

    stop_threads = [i.join() for i in threads]

    time.sleep(60)







