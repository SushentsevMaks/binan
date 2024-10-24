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

five = ['CRVUSDT', 'SANDUSDT', 'NMRUSDT', 'DOTUSDT', 'LUNAUSDT', 'RSRUSDT', 'TRBUSDT', 'SUSHIUSDT', 'KSMUSDT', 'EGLDUSDT', 'DIAUSDT', 'RUNEUSDT']

fivedop = ['FIOUSDT', 'UMAUSDT', 'BELUSDT', 'WINGUSDT', 'UNIUSDT', 'OXTUSDT', 'SUNUSDT', 'AVAXUSDT', 'FLMUSDT', 'ORNUSDT', 'UTKUSDT', 'XVSUSDT']

six = ['ALPHAUSDT', 'AAVEUSDT', 'NEARUSDT', 'FILUSDT', 'INJUSDT', 'AUDIOUSDT', 'CTKUSDT', 'AKROUSDT', 'AXSUSDT', 'HARDUSDT', 'STRAXUSDT', 'UNFIUSDT']

sixdop = ['ROSEUSDT', 'AVAUSDT', 'SKLUSDT', 'GRTUSDT', 'JUVUSDT', 'PSGUSDT', '1INCHUSDT', 'OGUSDT', 'ATMUSDT', 'ASRUSDT', 'CELOUSDT']

seven = ['RIFUSDT', 'TRUUSDT', 'CKBUSDT', 'TWTUSDT', 'FIROUSDT', 'LITUSDT', 'SFPUSDT', 'DODOUSDT', 'CAKEUSDT', 'ACMUSDT', 'BADGERUSDT', 'FISUSDT']

sevendop = ['OMUSDT', 'PONDUSDT', 'DEGOUSDT', 'ALICEUSDT', 'LINAUSDT', 'PERPUSDT', 'SUPERUSDT', 'CFXUSDT', 'TKOUSDT', 'PUNDIXUSDT', 'TLMUSDT', 'BARUSDT']

eight = ['FORTHUSDT', 'BAKEUSDT', 'BURGERUSDT', 'SLPUSDT', 'SHIBUSDT', 'ICPUSDT', 'ARUSDT', 'MASKUSDT', 'LPTUSDT', 'XVGUSDT', 'ATAUSDT', 'GTCUSDT']

eightdop = ['ERNUSDT', 'KLAYUSDT', 'PHAUSDT', 'MLNUSDT', 'DEXEUSDT', 'C98USDT', 'CLVUSDT', 'QNTUSDT', 'FLOWUSDT', 'MINAUSDT', 'RAYUSDT', 'FARMUSDT']

nine = ['ALPACAUSDT', 'QUICKUSDT', 'MBOXUSDT', 'REQUSDT', 'GHSTUSDT', 'WAXPUSDT', 'GNOUSDT', 'XECUSDT', 'ELFUSDT', 'DYDXUSDT', 'IDEXUSDT']

ninedop = ['VIDTUSDT', 'GALAUSDT', "CATIUSDT", 'ILVUSDT', 'YGGUSDT', 'SYSUSDT', 'DFUSDT', 'FIDAUSDT', 'AGLDUSDT', 'RADUSDT', 'BETAUSDT']

ten = ['RAREUSDT', 'LAZIOUSDT', 'CHESSUSDT', 'ADXUSDT', 'AUCTIONUSDT', 'DARUSDT', 'BNXUSDT', 'MOVRUSDT', 'CITYUSDT', 'ENSUSDT', 'KP3RUSDT', 'QIUSDT']

tendop = ['PORTOUSDT', 'POWRUSDT', 'JASMYUSDT', 'AMPUSDT', 'PYRUSDT', 'ALCXUSDT', 'SANTOSUSDT', 'BICOUSDT', 'FLUXUSDT', 'FXSUSDT', 'VOXELUSDT']

eleven = ['HIGHUSDT', 'CVXUSDT', 'PEOPLEUSDT', 'OOKIUSDT', 'SPELLUSDT', 'JOEUSDT', "DOGSUSDT", 'ACHUSDT', 'IMXUSDT', 'GLMRUSDT', 'LOKAUSDT', 'SCRTUSDT', 'API3USDT']

elevendop = ['BTTCUSDT', 'ACAUSDT', 'XNOUSDT', 'WOOUSDT', 'ALPINEUSDT', 'TUSDT', 'ASTRUSDT', 'GMTUSDT', 'KDAUSDT', 'APEUSDT', 'BSWUSDT', 'BIFIUSDT', 'TONUSDT']

twelve = ['STEEMUSDT', 'NEXOUSDT', 'REIUSDT', 'LDOUSDT', 'OPUSDT', 'RENDERUSDT', 'LEVERUSDT', 'STGUSDT', 'LUNCUSDT', 'GMXUSDT', 'POLYXUSDT', 'APTUSDT', 'BANANAUSDT']

twelvedop = ['OSMOUSDT', 'HFTUSDT', 'PHBUSDT', 'HOOKUSDT', 'MAGICUSDT', 'HIFIUSDT', 'GUSDT', 'RPLUSDT', 'PROSUSDT', 'GNSUSDT', 'SYNUSDT', 'VIBUSDT', 'SSVUSDT', 'ZROUSDT']

thirteenth = ['LQTYUSDT', 'AMBUSDT', 'USTCUSDT', 'GASUSDT', 'GLMUSDT', 'PROMUSDT', 'LISTAUSDT', 'QKCUSDT', 'UFTUSDT', 'IDUSDT', 'ARBUSDT', 'OAXUSDT', 'ZKUSDT']

