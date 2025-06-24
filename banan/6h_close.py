import time
from decimal import Decimal
from datetime import datetime
from binance.client import Client
from binance.exceptions import BinanceAPIException
import keys
import pandas as pd
import telebot
from sql_request import equal, sql_del, get_crypto
from threading import Thread
from typing import NamedTuple
from tradingview_ta import TA_Handler, Interval, Exchange

telega_token = "5926919919:AAFCHFocMt_pdnlAgDo-13wLe4h_tHO0-GE"

client = Client(keys.api_key, keys.api_secret)
# futures_exchange_info = client.futures_exchange_info()
# trading_pairs = [info['symbol'] for info in futures_exchange_info['symbols'] if info['symbol'][-4:] == "USDT"]

all_cripts_workss = ['LTCUSDT', 'ADAUSDT', 'XRPUSDT', 'EOSUSDT', 'IOTAUSDT', 'XLMUSDT', 'ONTUSDT', 'TRXUSDT', 'ETCUSDT', 'ICXUSDT', 'DASHUSDT', 'ENJUSDT', 'ATOMUSDT', 'TFUELUSDT', 'ONEUSDT', 'ALGOUSDT', 'DUSKUSDT', 'ANKRUSDT', 'RVNUSDT', 'HBARUSDT', 'NKNUSDT', 'KAVAUSDT', 'ARPAUSDT', 'IOTXUSDT', 'RLCUSDT', 'CTXCUSDT', 'BCHUSDT', 'TROYUSDT', 'CHRUSDT', 'ARDRUSDT', 'STMXUSDT', 'KNCUSDT', 'LRCUSDT', 'COMPUSDT', 'SCUSDT', 'ZENUSDT', 'SNXUSDT', 'VTHOUSDT', 'CATIUSDT', 'CRVUSDT', 'SANDUSDT', 'DOTUSDT', 'LUNAUSDT', 'SUSHIUSDT', 'KSMUSDT', 'EGLDUSDT', 'RUNEUSDT', 'ALPHAUSDT', 'AAVEUSDT', 'NEARUSDT', 'INJUSDT', 'CTKUSDT', 'AXSUSDT', 'HARDUSDT', 'STRAXUSDT', 'UNFIUSDT', 'RIFUSDT', 'TWTUSDT', 'FIROUSDT', 'LITUSDT', 'SFPUSDT', 'CAKEUSDT', 'BADGERUSDT', 'BURGERUSDT', 'SLPUSDT', 'SHIBUSDT', 'ARUSDT', 'MASKUSDT', 'XVGUSDT', 'ATAUSDT', 'QUICKUSDT', 'MBOXUSDT', 'REQUSDT', 'GHSTUSDT', 'WAXPUSDT', 'GNOUSDT', 'XECUSDT', 'DYDXUSDT', 'RAREUSDT', 'LAZIOUSDT', 'ADXUSDT', 'AUCTIONUSDT', 'DARUSDT', 'BNXUSDT', 'CITYUSDT', 'ENSUSDT', 'QIUSDT', 'HIGHUSDT', 'JOEUSDT', 'ACHUSDT', 'LOKAUSDT', 'SCRTUSDT', 'API3USDT', 'STEEMUSDT', 'NEXOUSDT', 'REIUSDT', 'OPUSDT', 'STGUSDT', 'LUNCUSDT', 'GMXUSDT', 'POLYXUSDT', 'APTUSDT', 'LQTYUSDT', 'GASUSDT', 'PROMUSDT', 'LISTAUSDT', 'QKCUSDT', 'IDUSDT', 'ZKUSDT', 'WBETHUSDT', 'WLDUSDT', 'CYBERUSDT', 'HMSTRUSDT', 'IQUSDT', 'NTRNUSDT', 'MEMEUSDT', 'REZUSDT', 'ALTUSDT', 'JUPUSDT', 'PYTHUSDT', 'RONINUSDT', 'AXLUSDT', 'HMSTRUSDT', 'VETUSDT', 'LINKUSDT', 'ONGUSDT', 'HOTUSDT', 'ZILUSDT', 'ZRXUSDT', 'BATUSDT', 'ZECUSDT', 'IOSTUSDT', 'CELRUSDT', 'WINUSDT', 'COSUSDT', 'MTLUSDT', 'DENTUSDT', 'CVCUSDT', 'CHZUSDT', 'BANDUSDT', 'XTZUSDT', 'FTTUSDT', 'LSKUSDT', 'BNTUSDT', 'LTOUSDT', 'MBLUSDT', 'COTIUSDT', 'STPTUSDT', 'DATAUSDT', 'CTSIUSDT', 'DGBUSDT', 'SXPUSDT', 'MKRUSDT', 'STORJUSDT', 'MANAUSDT', 'YFIUSDT', 'BALUSDT', 'BLZUSDT', 'JSTUSDT', 'UMAUSDT', 'OXTUSDT', 'SUNUSDT', 'AVAXUSDT', 'UTKUSDT', 'ROSEUSDT', 'SKLUSDT', 'GRTUSDT', 'JUVUSDT', 'PSGUSDT', '1INCHUSDT', 'OGUSDT', 'ATMUSDT', 'ASRUSDT', 'CELOUSDT', 'TURBOUSDT', 'OMUSDT', 'PONDUSDT', 'DEGOUSDT', 'SUPERUSDT', 'CFXUSDT', 'TKOUSDT', 'PUNDIXUSDT', 'BARUSDT', 'ERNUSDT', 'PHAUSDT', 'DEXEUSDT', 'C98USDT', 'CLVUSDT', 'QNTUSDT', 'FLOWUSDT', 'MINAUSDT', 'FARMUSDT', 'VIDTUSDT', 'GALAUSDT', 'CATIUSDT', 'ILVUSDT', 'SYSUSDT', 'AGLDUSDT', 'RADUSDT', 'BETAUSDT', 'PORTOUSDT', 'POWRUSDT', 'JASMYUSDT', 'AMPUSDT', 'PYRUSDT', 'ALCXUSDT', 'SANTOSUSDT', 'FLUXUSDT', 'BTTCUSDT', 'ACAUSDT', 'XNOUSDT', 'ASTRUSDT', 'GMTUSDT', 'APEUSDT', 'BIFIUSDT', 'TONUSDT', 'OSMOUSDT', 'HFTUSDT', 'PHBUSDT', 'HOOKUSDT', 'HIFIUSDT', 'GUSDT', 'RPLUSDT', 'PROSUSDT', 'SYNUSDT', 'ZROUSDT', 'SUIUSDT', 'AERGOUSDT', 'IOUSDT', 'NOTUSDT', 'BEAMXUSDT', 'VICUSDT', 'VANRYUSDT', 'NFPUSDT', 'ENAUSDT']
chat_id = -695765690

