import time
from decimal import Decimal
from datetime import datetime
# from decimal import Decimal, ROUND_FLOOR
from binance.client import Client
from binance.exceptions import BinanceAPIException
import keys
import pandas as pd
import telebot
from threading import Thread
from typing import NamedTuple

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

fifteenthdop = ['WIFUSDT', 'METISUSDT', 'AEVOUSDT', 'ETHFIUSDT', 'ENAUSDT', 'WUSDT', 'NEIROUSDT']

izg = []

all_cripts_workss = one + two + three + four + five + six + seven + eight + nine + ten + eleven + twelve + thirteenth + fourteenth + fifteenth + izg + \
    onedop + twodop + threedop + fourdop + fivedop + sixdop + sevendop + eightdop + ninedop + tendop + elevendop + twelvedop + \
    thirteenthdop + fourteenthdop + fifteenthdop

ex = {}

chat_id = -695765690

keks = {}


def top_coin(trading_pairs: list):
    for name_cript_check in trading_pairs:
        start = time.time()
        if name_cript_check not in ex or start - ex[name_cript_check] > 7200:
            try:
                # print(name_cript_check)
                # print(last_data(name_cript_check, "3m", "300"))
                data_token: Dataset = last_data(name_cript_check, "1m", "1440")
                price_change_in_9min = round((data_token.high_price[-1] / data_token.high_price[-9]) * 100 - 100, 2)
                price_change_in_8min = round((data_token.high_price[-1] / data_token.high_price[-8]) * 100 - 100, 2)
                price_change_in_7min = round((data_token.high_price[-1] / data_token.high_price[-7]) * 100 - 100, 2)
                price_change_in_6min = round((data_token.high_price[-1] / data_token.high_price[-6]) * 100 - 100, 2)
                price_change_in_5min = round((data_token.high_price[-1] / data_token.high_price[-5]) * 100 - 100, 2)
                price_change_in_2min = round((data_token.high_price[-1] / data_token.high_price[-2]) * 100 - 100, 2)
                price_change_in_3min = round((data_token.high_price[-1] / data_token.high_price[-3]) * 100 - 100, 2)
                price_change_in_4min = round((data_token.high_price[-1] / data_token.high_price[-4]) * 100 - 100, 2)
                price_change_percent_24h = round(((data_token.close_price[-15] / data_token.close_price[0]) * 100) - 100, 2)
                price_change_percent_min_24h = round(((data_token.high_price[-1] / min([i for i in data_token.high_price])) * 100) - 100, 2)
                price_change_percent_max_24h = round(((data_token.high_price[-1] / max([i for i in data_token.high_price])) * 100) - 100, 2)
                volume_per_5h = sum([int(i * data_token.high_price[-1]) for i in data_token.volume[1140:-25]]) / len(data_token.volume[1140:-25])
                volatility_date = list(map(lambda x: x[0] / x[1] * 100 - 100, zip(data_token.high_price, data_token.low_price)))
                volatility = round(sum(volatility_date) / len(volatility_date), 2)
                # print(name_cript_check)
                now = datetime.now()
                frame = now.strftime("%H:%M:%S")

                if ((price_change_in_3min > 3 or price_change_in_2min > 3)
                        and data_token.high_price[-3:] == sorted(data_token.high_price[-3:])
                        and (name_cript_check not in keks or start-keks[name_cript_check] > 2000)):


                    telebot.TeleBot(telega_token).send_message(chat_id, f"ОБЪЕМЫ МЕНЬШЕ 250 - {name_cript_check}\n"
                                                                        f"Цены {data_token.high_price[-8:]}\n"
                                                                        f"Объемы {int(volume_per_5h)}\n"
                                                                        f"Изменение цены за 6 мин {round(price_change_in_6min, 2)}%  {round(price_change_in_6min - price_change_in_5min, 2)}%\n"
                                                                        f"Изменение цены за 5 мин {round(price_change_in_5min, 2)}%  {round(price_change_in_5min - price_change_in_4min, 2)}%\n"
                                                                        f"Изменение цены за 4 мин {round(price_change_in_4min, 2)}%  {round(price_change_in_4min - price_change_in_3min, 2)}%\n"
                                                                        f"Изменение цены за 3 мин {round(price_change_in_3min, 2)}%  {round(price_change_in_3min - price_change_in_2min, 2)}%\n"
                                                                        f"Изменение цены за 2 мин {round(price_change_in_2min, 2)}%\n"
                                                                        f"Изменение цены за 24ч  {round(price_change_percent_24h, 2)}%\n"
                                                                        f"Средняя волатильность за 10ч  {volatility}%\n"
                                                                        f"Изменение цены от минимальной за 24ч  {round(price_change_percent_min_24h, 2)}%\n"
                                                                        f"Изменение цены от максимальной за 24ч  {round(price_change_percent_max_24h, 2)}%\n"
                                                                        f"Время засечки  {frame}%\n")
                    keks[name_cript_check] = time.time()
                # and price_change_in_5min < 10 \
                # and price_change_percent_min_24h < 20 \
                # and price_change_percent_max_24h < 20
                if ((4.5 > price_change_in_2min > 2.4 and 4.5 > price_change_in_3min - price_change_in_2min > 0.85
                     and price_change_in_4min - price_change_in_3min > -0.25
                     and price_change_in_4min - price_change_in_3min != 0
                     and price_change_in_5min - price_change_in_4min > -0.3
                     and price_change_in_6min - price_change_in_5min > -0.9)
                    or (4.5 > price_change_in_2min > 0.85 and 4.5 > price_change_in_3min - price_change_in_2min > 2.3
                        and price_change_in_4min - price_change_in_3min > -0.25
                        and price_change_in_4min - price_change_in_3min != 0
                        and price_change_in_5min - price_change_in_4min > -0.3
                        and price_change_in_6min - price_change_in_5min > -0.9)
                    or (4.5 > price_change_in_2min > 1.25 and 4.5 > price_change_in_3min - price_change_in_2min > 1.25
                        and price_change_in_4min - price_change_in_3min > -0.25
                        and price_change_in_5min - price_change_in_4min > -0.3
                        and price_change_in_6min - price_change_in_5min > -0.9)
                    or (4.5 > price_change_in_2min > 1.5 and 4.5 > price_change_in_4min - price_change_in_3min > 1.5
                        and price_change_in_3min - price_change_in_2min > 0
                        and price_change_in_5min - price_change_in_4min > -0.3
                        and price_change_in_6min - price_change_in_5min > -0.9)) \
                    and 12 > price_change_percent_24h > -10 \
                    and volume_per_5h > 250 \
                    and price_change_percent_max_24h >= 0:


                    telebot.TeleBot(telega_token).send_message(chat_id, f"RABOTAEM - {name_cript_check}\n"
                                                                        f"Цены {data_token.high_price[-9:]}\n"
                                                                        f"Объемы {int(volume_per_5h)}\n"
                                                                        f"Изменение цены за 9 мин {round(price_change_in_9min, 2)}%  {round(price_change_in_9min - price_change_in_8min, 2)}%\n"
                                                                        f"Изменение цены за 8 мин {round(price_change_in_8min, 2)}%  {round(price_change_in_8min - price_change_in_7min, 2)}%\n"
                                                                        f"Изменение цены за 7 мин {round(price_change_in_7min, 2)}%  {round(price_change_in_7min - price_change_in_6min, 2)}%\n"
                                                                        f"Изменение цены за 6 мин {round(price_change_in_6min, 2)}%  {round(price_change_in_6min - price_change_in_5min, 2)}%\n"
                                                                        f"Изменение цены за 5 мин {round(price_change_in_5min, 2)}%  {round(price_change_in_5min - price_change_in_4min, 2)}%\n"
                                                                        f"Изменение цены за 4 мин {round(price_change_in_4min, 2)}%  {round(price_change_in_4min - price_change_in_3min, 2)}%\n"
                                                                        f"Изменение цены за 3 мин {round(price_change_in_3min, 2)}%  {round(price_change_in_3min - price_change_in_2min, 2)}%\n"
                                                                        f"Изменение цены за 2 мин {round(price_change_in_2min, 2)}%\n"
                                                                        f"Изменение цены за 24ч  {round(price_change_percent_24h, 2)}%\n"
                                                                        f"Средняя волатильность за 10ч  {volatility}%\n"
                                                                        f"Изменение цены от минимальной за 24ч  {round(price_change_percent_min_24h, 2)}%\n"
                                                                        f"Изменение цены от максимальной за 24ч  {round(price_change_percent_max_24h, 2)}%\n"
                                                                        f"Время покупки {frame}\n")
                    time.sleep(5)
                    ex[name_cript_check] = time.time()
            except:
                pass


class Dataset(NamedTuple):
    high_price: list
    volume: list
    close_price: list
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
                   close_price=[i.Close for i in frame.itertuples()], low_price=[i.Low for i in frame.itertuples()])


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


# def get_recommend(i):
#     interval = Interval.INTERVAL_1_MINUTE
#     output = TA_Handler(symbol=i, screener="Crypto", exchange="Binance", interval=interval)
#
#     activiti = output.get_analysis().summary
#     return activiti


while True:
    start_time_check = time.time()
    '''Заглушка для ожидания конца таймфрейма 15 мин'''

    bib = [[all_cripts_workss[i]] for i in range(0, len(all_cripts_workss))]

    '''Старт программы'''
    threads = [Thread(target=top_coin, args=([i])) for i in bib]

    start_threads = [i.start() for i in threads]

    stop_threads = [i.join() for i in threads]

    time.sleep(70)