thirteenthdop = ['RDNTUSDT', 'WBTCUSDT', 'EDUUSDT', 'SUIUSDT', 'AERGOUSDT', 'PEPEUSDT', 'IOUSDT', 'FLOKIUSDT', 'ASTUSDT', 'SNTUSDT', 'COMBOUSDT', 'MAVUSDT', 'PENDLEUSDT', 'NOTUSDT']

fourteenth = ['ARKMUSDT', 'WBETHUSDT', 'WLDUSDT', 'SEIUSDT', 'CYBERUSDT', 'ARKUSDT', 'BBUSDT', 'CREAMUSDT', 'GFTUSDT', 'IQUSDT', 'NTRNUSDT', 'TIAUSDT', 'MEMEUSDT', 'REZUSDT']

fourteenthdop = ['ORDIUSDT', 'BEAMXUSDT', 'PIVXUSDT', 'VICUSDT', 'BLURUSDT', 'VANRYUSDT', 'OMNIUSDT', 'JTOUSDT', '1000SATSUSDT', 'BONKUSDT', 'ACEUSDT', 'NFPUSDT', 'AIUSDT', 'TAOUSDT']

fifteenth = ['XAIUSDT', 'MANTAUSDT', 'ALTUSDT', 'JUPUSDT', 'PYTHUSDT', 'RONINUSDT', 'SAGAUSDT', 'DYMUSDT', 'PIXELUSDT', 'STRKUSDT', 'PORTALUSDT', 'PDAUSDT', 'AXLUSDT', 'TNSRUSDT']

fifteenthdop = ['WIFUSDT', 'METISUSDT', 'AEVOUSDT', 'BOMEUSDT', 'ETHFIUSDT', 'ENAUSDT', 'WUSDT', "HMSTRUSDT"]

izg = []