keks = {}

def top_coin(trading_pairs: list):
    for name_cript_check in trading_pairs:
        try:
            # print(name_cript_check)
            # print(last_data(name_cript_check, "3m", "300"))
            '''6 ЧАСОВИК'''
            ''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
            ''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
            ''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
            time_frames = [4, 10, 16, 22]

            if time.localtime(time.time()).tm_min == 59 and time.localtime(time.time()).tm_hour in time_frames:

                data_token: Dataset = last_data(name_cript_check, "6h", "48000")
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


                """Определяем было падение за последние 20 дней более чем на -30%"""
                a = list(zip(data_token.close_price, data_token.open_price))
                b = min(list(map(lambda x: round(x[0] / x[1] * 100 - 100, 2), a)))

                if -4.2 > res > -20 and res_sum5 > 15 and b > -30:

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


                    telebot.TeleBot(telega_token).send_message(chat_id, f"RABOTAEM 6 ЧАСОВИК- {name_cript_check}\n"
                                                                        f"{time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))}\n"
                                                                        f"Рост по фреймам - {len([i for i in high_frames if i > sell_pr - 100])}\n"
                                                                        f"Объемы {int(volume_per_5h)}\n"
                                                                        f"Цена упала на {res}%\n"
                                                                        f"Свечной хвостик {res_k_low}%\n"
                                                                        f"Изменение цены за сутки {price_change_percent_24h}%\n")

                    if name_cript_check not in [i['name_cript'] for i in get_crypto("`vision_equals_6h`")] and volume_per_5h > 7500:
                        equal("`vision_equals_6h`", name_cript_check, res, res_before, price_change_percent_24h, awerage_high_frame,
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

    sql_del("`vision_equals_6h`")

    '''Старт программы'''
    threads = [Thread(target=top_coin, args=([i])) for i in bib]

    start_threads = [i.start() for i in threads]

    stop_threads = [i.join() for i in threads]

    time.sleep(60)