all_cripts_workss = one + two + three + four + five + six + seven + eight + nine + ten + eleven + twelve + thirteenth + fourteenth + fifteenth + izg + \
    onedop + twodop + threedop + fourdop + fivedop + sixdop + sevendop + eightdop + ninedop + tendop + elevendop + twelvedop + \
    thirteenthdop + fourteenthdop + fifteenthdop

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

                data_token: Dataset = last_data(name_cript_check, "4h", "17280")
                volume_per_5h: float = sum([int(i * data_token.high_price[-1]) for i in data_token.volume[-6:]]) / len(data_token.volume[-6:]) / 80
                res: float = round(data_token.close_price[-1] / data_token.open_price[-1] * 100 - 100, 2)
                res_2: float = round(data_token.close_price[-2] / data_token.open_price[-2] * 100 - 100, 2)
                res_3: float = round(data_token.close_price[-3] / data_token.open_price[-3] * 100 - 100, 2)
                res_4: float = round(data_token.close_price[-4] / data_token.open_price[-4] * 100 - 100, 2)
                res_5: float = round(data_token.close_price[-5] / data_token.open_price[-5] * 100 - 100, 2)
                res_before: float = round(data_token.close_price[-1] / data_token.low_price[-1] * 100 - 100, 2)
                price_change_percent_24h: float = round(((data_token.close_price[-1] / data_token.open_price[-6]) * 100) - 100, 2)
                price_change_percent_7d: float = round(((max(data_token.high_price) / data_token.close_price[-1]) * 100) - 100, 2)

                '''процент падения за последние 2ч. Отрицательные значение == был рост'''
                loss_price_for_two_hours: float = round(100 - data_token.close_price[-2] / max([i for i in data_token.open_price[-9:]]) * 100, 2)

                if ((-4.1 > res > -20)
                        or (res < -2 and res_2 < -0.8 and res_3 < -0.8 and res_4 < -0.8 and res_5 < -0.8 and res + res_2 + res_3 + res_4 + res_5 < -10))\
                        or (res < -2 and res_2 < -0.8 and res_3 < -0.8 and res_4 < -0.8 and res + res_2 + res_3 + res_4 < -9)\
                        or (res < -2 and res_2 < -0.8 and res_3 < -0.8 and res + res_2 + res_3 < -8)\
                        or (res < -2 and res_2 < -2 and res + res_2 < -6):

                    if res < -2 and res_2 < -0.8 and res_3 < -0.8 and res_4 < -0.8 and res_5 < -0.8 and res + res_2 + res_3 + res_4 + res_5 < -10:
                        res_before: float = round(
                            data_token.close_price[-1] / min(data_token.low_price[-5:]) * 100 - 100, 2)
                        if res_before == 0:
                            res_k_low = 10000
                        else:
                            res_k_low = round(abs(res + res_2 + res_3 + res_4 + res_5) / res_before * 100, 2)
                        sell_pr = 101.15

                        """Волатильность по фреймам"""
                        high_frames = list(
                            map(lambda x: round(x[1] / x[0] * 100 - 100, 2),
                                zip(data_token.open_price, data_token.high_price)))
                        awerage_high_frame = len([i for i in high_frames if i > sell_pr - 100])

                        telebot.TeleBot(telega_token).send_message(chat_id, f"RABOTAEM 4 ЧАСОВИК- {name_cript_check}\n"
                                                                            f"{time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))}\n"
                                                                            f"Рост по фреймам - {len([i for i in high_frames if i > sell_pr - 100])}\n"
                                                                            f"Объемы {int(volume_per_5h)}\n"
                                                                            f"Цена упала на {res + res_2 + res_3 + res_4 + res_5}%\n"
                                                                            f"Свечной хвостик {res_k_low}%\n"
                                                                            f"Изменение цены за сутки {price_change_percent_24h}%\n")

                        if name_cript_check not in [i['name_cript'] for i in
                                                    get_crypto()] and volume_per_5h > 7500 and res_k_low > 200:
                            equal(name_cript_check, res + res_2 + res_3 + res_4 + res_5, res_before,
                                  price_change_percent_24h,
                                  awerage_high_frame, price_change_percent_7d, res_k_low)

                    elif res < -2 and res_2 < -0.8 and res_3 < -0.8 and res_4 < -0.8 and res + res_2 + res_3 + res_4 < -9:
                        res_before: float = round(
                            data_token.close_price[-1] / min(data_token.low_price[-4:]) * 100 - 100, 2)
                        if res_before == 0:
                            res_k_low = 10000
                        else:
                            res_k_low = round(abs(res + res_2 + res_3 + res_4) / res_before * 100, 2)

                        sell_pr = 101.15

                        """Волатильность по фреймам"""
                        high_frames = list(
                            map(lambda x: round(x[1] / x[0] * 100 - 100, 2),
                                zip(data_token.open_price, data_token.high_price)))
                        awerage_high_frame = len([i for i in high_frames if i > sell_pr - 100])

                        telebot.TeleBot(telega_token).send_message(chat_id, f"RABOTAEM 4 ЧАСОВИК- {name_cript_check}\n"
                                                                            f"{time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))}\n"
                                                                            f"Рост по фреймам - {len([i for i in high_frames if i > sell_pr - 100])}\n"
                                                                            f"Объемы {int(volume_per_5h)}\n"
                                                                            f"Цена упала на {res + res_2 + res_3 + res_4}%\n"
                                                                            f"Свечной хвостик {res_k_low}%\n"
                                                                            f"Изменение цены за сутки {price_change_percent_24h}%\n")

                        if name_cript_check not in [i['name_cript'] for i in
                                                    get_crypto()] and volume_per_5h > 7500 and res_k_low > 200:
                            equal(name_cript_check, res + res_2 + res_3 + res_4, res_before, price_change_percent_24h,
                                  awerage_high_frame, price_change_percent_7d, res_k_low)

                    elif res < -2 and res_2 < -0.8 and res_3 < -0.8 and res + res_2 + res_3 < -9:
                        res_before: float = round(data_token.close_price[-1] / min(data_token.low_price[-3:]) * 100 - 100, 2)
                        if res_before == 0:
                            res_k_low = 10000
                        else:
                            res_k_low = round(abs(res + res_2 + res_3) / res_before * 100, 2)

                        sell_pr = 101.15

                        """Волатильность по фреймам"""
                        high_frames = list(
                            map(lambda x: round(x[1] / x[0] * 100 - 100, 2),
                                zip(data_token.open_price, data_token.high_price)))
                        awerage_high_frame = len([i for i in high_frames if i > sell_pr - 100])

                        telebot.TeleBot(telega_token).send_message(chat_id, f"RABOTAEM 4 ЧАСОВИК- {name_cript_check}\n"
                                                                            f"{time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))}\n"
                                                                            f"Рост по фреймам - {len([i for i in high_frames if i > sell_pr - 100])}\n"
                                                                            f"Объемы {int(volume_per_5h)}\n"
                                                                            f"Цена упала на {res + res_2 + res_3}%\n"
                                                                            f"Свечной хвостик {res_k_low}%\n"
                                                                            f"Изменение цены за сутки {price_change_percent_24h}%\n")

                        if name_cript_check not in [i['name_cript'] for i in
                                                    get_crypto()] and volume_per_5h > 7500 and res_k_low > 200:
                            equal(name_cript_check, res + res_2 + res_3, res_before, price_change_percent_24h,
                                  awerage_high_frame,
                                  price_change_percent_7d, res_k_low)

                    elif res < -2 and res_2 < -2 and res + res_2 < -6:
                        res_before: float = round(data_token.close_price[-1] / min(data_token.low_price[-2:]) * 100 - 100, 2)
                        if res_before == 0:
                            res_k_low = 10000
                        else:
                            res_k_low = round(abs(res + res_2) / res_before * 100, 2)

                        sell_pr = 101.15

                        """Волатильность по фреймам"""
                        high_frames = list(
                            map(lambda x: round(x[1] / x[0] * 100 - 100, 2),
                                zip(data_token.open_price, data_token.high_price)))
                        awerage_high_frame = len([i for i in high_frames if i > sell_pr - 100])

                        telebot.TeleBot(telega_token).send_message(chat_id, f"RABOTAEM 4 ЧАСОВИК- {name_cript_check}\n"
                                                                            f"{time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))}\n"
                                                                            f"Рост по фреймам - {len([i for i in high_frames if i > sell_pr - 100])}\n"
                                                                            f"Объемы {int(volume_per_5h)}\n"
                                                                            f"Цена упала на {res + res_2}%\n"
                                                                            f"Свечной хвостик {res_k_low}%\n"
                                                                            f"Изменение цены за сутки {price_change_percent_24h}%\n")

                        if name_cript_check not in [i['name_cript'] for i in
                                                    get_crypto()] and volume_per_5h > 7500 and res_k_low > 200:
                            equal(name_cript_check, res + res_2, res_before, price_change_percent_24h,
                                  awerage_high_frame,
                                  price_change_percent_7d, res_k_low)

                    elif -4.1 > res > -20:
                        res_before: float = round(data_token.close_price[-1] / data_token.low_price[-1] * 100 - 100, 2)
                        if res_before == 0:
                            res_k_low = 10000
                        else:
                            res_k_low = round(abs(res) / res_before * 100, 2)

                        if -4.1 > res > -10:
                            sell_pr = 101.15

                        if -10 > res > -20:
                            sell_pr = 101.5

                        """Волатильность по фреймам"""
                        high_frames = list(map(lambda x: round(x[1] / x[0] * 100 - 100, 2), zip(data_token.open_price, data_token.high_price)))
                        awerage_high_frame = len([i for i in high_frames if i > sell_pr - 100])

                        telebot.TeleBot(telega_token).send_message(chat_id, f"RABOTAEM 4 ЧАСОВИК- {name_cript_check}\n"
                                                                            f"{time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))}\n"
                                                                            f"Рост по фреймам - {len([i for i in high_frames if i > sell_pr - 100])}\n"
                                                                            f"Объемы {int(volume_per_5h)}\n"
                                                                            f"Цена упала на {res}%\n"
                                                                            f"Свечной хвостик {res_k_low}%\n"
                                                                            f"Изменение цены за сутки {price_change_percent_24h}%\n")

                        if name_cript_check not in [i['name_cript'] for i in
                                                    get_crypto()] and volume_per_5h > 7500 and res_k_low > 200:
                            equal(name_cript_check, res, res_before, price_change_percent_24h, awerage_high_frame,
                                  price_change_percent_7d, res_k_low)

                    '''Если такой крипты в базе еще нет, то добавляем в базу '''
                    if name_cript_check not in [i['name_cript'] for i in get_crypto()] and volume_per_5h > 6500 and res_k_low > 200:
                        #smotr_15_frame: Dataset = last_data(name_cript_check, "15m", "60")
                        #res_15_frame: float = round(data_token.close_price[-1] / data_token.open_price[-1] * 100 - 100, 2)
                        equal(name_cript_check, res, res_before, price_change_percent_24h, awerage_high_frame, price_change_percent_7d, res_k_low)

                    start_time_check = time.time()
                    '''Заглушка для ожидания конца таймфрейма 15 мин (58 сек не менять!)'''
                    while time.localtime(start_time_check).tm_min != 59 or time.localtime(start_time_check).tm_sec < 58:
                        start_time_check = time.time()
                        time.sleep(1)

                    bd_cript = get_crypto()
                    '''Проверка на наилучший объект и работа с ним дальше'''
                    reit_bd_cript = []

                    for j in bd_cript:
                        reit_bd_cript.append([j['name_cript'], j["res"], j["price_change_percent_24h"], j["awerage_high_frame"], j["high_close_change"], j["res_k_low"]])

                    """Алгоритм сортировки по рейтингу (падение за таймфрейм(4 часа) и изменение цены за сутки)"""
                    reit_timeframe_change = [i[0] for i in sorted(reit_bd_cript, key=lambda x: x[1])]
                    reit_day_change = [i[0] for i in sorted(reit_bd_cript, key=lambda x: x[2])]
                    reit_awerage_high_frame = [i[0] for i in sorted(reit_bd_cript, key=lambda x: -x[3])]
                    reit_change_7d = [i[0] for i in sorted(reit_bd_cript, key=lambda x: -x[4])]

                    """Формируем список крипт со значениями"""
                    itog = []
                    for i in reit_timeframe_change:
                        for j in reit_bd_cript:
                            if i == j[0]:
                                itog.append([i, reit_timeframe_change.index(i), reit_day_change.index(i), reit_awerage_high_frame.index(i), j[4], reit_change_7d.index(i), j[1]])

                    """Определяем топ крипту и оставшийся массив для доп закупа"""
                    # top = sorted(reit_bd_cript, key=lambda x: -x[4])[0][0]
                    # all_work_crypt = sorted(reit_bd_cript, key=lambda x: -x[4])
                    top = sorted([[i[0], i[1] + i[2] + i[5], i[6]] for i in itog], key=lambda x: x[1])[0][0]
                    all_work_crypt = sorted([[i[0], i[1] + i[2] + i[5], i[6]] for i in itog], key=lambda x: x[1])
                    # top = sorted([[i[0], i[1] + i[2], i[3]] for i in itog], key=lambda x: (-x[2], x[1]))[0][0]
                    # all_work_crypt = sorted([[i[0], i[1] + i[2], i[3]] for i in itog], key=lambda x: (-x[2], [1]))[1:]

                    ''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
                    '''''''''''''''''''''''''''Основная логика'''''''''''''''''''''''''''''''''''''''''''''''''''
                    ''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
                    start_time = time.time()

                    """Алгоритм закупа"""
                    if name_cript_check == top:
                        telebot.TeleBot(telega_token).send_message(chat_id, f"ВЫБОР ПАЛ НА {name_cript_check}\n"
                                                                            f"Список крипт из базы по рейтингу - {sorted(reit_bd_cript, key=lambda x: -x[3])}\n"
                                                                            f"------------------------\n"
                                                                            f"РЕЙТИНГ - {sorted([[i[0], i[1] + i[2] + i[5]] for i in itog], key=lambda x: x[1])}\n"
                                                                            f"------------------------\n"
                                                                            f"Количество триггеров - {len(bd_cript)}\n")

                        buy_qty = round(20 / data_token.close_price[-1], 1)

                        try:
                            order_buy = client.create_order(symbol=name_cript_check, side='BUY', type='MARKET',
                                                                quantity=buy_qty)
                        except BinanceAPIException as e:
                            if e.message == "Filter failure: LOT_SIZE":
                                buy_qty = int(round(20 / data_token.close_price[-1], 1))
                                try:
                                    order_buy = client.create_order(symbol=name_cript_check, side='BUY', type='MARKET',
                                                                        quantity=buy_qty)
                                except:
                                    telebot.TeleBot(telega_token).send_message(chat_id, f"BUY ERROR: {e.message}\n"
                                                                                            f"{name_cript_check}\n"
                                                                                            f"Количество покупаемого - {buy_qty}, Цена - {data_token.high_price[-1]}")
                                    time.sleep(1)
                                    break
                            else:
                                telebot.TeleBot(telega_token).send_message(chat_id, f"BUY ERROR: {e.message}\n"
                                                                                        f"{name_cript_check}\n"
                                                                                        f"Количество покупаемого - {buy_qty}, Цена - {data_token.high_price[-1]}")
                                time.sleep(1)
                                break

                        try:
                            buyprice = float(order_buy["fills"][0]["price"])
                            open_position = True

                        except Exception as e:
                            telebot.TeleBot(telega_token).send_message(chat_id, f"ERROR: {e}\n")
                            time.sleep(1)
                            break

                        time.sleep(5)

                        """Алгоритм продажи"""
                        while open_position:
                            last_time = time.time()
                            all_orders = pd.DataFrame(client.get_all_orders(symbol=name_cript_check), columns=["orderId", "type", "side", "price", "status"])
                            balance = client.get_asset_balance(asset=name_cript_check[:-4])
                            sell_qty = float(balance["free"])
                                # sell_qty = Decimal(sell_qty).quantize(Decimal(okr), ROUND_FLOOR)

                            if sell_qty > 0.05 and len(all_orders[all_orders.isin(["NEW"]).any(axis=1)]) == 0:
                                try:
                                    x = Decimal(str(round((buyprice / 100) * sell_pr, max([len(f'{i:.15f}'.rstrip("0").split(".")[1]) for i in data_token[0][-5:]]))))
                                    order_sell = client.order_limit_sell(symbol=name_cript_check, quantity=sell_qty, price=x)

                                except BinanceAPIException as e:
                                    telebot.TeleBot(telega_token).send_message(chat_id, f"SELL ERROR 1: {e}\n"
                                                                                        f"buyprice - {buyprice}, sell_pr - {sell_pr}\n"
                                                                                        f"Количество продаваемого - {sell_qty}, Цена - {x}\n"
                                                                                        f"Монеты в кошельке - {float(sell_qty)}, Количество открытых ордеров - {len(all_orders[all_orders.isin(['NEW']).any(axis=1)])}")
                                    time.sleep(10)

                                    try:
                                        x = round((buyprice / 100) * sell_pr, max([len(str(i).split(".")[1]) for i in data_token[0][-5:]]))
                                        order_sell = client.order_limit_sell(symbol=name_cript_check, quantity=sell_qty, price=x)
                                    except BinanceAPIException as e:
                                        telebot.TeleBot(telega_token).send_message(chat_id, f"SELL ERROR: {e}\n"
                                                                                            f"Количество продаваемого - {sell_qty}, Цена - {x}\n"
                                                                                            f"Монеты в кошельке - {float(sell_qty)}, Количество открытых ордеров - {len(all_orders[all_orders.isin(['NEW']).any(axis=1)])}")
                                        time.sleep(10)

                                        try:
                                            x = Decimal(str(round((buyprice / 100) * sell_pr, max([len(f'{i:.15f}'.rstrip("0").split(".")[1]) for i in data_token[0][-5:]]))))
                                            order_sell = client.order_limit_sell(symbol=name_cript_check, quantity=int(sell_qty), price=x)
                                        except BinanceAPIException as e:
                                            telebot.TeleBot(telega_token).send_message(chat_id, f"SELL ERROR: {e}\n"
                                                                                                f"Количество продаваемого - {int(sell_qty)}, Цена - {x}\n"
                                                                                                f"Монеты в кошельке - {float(sell_qty)}, Количество открытых ордеров - {len(all_orders[all_orders.isin(['NEW']).any(axis=1)])}")
                                            time.sleep(10)

                                            try:
                                                x = round((buyprice / 100) * sell_pr, max([len(str(i).split(".")[1]) for i in data_token[0][-5:]]))
                                                order_sell = client.order_limit_sell(symbol=name_cript_check, quantity=int(sell_qty), price=x)
                                            except BinanceAPIException as e:
                                                telebot.TeleBot(telega_token).send_message(chat_id, f"ВСЕ РАВНО ФЕЙЛ: {e}\n"
                                                                                                    f"Количество продаваемого - {int(sell_qty)}, Цена - {x}\n"
                                                                                                    f"Монеты в кошельке - {float(sell_qty)}, Количество открытых ордеров - {len(all_orders[all_orders.isin(['NEW']).any(axis=1)])}")
                                                time.sleep(600)

                            elif float(sell_qty) < 0.05 and len(all_orders[all_orders.isin(["NEW"]).any(axis=1)]) == 0:
                                open_position = False
                                bot = telebot.TeleBot(telega_token)
                                message = f"СДЕЛКА ЗАВЕРШЕНА - {name_cript_check}\n" \
                                          f"\n" \
                                          f"ПРИБЫЛЬ СО СДЕЛКИ: +{round(sell_pr-100, 2)}%\n" \
                                          f"\n" \
                                          f"https://www.binance.com/ru/trade/{name_cript_check[:-4]}_USDT?_from=markets&theme=dark&type=grid"
                                bot.send_message(chat_id, message)

                            if last_time - start_time > 53400:
                                # if buyprice * 0.90 > data_token.close_price[-1]:
                                #     telebot.TeleBot(telega_token).send_message(chat_id,
                                #                                                f"ОБВАЛ!!!!!!!!!!!! ------>>>>> {name_cript_check}")
                                #     break
                                # else:

                                orders = client.get_open_orders(symbol=name_cript_check)
                                for order in orders:
                                    ordId = order["orderId"]
                                    client.cancel_order(symbol=name_cript_check, orderId=ordId)

                                time.sleep(1)
                                try:
                                    balance = client.get_asset_balance(asset=name_cript_check[:-4])
                                    sell_qty = float(balance["free"])
                                    order_sell = client.order_market_sell(symbol=name_cript_check, quantity=sell_qty)
                                    orders = client.get_all_orders(symbol=name_cript_check, limit=1)
                                    price = round(float(orders[0]['cummulativeQuoteQty']) / float(orders[0]["origQty"]),7)
                                    telebot.TeleBot(telega_token).send_photo(chat_id, 'https://github.com/bibar228/hhru-analize/blob/main/patrik_35715679_orig_.jpg?raw=true', caption=
                                                                                        f"ВРЕМЯ ИСТЕКЛО - {name_cript_check}\n"
                                                                                        f"Продажа по времени {price}\n"
                                                                                        f"Покупал за {buyprice}\n"
                                                                                        f"Разница {round(100 - 100 * (buyprice / price), 2)}%")
                                    open_position = False

                                except Exception as e:
                                    telebot.TeleBot(telega_token).send_message(chat_id,f"Ошибка продажи в минус, Нужен хелп!\n"
                                                                                       f"{e}\n"
                                                                                       f"sell_qty {sell_qty}\n"
                                                                                       f"balance {balance}")
                                    time.sleep(500)


                            data_token: Dataset = last_data(name_cript_check, "15m", "1440")
                            time.sleep(4)

                        max_price = max(data_token[0])

                        time.sleep(1)
                        try:
                            sql_req_str2(name_cript_check, price_change_percent_24h, volume_per_5h, max_price, loss_price_for_two_hours, res)
                        except:
                            time.sleep(5)
                            sql_req_str2(name_cript_check, price_change_percent_24h, volume_per_5h, max_price, loss_price_for_two_hours, res)

                        new_alg_crypto_work_end = []
                        """Заглушка до 25 минут, если первая продажа была быстрее"""
                        while last_time - start_time < 1200:
                            last_time = time.time()
                            time.sleep(1)


                        """АЛГОРИТМ ДОП ЗАКУПА ПОСЛЕ ОСНОВНОГО"""
                        if len(all_work_crypt) > 1:

                            telebot.TeleBot(telega_token).send_message(chat_id,f"Заглушку прошел, включаю доп алг")

                            while last_time - start_time < 12000:
                                sell_pr = 101.15

                                for i in all_work_crypt[1:round(len(all_work_crypt))]:

                                    last_time = time.time()
                                    data_token: Dataset = last_data(i[0], "4h", "1440")
                                    volume_per_5h: float = sum([int(i * data_token.high_price[-1]) for i in data_token.volume[:-1]]) / len(data_token.volume[:-1]) / 80
                                    res_now: float = round(data_token.close_price[-1] / data_token.open_price[-1] * 100 - 100, 2)
                                    res_past: float = round(data_token.high_price[-1] / data_token.close_price[-2] * 100 - 100, 2)
                                    price_change_percent_24h: float = round(((data_token.close_price[-1] / data_token.open_price[0]) * 100) - 100, 2)
                                    '''процент падения за последние 2ч. Отрицательные значение == был рост'''
                                    loss_price_for_two_hours: float = round(100 - data_token.close_price[-2] / max([i for i in data_token.open_price[-9:]]) * 100, 2)

                                    """ЗАКУПАЕМ С УСЛОВИЯМИ"""
                                    if res_now < 0 and res_past < 0.6 and last_time - start_time < 12000 and i[0] not in new_alg_crypto_work_end:
                                        start_time_dop_alg = time.time()

                                        buy_qty = round(20 / data_token.close_price[-1], 1)
                                        telebot.TeleBot(telega_token).send_message(chat_id, f"!!!!!!!!!!!!!ДОП АЛГОРИТМ!!!!!!!!!!!!!\n"
                                                                                            f"РАБОТАЕМ С {i[0]}\n"
                                                                                            f"Изменение цены сейчас относительно начала фрейма: {res_now}%\n"
                                                                                            f"Максимальный рост цены в этот фрейм: {res_past}%\n")
                                        new_alg_crypto_work_end.append(i[0])

                                        try:
                                            order_buy = client.create_order(symbol=i[0], side='BUY', type='MARKET', quantity=buy_qty)
                                        except BinanceAPIException as e:
                                            if e.message == "Filter failure: LOT_SIZE":
                                                buy_qty = int(round(20 / data_token.close_price[-1], 1))
                                                try:
                                                    order_buy = client.create_order(symbol=i[0], side='BUY', type='MARKET', quantity=buy_qty)
                                                except:
                                                    telebot.TeleBot(telega_token).send_message(chat_id,
                                                                                               f"BUY ERROR: {e.message}\n"
                                                                                               f"{i[0]}\n"
                                                                                               f"Количество покупаемого - {buy_qty}, Цена - {data_token.high_price[-1]}")
                                                    time.sleep(1)
                                                    break
                                            else:
                                                telebot.TeleBot(telega_token).send_message(chat_id,
                                                                                           f"BUY ERROR: {e.message}\n"
                                                                                           f"{i[0]}\n"
                                                                                           f"Количество покупаемого - {buy_qty}, Цена - {data_token.high_price[-1]}")
                                                time.sleep(1)
                                                break

                                        try:
                                            buyprice = float(order_buy["fills"][0]["price"])
                                            open_position = True

                                        except Exception as e:
                                            telebot.TeleBot(telega_token).send_message(chat_id, f"ERROR: {e}\n")
                                            time.sleep(1)
                                            break

                                        time.sleep(5)

                                        """Алгоритм продажи"""
                                        while open_position:
                                            last_time_dop_alg = time.time()
                                            all_orders = pd.DataFrame(client.get_all_orders(symbol=i[0]), columns=["orderId", "type", "side", "price", "status"])
                                            balance = client.get_asset_balance(asset=i[0][:-4])
                                            sell_qty = float(balance["free"])
                                            # sell_qty = Decimal(sell_qty).quantize(Decimal(okr), ROUND_FLOOR)

                                            if sell_qty > 0.05 and len(all_orders[all_orders.isin(["NEW"]).any(axis=1)]) == 0:
                                                try:
                                                    y = Decimal(str(round((buyprice / 100) * sell_pr, max([len(f'{i:.15f}'.rstrip("0").split(".")[1]) for i in data_token[0][-5:]]))))
                                                    order_sell = client.order_limit_sell(symbol=i[0],
                                                                                         quantity=sell_qty,
                                                                                         price=y)

                                                except BinanceAPIException as e:
                                                    telebot.TeleBot(telega_token).send_message(chat_id,
                                                                                               f"ERROR 1 {e}\n"
                                                                                               f"buyprice - {buyprice}, sell_pr - {sell_pr}\n"
                                                                                               f"Количество продаваемого - {sell_qty}, Цена - {y}\n"
                                                                                               f"Монеты в кошельке - {float(sell_qty)}, Количество открытых ордеров - {len(all_orders[all_orders.isin(['NEW']).any(axis=1)])}")
                                                    time.sleep(10)

                                                    try:
                                                        y = round((buyprice / 100) * sell_pr, max([len(str(i).split(".")[1]) for i in data_token[0][-5:]]))
                                                        order_sell = client.order_limit_sell(symbol=i[0],
                                                                                             quantity=sell_qty,
                                                                                             price=y)
                                                    except BinanceAPIException as e:
                                                        telebot.TeleBot(telega_token).send_message(chat_id,
                                                                                                   f"ERROR 2 {e}\n"
                                                                                                   f"buyprice - {buyprice}, sell_pr - {sell_pr}\n"
                                                                                                   f"Количество продаваемого - {sell_qty}, Цена - {y}\n"
                                                                                                   f"Монеты в кошельке - {float(sell_qty)}, Количество открытых ордеров - {len(all_orders[all_orders.isin(['NEW']).any(axis=1)])}")
                                                        time.sleep(10)

                                                        try:
                                                            y = Decimal(str(round((buyprice / 100) * sell_pr, max([len(f'{i:.15f}'.rstrip("0").split(".")[1]) for i in data_token[0][-5:]]))))
                                                            order_sell = client.order_limit_sell(symbol=i[0],
                                                                                                 quantity=int(sell_qty),
                                                                                                 price=y)
                                                        except BinanceAPIException as e:
                                                            telebot.TeleBot(telega_token).send_message(chat_id,
                                                                                                       f"ERROR 3 {e}\n"
                                                                                                       f"buyprice - {buyprice}, sell_pr - {sell_pr}\n"
                                                                                                       f"Количество продаваемого - {int(sell_qty)}, Цена - {y}\n"
                                                                                                       f"Монеты в кошельке - {float(sell_qty)}, Количество открытых ордеров - {len(all_orders[all_orders.isin(['NEW']).any(axis=1)])}")
                                                            time.sleep(10)

                                                            try:
                                                                y = round((buyprice / 100) * sell_pr, max([len(str(i).split(".")[1]) for i in data_token[0][-5:]]))
                                                                order_sell = client.order_limit_sell(symbol=i[0], quantity=int(sell_qty), price=y)

                                                            except BinanceAPIException as e:
                                                                telebot.TeleBot(telega_token).send_message(chat_id,
                                                                                                           f"ВСЕ РАВНО ФЕЙЛ: {e}\n"
                                                                                                           f"buyprice - {buyprice}, sell_pr - {sell_pr}\n"
                                                                                                           f"Количество продаваемого - {int(sell_qty)}, Цена - {y}\n"
                                                                                                           f"Монеты в кошельке - {float(sell_qty)}, Количество открытых ордеров - {len(all_orders[all_orders.isin(['NEW']).any(axis=1)])}")
                                                                time.sleep(600)

                                            elif float(sell_qty) < 0.05 and len(all_orders[all_orders.isin(["NEW"]).any(axis=1)]) == 0:
                                                open_position = False
                                                bot = telebot.TeleBot(telega_token)
                                                message = f"СДЕЛКА ЗАВЕРШЕНА - {i[0]}\n" \
                                                          f"\n" \
                                                          f"ПРИБЫЛЬ СО СДЕЛКИ: +{round(sell_pr - 100, 2)}%\n" \
                                                          f"\n" \
                                                          f"https://www.binance.com/ru/trade/{i[0][:-4]}_USDT?_from=markets&theme=dark&type=grid"
                                                bot.send_message(chat_id, message)

                                            if last_time_dop_alg - start_time_dop_alg > 42300:
                                                telebot.TeleBot(telega_token).send_message(chat_id,
                                                                                           f"ВРЕМЯ ИСТЕКЛО {i[0]} {buyprice} {data_token.close_price[-1]}")
                                                # if buyprice * 0.90 > data_token.close_price[-1]:
                                                #     telebot.TeleBot(telega_token).send_message(chat_id,
                                                #                                                f"ОБВАЛ!!!!!!!!!!!! ------>>>>> {i[0]}")
                                                #     break
                                                # else:
                                                telebot.TeleBot(telega_token).send_message(chat_id,
                                                                                           f"ПРОДАЕМ ПО ВРЕМЕНИ")
                                                orders = client.get_open_orders(symbol=i[0])
                                                for order in orders:
                                                    ordId = order["orderId"]
                                                    client.cancel_order(symbol=i[0], orderId=ordId)

                                                try:
                                                    balance = client.get_asset_balance(asset=i[0][:-4])
                                                    sell_qty = float(balance["free"])
                                                    order_sell = client.order_market_sell(symbol=i[0],
                                                                                          quantity=sell_qty)
                                                    orders = client.get_all_orders(symbol=i[0], limit=1)
                                                    price = round(float(orders[0]['cummulativeQuoteQty']) / float(orders[0]["origQty"]), 7)
                                                    telebot.TeleBot(telega_token).send_photo(chat_id,
                                                                                             'https://github.com/bibar228/hhru-analize/blob/main/patrik_35715679_orig_.jpg?raw=true',
                                                                                             caption=f"Продажа по времени {price}\n"
                                                                                                    f"Покупал за {buyprice}\n"
                                                                                                    f"Разница {round(100 - 100 * (buyprice / price), 2)}%")
                                                    open_position = False

                                                except Exception as e:
                                                    telebot.TeleBot(telega_token).send_message(chat_id,
                                                                                               f"Ошибка продажи в минус, Нужен хелп!\n"
                                                                                               f"{e}")
                                                    time.sleep(500)


                                            data_token: Dataset = last_data(i[0], "15m", "1440")
                                            time.sleep(4)

                                        max_price = max(data_token[0])

                                        time.sleep(1)
                                        try:
                                            sql_req_str2(i[0], price_change_percent_24h, volume_per_5h, max_price, loss_price_for_two_hours, res_now)
                                        except:
                                            time.sleep(5)
                                            sql_req_str2(i[0], price_change_percent_24h, volume_per_5h, max_price, loss_price_for_two_hours, res_now)

                                        time.sleep(1)


                        telebot.TeleBot(telega_token).send_message(chat_id,f"Доп. алг закончился, готов к новому циклу")


                    time.sleep(60)
                    sql_del()

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
    # frame.to_csv('file1.csv')
    # print(frame["Volume"].sum())
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
    # print(data)
    # print(sum(data[0][:-1])/len(data[0][:-1]))
    # print(data[0][-1])
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
    while time.localtime(start_time_check).tm_min % 15 != 14 or time.localtime(start_time_check).tm_sec < 20:
        start_time_check = time.time()
        time.sleep(1)

    '''Старт программы'''
    threads = [Thread(target=top_coin, args=([one])), Thread(target=top_coin, args=([two])),
               Thread(target=top_coin, args=([three])),
               Thread(target=top_coin, args=([four])), Thread(target=top_coin, args=([five])),
               Thread(target=top_coin, args=([six])),
               Thread(target=top_coin, args=([seven])), Thread(target=top_coin, args=([eight])),
               Thread(target=top_coin, args=([nine])),
               Thread(target=top_coin, args=([ten])), Thread(target=top_coin, args=([eleven])),
               Thread(target=top_coin, args=([twelve])),
               Thread(target=top_coin, args=([thirteenth])), Thread(target=top_coin, args=([fourteenth])),
               Thread(target=top_coin, args=([fifteenth])),
               Thread(target=top_coin, args=([onedop])), Thread(target=top_coin, args=([twodop])),
               Thread(target=top_coin, args=([threedop])),
               Thread(target=top_coin, args=([fourdop])), Thread(target=top_coin, args=([fivedop])),
               Thread(target=top_coin, args=([sixdop])),
               Thread(target=top_coin, args=([sevendop])), Thread(target=top_coin, args=([eightdop])),
               Thread(target=top_coin, args=([ninedop])),
               Thread(target=top_coin, args=([tendop])), Thread(target=top_coin, args=([elevendop])),
               Thread(target=top_coin, args=([twelvedop])),
               Thread(target=top_coin, args=([thirteenthdop])), Thread(target=top_coin, args=([fourteenthdop])),
               Thread(target=top_coin, args=([fifteenthdop]))]

    start_threads = [i.start() for i in threads]

    stop_threads = [i.join() for i in threads]






