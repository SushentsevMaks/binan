import time
from datetime import datetime
from decimal import Decimal, ROUND_FLOOR
from threading import Thread

import pymysql
import requests
from binance.client import Client, AsyncClient
from binance.exceptions import BinanceAPIException
from historical_binance import BinanceDataDownloader, BinanceDataProvider

import keys
import pandas as pd
import telebot
from tradingview_ta import TA_Handler, Interval, Exchange

import re

from binan.banan.sql_request import get_crypto, equal, sql_del

telega_token = "5926919919:AAFCHFocMt_pdnlAgDo-13wLe4h_tHO0-GE"
import asyncio

client = Client(keys.api_key, keys.api_secret)

one = ['NEOUSDT', 'LTCUSDT', 'QTUMUSDT', 'ADAUSDT', 'XRPUSDT', 'EOSUSDT', 'IOTAUSDT', 'XLMUSDT', 'ONTUSDT', 'TRXUSDT', 'ETCUSDT', 'ICXUSDT']

onedop = ['HMSTRUSDT', 'NULSUSDT', 'VETUSDT', 'LINKUSDT', 'ONGUSDT', 'HOTUSDT', 'ZILUSDT', 'ZRXUSDT', 'FETUSDT', 'BATUSDT', 'ZECUSDT', 'IOSTUSDT', 'CELRUSDT']

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

ninedop = ['VIDTUSDT', 'GALAUSDT', "CATIUSDT", 'ILVUSDT', 'YGGUSDT', 'SYSUSDT', 'DFUSDT', 'FIDAUSDT', 'AGLDUSDT', 'RADUSDT', 'BETAUSDT']

ten = ['RAREUSDT', 'LAZIOUSDT', 'CHESSUSDT', 'ADXUSDT', 'AUCTIONUSDT', 'DARUSDT', 'BNXUSDT', 'MOVRUSDT', 'CITYUSDT', 'ENSUSDT', 'KP3RUSDT', 'QIUSDT']

tendop = ['PORTOUSDT', 'POWRUSDT', 'JASMYUSDT', 'AMPUSDT', 'PYRUSDT', 'ALCXUSDT', 'SANTOSUSDT', 'BICOUSDT', 'FLUXUSDT', 'FXSUSDT', 'VOXELUSDT']

eleven = ['HIGHUSDT', 'CVXUSDT', 'PEOPLEUSDT', 'OOKIUSDT', 'SPELLUSDT', 'JOEUSDT', "DOGSUSDT", 'ACHUSDT', 'IMXUSDT', 'GLMRUSDT', 'LOKAUSDT', 'SCRTUSDT', 'API3USDT']

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

# for i in trading_pairs:
#     if i == "WANUSDT":
#         print("yes")
# futures_exchange_info = client.get_exchange_info()
# trading_pairs2 = [info['symbol'] for info in futures_exchange_info['symbols'] if info['symbol'][-4:] == "USDT"]
from typing import NamedTuple


class Dataset(NamedTuple):
    high_price: list
    volume: list
    close_price: list
    open_price: list
    low_price: list


def last_data(symbol, interval, lookback):
    frame = pd.DataFrame(client.get_historical_klines(symbol, interval, lookback + 'min ago UTC'))
    frame = frame.iloc[:, :6]
    frame.columns = ['Time', 'Open', 'High', 'Low', 'Close', 'Volume']
    frame = frame.set_index('Time')
    frame.index = pd.to_datetime(frame.index, unit='ms')
    frame = frame.astype(float)
    # frame.to_csv('file1.csv')
    # print(frame["Volume"].sum())
    return Dataset(high_price=[i.High for i in frame.itertuples()], volume=[i.Volume for i in frame.itertuples()],
                   close_price=[i.Close for i in
                                frame.itertuples()], open_price=[i.Open for i in
                                                                 frame.itertuples()], low_price=[i.Low for i in
                                                                                                 frame.itertuples()])


chat_id = -695765690

# one = ['1INCHUSDT', 'AAVEUSDT', 'ACAUSDT', 'ACHUSDT', 'ACMUSDT', 'ADAUSDT', 'ADXUSDT', 'AERGOUSDT', 'AGIXUSDT', 'AGLDUSDT', 'AKROUSDT', 'ALCXUSDT', 'ALGOUSDT', 'ALICEUSDT', 'ALPACAUSDT', 'ALPHAUSDT', 'ALPINEUSDT', 'AMBUSDT', 'AMPUSDT', 'ANKRUSDT', 'ANTUSDT', 'APEUSDT', 'API3USDT', 'APTUSDT', 'ARBUSDT', 'ARDRUSDT', 'ARKMUSDT', 'ARPAUSDT', 'ARUSDT', 'ASRUSDT', 'ASTRUSDT', 'ASTUSDT', 'ATAUSDT', 'ATMUSDT', 'ATOMUSDT', 'AUCTIONUSDT', 'AUDIOUSDT', 'AVAUSDT', 'AVAXUSDT', 'AXSUSDT', 'BADGERUSDT', 'BAKEUSDT', 'BALUSDT', 'BANDUSDT', 'BARUSDT', 'BATUSDT', 'BCHUSDT', 'BELUSDT', 'BETAUSDT', 'BETHUSDT']
#
# two = ['BICOUSDT', 'BIFIUSDT', 'BLZUSDT', 'BNTUSDT', 'BNXUSDT', 'BONDUSDT', 'BSWUSDT', 'BTSUSDT', 'BTTCUSDT', 'BURGERUSDT', 'BUSDUSDT', 'C98USDT', 'CAKEUSDT', 'CELOUSDT', 'CELRUSDT', 'CFXUSDT', 'CHESSUSDT', 'CHRUSDT', 'CHZUSDT', 'CITYUSDT', 'CKBUSDT', 'CLVUSDT', 'COMBOUSDT', 'COMPUSDT', 'COSUSDT', 'COTIUSDT', 'CRVUSDT', 'CTKUSDT', 'CTSIUSDT', 'CTXCUSDT', 'CVCUSDT', 'CVPUSDT', 'CVXUSDT', 'CYBERUSDT', 'DARUSDT', 'DASHUSDT', 'DATAUSDT', 'DCRUSDT', 'DEGOUSDT', 'DENTUSDT', 'DEXEUSDT', 'DFUSDT', 'DGBUSDT', 'DIAUSDT', 'DOCKUSDT', 'DODOUSDT', 'DOGEUSDT', 'DOTUSDT', 'DREPUSDT', 'DUSKUSDT']
#
# three = ['DYDXUSDT', 'EDUUSDT', 'EGLDUSDT', 'ELFUSDT', 'ENJUSDT', 'ENSUSDT', 'EOSUSDT', 'EPXUSDT', 'ERNUSDT', 'ETCUSDT', 'EURUSDT', 'FARMUSDT', 'FDUSDUSDT', 'FETUSDT', 'FIDAUSDT', 'FILUSDT', 'FIOUSDT', 'FIROUSDT', 'FISUSDT', 'FLMUSDT', 'FLOKIUSDT', 'FLOWUSDT', 'FLUXUSDT', 'FORTHUSDT', 'FORUSDT', 'FRONTUSDT', 'FTMUSDT', 'FUNUSDT', 'FXSUSDT', 'GALAUSDT', 'GALUSDT', 'GASUSDT', 'GBPUSDT', 'GHSTUSDT', 'GLMRUSDT', 'GLMUSDT', 'GMTUSDT', 'GMXUSDT', 'GNOUSDT', 'GNSUSDT', 'GRTUSDT', 'GTCUSDT', 'HARDUSDT', 'HBARUSDT', 'HFTUSDT', 'HIFIUSDT', 'HIGHUSDT', 'HIVEUSDT', 'HOOKUSDT', 'HOTUSDT']
#
# four = ['ICPUSDT', 'ICXUSDT', 'IDEXUSDT', 'IDUSDT', 'ILVUSDT', 'IMXUSDT', 'INJUSDT', 'IOSTUSDT', 'IOTAUSDT', 'IOTXUSDT', 'IRISUSDT', 'JASMYUSDT', 'JOEUSDT', 'JSTUSDT', 'JUVUSDT', 'KAVAUSDT', 'KDAUSDT', 'KEYUSDT', 'KLAYUSDT', 'KMDUSDT', 'KNCUSDT', 'KP3RUSDT', 'KSMUSDT', 'LAZIOUSDT', 'LDOUSDT', 'LEVERUSDT', 'LINAUSDT', 'LINKUSDT', 'LITUSDT', 'LOKAUSDT', 'LOOMUSDT', 'LPTUSDT', 'LQTYUSDT', 'LRCUSDT', 'LSKUSDT', 'LTCUSDT', 'LTOUSDT', 'LUNAUSDT', 'LUNCUSDT', 'MAGICUSDT', 'MANAUSDT', 'MASKUSDT', 'MATICUSDT', 'MAVUSDT', 'MBLUSDT', 'MBOXUSDT', 'MCUSDT', 'MDTUSDT', 'MDXUSDT', 'MINAUSDT']
#
# five = ['MKRUSDT', 'MLNUSDT', 'MOBUSDT', 'MOVRUSDT', 'MTLUSDT', 'MULTIUSDT', 'NEARUSDT', 'NEOUSDT', 'NEXOUSDT', 'NKNUSDT', 'NMRUSDT', 'NULSUSDT', 'OAXUSDT', 'OCEANUSDT', 'OGNUSDT', 'OGUSDT', 'OMGUSDT', 'OMUSDT', 'ONEUSDT', 'ONGUSDT', 'ONTUSDT', 'OOKIUSDT', 'OPUSDT', 'ORNUSDT', 'OSMOUSDT', 'OXTUSDT', 'PAXGUSDT', 'PENDLEUSDT', 'PEOPLEUSDT', 'PEPEUSDT', 'PERLUSDT', 'PERPUSDT', 'PHAUSDT', 'PHBUSDT', 'PLAUSDT', 'PNTUSDT', 'POLSUSDT', 'POLYXUSDT', 'PONDUSDT', 'PORTOUSDT', 'POWRUSDT', 'PROMUSDT', 'PROSUSDT', 'PSGUSDT', 'PUNDIXUSDT', 'PYRUSDT', 'QIUSDT', 'QKCUSDT', 'QNTUSDT', 'QTUMUSDT']
#
# six = ['QUICKUSDT', 'RADUSDT', 'RAREUSDT', 'RAYUSDT', 'RDNTUSDT', 'REEFUSDT', 'REIUSDT', 'RENUSDT', 'REQUSDT', 'RIFUSDT', 'RLCUSDT', 'RNDRUSDT', 'ROSEUSDT', 'RPLUSDT', 'RSRUSDT', 'RUNEUSDT', 'RVNUSDT', 'SANDUSDT', 'SANTOSUSDT', 'SCRTUSDT', 'SCUSDT', 'SEIUSDT', 'SFPUSDT', 'SHIBUSDT', 'SKLUSDT', 'SLPUSDT', 'SNTUSDT', 'SNXUSDT', 'SOLUSDT', 'SPELLUSDT', 'SSVUSDT', 'STEEMUSDT', 'STGUSDT', 'STMXUSDT', 'STORJUSDT', 'STPTUSDT', 'STRAXUSDT', 'STXUSDT', 'SUIUSDT', 'SUNUSDT', 'SUPERUSDT', 'SUSHIUSDT', 'SXPUSDT', 'SYNUSDT', 'SYSUSDT', 'TFUELUSDT', 'THETAUSDT', 'TKOUSDT', 'TLMUSDT', 'TOMOUSDT']
#
# seven = ['TRBUSDT', 'TROYUSDT', 'TRUUSDT', 'TRXUSDT', 'TUSDT', 'TUSDUSDT', 'TVKUSDT', 'TWTUSDT', 'UFTUSDT', 'UMAUSDT', 'UNFIUSDT', 'UNIUSDT', 'USDCUSDT', 'USDPUSDT', 'USTCUSDT', 'UTKUSDT', 'VETUSDT', 'VGXUSDT', 'VIBUSDT', 'VIDTUSDT', 'VITEUSDT', 'VOXELUSDT', 'VTHOUSDT', 'WANUSDT', 'WAVESUSDT', 'WAXPUSDT', 'WBETHUSDT', 'WBTCUSDT', 'WINGUSDT', 'WINUSDT', 'WLDUSDT', 'WNXMUSDT', 'WOOUSDT', 'WRXUSDT', 'WTCUSDT', 'XECUSDT', 'XEMUSDT', 'XLMUSDT', 'XMRUSDT', 'XNOUSDT', 'XRPUSDT', 'XTZUSDT', 'XVGUSDT', 'XVSUSDT', 'YFIUSDT', 'YGGUSDT', 'ZECUSDT', 'ZENUSDT', 'ZILUSDT', 'ZRXUSDT']

# futures_exchange_info = client.futures_exchange_info()
# trading_pairs_fut = [info['symbol'] for info in futures_exchange_info['symbols'] if info['symbol'][-4:] == "USDT"]


# count = 0
# x = []
# for i in trading_pairs:
#     if count == 23:
#         print(x)
#         print(len(x))
#         count = 0
#         x = []
#     x.append(i)
#     count += 1
# print(x)




# url = "https://api.binance.com/api/v3/exchangeInfo"
# response = requests.get(url)
# data = response.json()
# symbols = [symbol["symbol"] for symbol in data["symbols"] if symbol['symbol'][-4:] == "USDT"]
# s = []
# for i in symbols:
#     if i not in x:
#         s.append(i)
# print(s[::-1])

did = [['NEOUSDT', 4568.559375, 1.99], ['LTCUSDT', 35695.0375, 1.56], ['QTUMUSDT', 1583.7625, 2.11], ['ADAUSDT', 59900.54375, 2.43], ['XRPUSDT', 148798.178125, 1.47], ['EOSUSDT', 8298.846875, 1.81], ['IOTAUSDT', 3478.228125, 2.24], ['XLMUSDT', 10288.565625, 1.49], ['ONTUSDT', 1353.04375, 2.3], ['TRXUSDT', 71857.315625, 0.68], ['ETCUSDT', 10198.365625, 1.85], ['ICXUSDT', 1106.328125, 2.14], ['DASHUSDT', 3083.584375, 1.72], ['THETAUSDT', 7764.725, 2.73], ['ENJUSDT', 4373.49375, 3.17], ['ATOMUSDT', 14522.00625, 2.38], ['TFUELUSDT', 991.05, 1.7], ['ONEUSDT', 2807.65625, 2.97], ['FTMUSDT', 78920.55, 2.91], ['ALGOUSDT', 10653.678125, 2.01], ['DOGEUSDT', 203693.61875, 2.82], ['DUSKUSDT', 2698.0, 3.15], ['ANKRUSDT', 3341.0375, 2.7], ['RVNUSDT', 5761.39375, 4.22], ['HBARUSDT', 13164.071875, 2.4], ['NKNUSDT', 2026.546875, 3.72], ['STXUSDT', 23918.140625, 2.4], ['KAVAUSDT', 3231.525, 2.52], ['ARPAUSDT', 20383.86875, 4.83], ['IOTXUSDT', 3793.84375, 2.93], ['RLCUSDT', 1711.321875, 3.28], ['CTXCUSDT', 2550.6375, 4.46], ['BCHUSDT', 18227.153125, 2.05], ['TROYUSDT', 1950.1875, 3.05], ['VITEUSDT', 2706.790625, 3.11], ['HIVEUSDT', 1128.41875, 1.88], ['CHRUSDT', 3694.621875, 3.32], ['ARDRUSDT', 1247.29375, 2.34], ['MDTUSDT', 6422.821875, 3.82], ['STMXUSDT', 2257.3125, 2.16], ['KNCUSDT', 4305.715625, 2.09], ['LRCUSDT', 2380.95625, 2.37], ['COMPUSDT', 2675.6, 1.95], ['SCUSDT', 2342.3875, 2.11], ['ZENUSDT', 2082.159375, 2.05], ['SNXUSDT', 4811.99375, 2.53], ['VTHOUSDT', 893.6125, 2.06], ['CATIUSDT', 20445.725, 5.08], ['CRVUSDT', 20442.634375, 2.17], ['SANDUSDT', 10512.865625, 2.49], ['NMRUSDT', 4158.9625, 2.74], ['DOTUSDT', 24176.015625, 1.81], ['LUNAUSDT', 9298.309375, 3.18], ['RSRUSDT', 7382.8, 3.69], ['TRBUSDT', 12424.509375, 3.14], ['SUSHIUSDT', 6131.290625, 2.88], ['KSMUSDT', 2693.4875, 2.37], ['EGLDUSDT', 6768.915625, 2.54], ['DIAUSDT', 17116.10625, 5.4], ['RUNEUSDT', 79577.471875, 3.57], ['ALPHAUSDT', 8589.128125, 8.58], ['AAVEUSDT', 26728.58125, 2.15], ['NEARUSDT', 87144.240625, 2.66], ['FILUSDT', 32608.2375, 2.21], ['INJUSDT', 29680.6, 2.62], ['AUDIOUSDT', 3574.83125, 4.35], ['CTKUSDT', 3065.221875, 4.68], ['AKROUSDT', 1162.803125, 1.97], ['AXSUSDT', 6668.965625, 2.77], ['HARDUSDT', 4930.959375, 3.64], ['STRAXUSDT', 542.215625, 1.76], ['UNFIUSDT', 23368.28125, 22.47], ['RIFUSDT', 1896.14375, 3.25], ['TRUUSDT', 6635.403125, 3.42], ['CKBUSDT', 14767.778125, 2.58], ['TWTUSDT', 4079.959375, 2.04], ['FIROUSDT', 955.928125, 1.92], ['LITUSDT', 2179.5875, 3.98], ['SFPUSDT', 1262.478125, 1.39], ['DODOUSDT', 3360.54375, 2.76], ['CAKEUSDT', 9201.396875, 2.09], ['ACMUSDT', 883.546875, 1.82], ['BADGERUSDT', 2323.78125, 2.86], ['FISUSDT', 2421.915625, 2.55], ['BNSOLUSDT', 2020.165625, 2.71], ['FORTHUSDT', 923.871875, 2.14], ['BAKEUSDT', 10250.9875, 3.12], ['BURGERUSDT', 1589.65, 2.44], ['SLPUSDT', 21633.8125, 6.51], ['SHIBUSDT', 66512.74375, 2.3], ['ICPUSDT', 23239.06875, 2.69], ['ARUSDT', 27709.48125, 2.83], ['MASKUSDT', 27324.834375, 2.58], ['LPTUSDT', 4901.49375, 2.75], ['XVGUSDT', 1092.821875, 2.61], ['ATAUSDT', 1988.253125, 5.18], ['GTCUSDT', 3871.184375, 3.78], ['ALPACAUSDT', 1719.321875, 3.73], ['QUICKUSDT', 2378.51875, 2.79], ['MBOXUSDT', 4169.465625, 4.16], ['REQUSDT', 341.996875, 1.76], ['GHSTUSDT', 1329.740625, 3.19], ['WAXPUSDT', 2394.4125, 2.22], ['GNOUSDT', 6868.66875, 3.9], ['XECUSDT', 2323.878125, 2.23], ['ELFUSDT', 1345.31875, 1.29], ['DYDXUSDT', 36321.303125, 3.78], ['IDEXUSDT', 1396.453125, 2.81], ['RAREUSDT', 7715.4, 3.04], ['LAZIOUSDT', 1865.1375, 2.62], ['CHESSUSDT', 4720.878125, 5.59], ['ADXUSDT', 2271.99375, 4.12], ['AUCTIONUSDT', 6166.590625, 3.35], ['DARUSDT', 4803.78125, 3.25], ['BNXUSDT', 16306.95, 3.86], ['MOVRUSDT', 3882.221875, 3.04], ['CITYUSDT', 823.0375, 1.65], ['ENSUSDT', 12346.665625, 2.47], ['KP3RUSDT', 2950.6875, 8.72], ['QIUSDT', 1146.375, 2.06], ['HIGHUSDT', 6230.80625, 3.02], ['CVXUSDT', 1412.934375, 2.53], ['PEOPLEUSDT', 170395.815625, 4.02], ['OOKIUSDT', 8664.934375, 12.28], ['SPELLUSDT', 3680.88125, 3.68], ['JOEUSDT', 1623.125, 2.61], ['DOGSUSDT', 60670.76875, 3.68], ['ACHUSDT', 5620.778125, 3.1], ['IMXUSDT', 5213.14375, 2.53], ['GLMRUSDT', 2329.11875, 2.25], ['LOKAUSDT', 2294.790625, 3.12], ['SCRTUSDT', 854.121875, 2.63], ['API3USDT', 4620.815625, 3.8], ['STEEMUSDT', 1531.9375, 2.03], ['NEXOUSDT', 1174.75, 1.74], ['REIUSDT', 3943.69375, 3.93], ['LDOUSDT', 16180.51875, 2.55], ['OPUSDT', 35057.478125, 2.78], ['RENDERUSDT', 39995.3125, 3.01], ['LEVERUSDT', 4349.73125, 3.04], ['STGUSDT', 2022.303125, 1.93], ['LUNCUSDT', 12415.309375, 2.82], ['GMXUSDT', 3189.621875, 2.44], ['POLYXUSDT', 7205.865625, 3.13], ['APTUSDT', 89597.41875, 4.07], ['BANANAUSDT', 8674.596875, 2.87], ['LUMIAUSDT', 41054.665625, 6.7], ['LQTYUSDT', 18456.490625, 3.25], ['AMBUSDT', 2501.653125, 3.44], ['USTCUSDT', 9099.90625, 3.62], ['GASUSDT', 7886.165625, 2.33], ['GLMUSDT', 2067.728125, 2.3], ['PROMUSDT', 96498.89375, 7.66], ['LISTAUSDT', 5265.1125, 3.58], ['QKCUSDT', 3126.85, 1.89], ['UFTUSDT', 437.659375, 1.39], ['IDUSDT', 8957.44375, 3.83], ['ARBUSDT', 70628.359375, 2.51], ['OAXUSDT', 1225.903125, 2.56], ['ZKUSDT', 23047.76875, 3.51], ['ARKMUSDT', 33225.884375, 3.6], ['WBETHUSDT', 1593.434375, 1.76], ['WLDUSDT', 138161.79375, 3.67], ['SEIUSDT', 83381.403125, 2.93], ['CYBERUSDT', 8204.065625, 3.22], ['ARKUSDT', 5318.715625, 3.11], ['BBUSDT', 14611.04375, 3.56], ['CREAMUSDT', 1248.453125, 2.72], ['GFTUSDT', 1623.2875, 2.18], ['IQUSDT', 7507.26875, 2.9], ['NTRNUSDT', 1640.8125, 2.61], ['TIAUSDT', 73026.76875, 3.78], ['MEMEUSDT', 63394.409375, 4.09], ['REZUSDT', 8127.6875, 3.84], ['XAIUSDT', 14900.440625, 4.02], ['MANTAUSDT', 22495.446875, 3.41], ['ALTUSDT', 19010.2625, 3.45], ['JUPUSDT', 51150.621875, 4.53], ['PYTHUSDT', 19340.35625, 3.64], ['RONINUSDT', 7645.271875, 2.68], ['SAGAUSDT', 57620.996875, 4.5], ['DYMUSDT', 10165.925, 3.9], ['PIXELUSDT', 30627.225, 6.53], ['STRKUSDT', 33611.7125, 3.16], ['PORTALUSDT', 11341.803125, 4.63], ['PDAUSDT', 1925.140625, 3.53], ['AXLUSDT', 5903.134375, 3.98], ['TNSRUSDT', 29110.15625, 5.33], ['HMSTRUSDT', 13507.303125, 4.18], ['NULSUSDT', 1497.128125, 2.96], ['VETUSDT', 7040.94375, 2.05], ['LINKUSDT', 63304.575, 2.67], ['ONGUSDT', 1236.146875, 2.05], ['HOTUSDT', 5035.40625, 3.38], ['ZILUSDT', 3971.33125, 2.64], ['ZRXUSDT', 4754.578125, 3.41], ['FETUSDT', 72193.18125, 3.15], ['BATUSDT', 1206.134375, 2.35], ['ZECUSDT', 4220.909375, 2.9], ['IOSTUSDT', 2391.028125, 2.24], ['CELRUSDT', 2645.915625, 2.8], ['WINUSDT', 724.584375, 1.27], ['COSUSDT', 2213.853125, 1.93], ['MTLUSDT', 2253.05625, 4.18], ['DENTUSDT', 2014.2875, 2.68], ['KEYUSDT', 5133.190625, 3.19], ['WANUSDT', 408.315625, 1.98], ['FUNUSDT', 1043.715625, 1.61], ['CVCUSDT', 25922.35625, 3.67], ['CHZUSDT', 12457.984375, 2.86], ['BANDUSDT', 1352.35, 2.61], ['XTZUSDT', 2809.61875, 1.84], ['RENUSDT', 1028.575, 3.11], ['FTTUSDT', 13068.04375, 3.56], ['OGNUSDT', 1351.334375, 2.38], ['WRXUSDT', 645.96875, 1.96], ['LSKUSDT', 1067.228125, 2.31], ['BNTUSDT', 675.659375, 2.11], ['LTOUSDT', 1288.03125, 3.16], ['MBLUSDT', 4084.565625, 1.47], ['COTIUSDT', 6694.93125, 3.52], ['STPTUSDT', 2038.559375, 1.57], ['DATAUSDT', 1727.54375, 3.5], ['SOLUSDT', 1139447.08125, 2.49], ['CTSIUSDT', 2215.253125, 5.23], ['DGBUSDT', 919.478125, 2.54], ['SXPUSDT', 2517.875, 2.25], ['MKRUSDT', 22804.321875, 2.51], ['DCRUSDT', 1170.48125, 1.95], ['STORJUSDT', 11458.715625, 3.33], ['MANAUSDT', 4969.971875, 2.72], ['YFIUSDT', 2784.328125, 1.72], ['BALUSDT', 1444.49375, 2.11], ['BLZUSDT', 1882.5875, 3.38], ['IRISUSDT', 751.6875, 2.3], ['KMDUSDT', 894.8, 2.08], ['JSTUSDT', 1652.803125, 0.82], ['FIOUSDT', 3348.20625, 3.61], ['UMAUSDT', 5611.45, 3.3], ['BELUSDT', 5280.440625, 3.86], ['WINGUSDT', 41955.69375, 5.09], ['UNIUSDT', 74169.0, 3.45], ['OXTUSDT', 1340.465625, 2.73], ['SUNUSDT', 11216.94375, 2.88], ['AVAXUSDT', 64405.034375, 2.23], ['FLMUSDT', 1318.45, 3.15], ['UTKUSDT', 1187.20625, 2.26], ['XVSUSDT', 8102.665625, 2.42], ['EIGENUSDT', 46224.54375, 3.86], ['ROSEUSDT', 7636.171875, 3.17], ['AVAUSDT', 391.74375, 1.71], ['SKLUSDT', 2563.25, 3.07], ['GRTUSDT', 11429.3625, 2.42], ['JUVUSDT', 1225.46875, 1.83], ['PSGUSDT', 3736.915625, 3.3], ['1INCHUSDT', 4974.021875, 2.63], ['OGUSDT', 20139.384375, 4.98], ['ATMUSDT', 2310.51875, 1.95], ['ASRUSDT', 1527.875, 1.96], ['CELOUSDT', 15613.240625, 3.11], ['TURBOUSDT', 57584.728125, 5.02], ['SCRUSDT', 48347.259375, 10.04], ['OMUSDT', 12588.625, 2.5], ['PONDUSDT', 1692.09375, 2.26], ['DEGOUSDT', 6491.509375, 4.57], ['ALICEUSDT', 3499.6625, 3.29], ['LINAUSDT', 4032.65625, 2.99], ['PERPUSDT', 2677.7875, 3.65], ['SUPERUSDT', 14469.565625, 4.03], ['CFXUSDT', 15378.2125, 3.13], ['TKOUSDT', 1423.8125, 2.09], ['PUNDIXUSDT', 1100.775, 1.82], ['TLMUSDT', 3811.85625, 3.17], ['BARUSDT', 872.071875, 1.72], ['ERNUSDT', 33453.9625, 5.78], ['KLAYUSDT', 2955.75, 1.32], ['PHAUSDT', 2163.15, 3.03], ['MLNUSDT', 916.178125, 2.98], ['DEXEUSDT', 479.234375, 1.73], ['C98USDT', 3413.834375, 2.86], ['CLVUSDT', 1734.796875, 2.28], ['QNTUSDT', 5934.378125, 1.93], ['FLOWUSDT', 3845.471875, 2.29], ['MINAUSDT', 8472.2, 3.06], ['RAYUSDT', 78718.884375, 6.29], ['FARMUSDT', 895.0625, 2.11], ['VIDTUSDT', 8431.48125, 3.11], ['GALAUSDT', 35094.375, 3.7], ['CATIUSDT', 21756.35, 5.14], ['ILVUSDT', 6600.4, 3.44], ['YGGUSDT', 10390.0, 3.88], ['SYSUSDT', 2777.35625, 3.84], ['DFUSDT', 510.63125, 1.79], ['FIDAUSDT', 14426.221875, 5.45], ['AGLDUSDT', 2474.08125, 3.47], ['RADUSDT', 52272.45625, 8.4], ['BETAUSDT', 4141.525, 2.29], ['PORTOUSDT', 1997.396875, 2.99], ['POWRUSDT', 1324.6125, 2.1], ['JASMYUSDT', 19373.465625, 3.1], ['AMPUSDT', 4462.171875, 4.87], ['PYRUSDT', 2792.653125, 2.52], ['ALCXUSDT', 960.996875, 2.37], ['SANTOSUSDT', 22085.8875, 3.44], ['BICOUSDT', 6234.125, 3.16], ['FLUXUSDT', 2211.38125, 2.63], ['FXSUSDT', 2416.815625, 2.21], ['VOXELUSDT', 2787.25, 3.95], ['1MBABYDOGEUSDT', 41442.440625, 4.49], ['BTTCUSDT', 2619.475, 2.12], ['ACAUSDT', 1767.51875, 3.43], ['XNOUSDT', 620.490625, 2.37], ['WOOUSDT', 5807.878125, 3.5], ['ALPINEUSDT', 2636.725, 2.48], ['TUSDT', 2147.984375, 2.14], ['ASTRUSDT', 8650.703125, 2.34], ['GMTUSDT', 14751.8875, 2.93], ['KDAUSDT', 3847.540625, 2.9], ['APEUSDT', 95205.83125, 7.04], ['BSWUSDT', 2219.03125, 2.6], ['BIFIUSDT', 527.74375, 2.05], ['TONUSDT', 61153.178125, 1.68], ['OSMOUSDT', 2087.33125, 1.93], ['HFTUSDT', 2105.4625, 2.69], ['PHBUSDT', 8730.53125, 3.71], ['HOOKUSDT', 2969.8875, 3.25], ['MAGICUSDT', 5193.971875, 3.71], ['HIFIUSDT', 3227.571875, 2.93], ['GUSDT', 3247.3875, 2.02], ['RPLUSDT', 958.240625, 2.5], ['PROSUSDT', 16639.721875, 4.07], ['GNSUSDT', 1339.390625, 2.23], ['SYNUSDT', 8015.203125, 4.25], ['VIBUSDT', 1324.121875, 2.04], ['SSVUSDT', 10086.846875, 2.93], ['ZROUSDT', 36238.265625, 3.1], ['RDNTUSDT', 9103.76875, 3.3], ['WBTCUSDT', 3183.996875, 1.24], ['EDUUSDT', 7593.26875, 2.73], ['SUIUSDT', 319313.80625, 3.29], ['AERGOUSDT', 1780.059375, 2.4], ['PEPEUSDT', 322039.38125, 2.98], ['IOUSDT', 38149.00625, 4.27], ['FLOKIUSDT', 67724.615625, 3.03], ['ASTUSDT', 617.80625, 2.03], ['SNTUSDT', 2336.528125, 3.36], ['COMBOUSDT', 2779.634375, 3.09], ['MAVUSDT', 4938.03125, 3.57], ['PENDLEUSDT', 38471.865625, 3.65], ['NOTUSDT', 66090.515625, 3.08], ['ORDIUSDT', 52507.559375, 3.11], ['BEAMXUSDT', 13406.025, 4.61], ['PIVXUSDT', 352.45625, 2.24], ['VICUSDT', 658.996875, 2.81], ['BLURUSDT', 10763.984375, 3.21], ['VANRYUSDT', 7956.525, 3.54], ['OMNIUSDT', 6604.890625, 3.4], ['JTOUSDT', 24798.525, 4.29], ['1000SATSUSDT', 66117.996875, 3.15], ['BONKUSDT', 56352.671875, 3.49], ['ACEUSDT', 7072.178125, 4.03], ['NFPUSDT', 4702.7125, 3.33], ['AIUSDT', 8431.453125, 3.95], ['TAOUSDT', 84017.125, 3.46], ['WIFUSDT', 208003.65, 4.03], ['METISUSDT', 7105.93125, 3.86], ['AEVOUSDT', 15840.6125, 3.05], ['BOMEUSDT', 164779.859375, 4.94], ['ETHFIUSDT', 37837.34375, 3.63], ['ENAUSDT', 62143.809375, 4.29], ['WUSDT', 15752.653125, 3.21], ['HMSTRUSDT', 14319.0875, 4.18], ['NEIROUSDT', 364432.075, 6.71]]
def top_coin(trading_pairs: list):
    j = []
    for name_cript_check in trading_pairs:
        try:
            data_token: Dataset = last_data(name_cript_check, "4h", "17280")
            volume_per_5h: float = sum([int(i * data_token.high_price[-1]) for i in data_token.volume[-6:]]) / len(
                data_token.volume[-6:]) / 80
            res: float = round(data_token.close_price[-2] / data_token.open_price[-2] * 100 - 100, 2)
            res_2: float = round(data_token.close_price[-3] / data_token.open_price[-3] * 100 - 100, 2)
            res_3: float = round(data_token.close_price[-4] / data_token.open_price[-4] * 100 - 100, 2)
            res_4: float = round(data_token.close_price[-5] / data_token.open_price[-5] * 100 - 100, 2)
            res_5: float = round(data_token.close_price[-6] / data_token.open_price[-6] * 100 - 100, 2)
            price_change_percent_24h: float = round(
                ((data_token.close_price[-1] / data_token.open_price[-6]) * 100) - 100, 2)
            price_change_percent_7d: float = round(
                ((max(data_token.high_price) / data_token.close_price[-1]) * 100) - 100, 2)
            res_sum5 = round(sum(list(map(lambda x: x[0] / x[1] * 100 - 100,
                                          list(zip(data_token.high_price[-5:], data_token.low_price[-5:]))))), 2)

            pattern_ravenstva_svechei = abs(res) - abs(res_2)
            try:
                percent_raznici_svechei = abs(pattern_ravenstva_svechei) / abs(res_2) * 100
            except:
                percent_raznici_svechei = 80

            '''процент падения за последние 2ч. Отрицательные значение == был рост'''
            loss_price_for_two_hours: float = round(
                100 - data_token.close_price[-2] / max([i for i in data_token.open_price[-9:]]) * 100, 2)

            if ((-4.1 > res > -20)
                or (
                        res < -2 and res_2 < -0.8 and res_3 < -0.8 and res_4 < -0.8 and res_5 < -0.8 and res + res_2 + res_3 + res_4 + res_5 < -10)) \
                    or (
                    res < -2 and res_2 < -0.8 and res_3 < -0.8 and res_4 < -0.8 and res + res_2 + res_3 + res_4 < -9) \
                    or (res < -2 and res_2 < -0.8 and res_3 < -0.8 and res + res_2 + res_3 < -8) \
                    or (res < -2 and res_2 < -2 and res + res_2 < -6):

                if res < -2 and res_2 < -0.8 and res_3 < -0.8 and res_4 < -0.8 and res_5 < -0.8 and res + res_2 + res_3 + res_4 + res_5 < -15:
                    res_before: float = round(
                        data_token.close_price[-1] / min(data_token.low_price[-5:]) * 100 - 100, 2)
                    if res_before == 0:
                        res_k_low = 10000
                    else:
                        res_k_low = round(abs(res + res_2 + res_3 + res_4 + res_5) / res_before * 100, 2)

                    if res_sum5 < 30:
                        sell_pr = 101
                    elif res_sum5 > 50:
                        sell_pr = 101.5
                    else:
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


                elif res < -2 and res_2 < -0.8 and res_3 < -0.8 and res_4 < -0.8 and res + res_2 + res_3 + res_4 < -12:
                    res_before: float = round(
                        data_token.close_price[-1] / min(data_token.low_price[-4:]) * 100 - 100, 2)
                    if res_before == 0:
                        res_k_low = 10000
                    else:
                        res_k_low = round(abs(res + res_2 + res_3 + res_4) / res_before * 100, 2)

                    if res_sum5 < 30:
                        sell_pr = 101
                    elif res_sum5 > 50:
                        sell_pr = 101.5
                    else:
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


                elif res < -2 and res_2 < -0.8 and res_3 < -0.8 and res + res_2 + res_3 < -10:
                    res_before: float = round(data_token.close_price[-1] / min(data_token.low_price[-3:]) * 100 - 100,
                                              2)
                    if res_before == 0:
                        res_k_low = 10000
                    else:
                        res_k_low = round(abs(res + res_2 + res_3) / res_before * 100, 2)

                    if res_sum5 < 30:
                        sell_pr = 101
                    elif res_sum5 > 50:
                        sell_pr = 101.5
                    else:
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


                elif res < -2 and res_2 < -2 and res + res_2 < -8:
                    res_before: float = round(data_token.close_price[-1] / min(data_token.low_price[-2:]) * 100 - 100,
                                              2)
                    if res_before == 0:
                        res_k_low = 10000
                    else:
                        res_k_low = round(abs(res + res_2) / res_before * 100, 2)

                    if res_sum5 < 30:
                        sell_pr = 101
                    elif res_sum5 > 50:
                        sell_pr = 101.5
                    else:
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


                elif -4.2 > res and percent_raznici_svechei > 15:
                    res_before: float = round(data_token.close_price[-1] / data_token.low_price[-1] * 100 - 100, 2)
                    if res_before == 0:
                        res_k_low = 10000
                    else:
                        res_k_low = round(abs(res) / res_before * 100, 2)

                    if res_sum5 < 30:
                        sell_pr = 101
                    elif res_sum5 > 50:
                        sell_pr = 101.5
                    else:
                        sell_pr = 101.15

                    """Волатильность по фреймам"""
                    high_frames = list(map(lambda x: round(x[1] / x[0] * 100 - 100, 2),
                                           zip(data_token.open_price, data_token.high_price)))
                    awerage_high_frame = len([i for i in high_frames if i > sell_pr - 100])

                    telebot.TeleBot(telega_token).send_message(chat_id, f"RABOTAEM 4 ЧАСОВИК- {name_cript_check}\n"
                                                                        f"{time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))}\n"
                                                                        f"Рост по фреймам - {len([i for i in high_frames if i > sell_pr - 100])}\n"
                                                                        f"Объемы {int(volume_per_5h)}\n"
                                                                        f"Цена упала на {res}%\n"
                                                                        f"Свечной хвостик {res_k_low}%\n"
                                                                        f"Изменение цены за сутки {price_change_percent_24h}%\n")
        except Exception as e:
            pass



dd = [['PROSUSDT', -17.14, 29.11, 50.0, 24.61, 106.93], ['SCRUSDT', -4.55, -10.45, 44.0, 28.42, 22.12]]

print(sorted(dd, key=lambda x: -x[5])[0][5])


#print([[i] for i in sorted(did, key=lambda x: x[1]) if i[1] < 3000 and i[2] < 2])
#print(sorted(did, key=lambda x: x[2]))
#print([[all_cripts_workss[i], all_cripts_workss[i+1]] for i in range(0, len(all_cripts_workss), 2)])


# while True:
#     start = time.time()
#     print("start")
#
#     '''Старт программы'''
#     threads = [Thread(target=top_coin, args=([i])) for i in all_cripts_workss]
#
#     start_threads = [i.start() for i in threads]
#
#     stop_threads = [i.join() for i in threads]
#
#     print("finish")
#     finish = time.time()
#     print(finish - start)




# from binance.exceptions import BinanceAPIException
# #x = Decimal(str(round((buyprice / 100) * sell_pr, max([len(f'{i:.15f}'.rstrip("0").split(".")[1]) for i in data_token[0][-5:]]))))
# buyprice = 0.004146
# data_token: Dataset = last_data("REEFUSDT", "4h", "1440")
# try:
#     x = Decimal(str(round((buyprice / 100) * 101.15, max([len(f'{i:.15f}'.rstrip("0").split(".")[1]) for i in data_token[0][-5:]]))))
#     print(x)
#     order_sell = client.order_limit_sell(symbol="REEFUSDT", quantity=4825.0, price=x)
# except BinanceAPIException as e:
#     print(e)



# tt =  [['FETUSDT', -4.34, 3.49, 16.0], ['BONKUSDT', -4.84, 0.16, 16.0], ['NFPUSDT', -4.37, 7.42, 15.0], ['WLDUSDT', -8.74, 16.89, 14.0], ['ARKMUSDT', -6.39, 19.64, 14.0]]
# t = [['FETUSDT', 3.43], ['BONKUSDT', 4.63], ['NFPUSDT', 3.46], ['WLDUSDT', 2.5], ['ARKMUSDT', 3.14]]
# #
# # for i in tt:
# #     data_token: Dataset = last_data(i[0], "4h", "4320")
# #     kk = list(map(lambda x: round(x[0] / x[1] * 100 - 100, 2), zip(data_token.high_price, data_token.close_price)))
# #
# #     high_low_change: float = round(data_token.high_price[-1] / data_token.low_price[-1] * 100 - 100, 2)
# #     print(i[0], sum(kk)/len(kk))
# #     t.append([i[0], round(sum(kk)/len(kk), 2)])
# print(sorted(t, key=lambda x: -x[1]))
#
# reit_timeframe_change = [i[0] for i in sorted(tt, key=lambda x: x[1])]
# reit_day_change = [i[0] for i in sorted(tt, key=lambda x: x[2])]
# #reit_awerage_high_frame = [i[0] for i in sorted(reit_bd_cript, key=lambda x: -x[3])]
#
# """Формируем список крипт со значениями"""
# itog = []
# for i in reit_timeframe_change:
#     for j in tt:
#         if i == j[0]:
#             itog.append([i, reit_timeframe_change.index(i), reit_day_change.index(i), j[3]])
#
# """Определяем топ крипту и оставшийся массив для доп закупа"""
# # top = sorted(reit_bd_cript, key=lambda x: -x[3])[0][0]
# # all_work_crypt = sorted(reit_bd_cript, key=lambda x: -x[3])[1:]
# top = sorted([[i[0], i[1] + i[2], i[3]] for i in itog], key=lambda x: (-x[2], x[1]))
# all_work_crypt = sorted([[i[0], i[1] + i[2], i[3]] for i in itog], key=lambda x: (-x[2], [1]))[1:]
# print(top)


#from binance import ThreadedWebsocketManager

# handler = TA_Handler(
#     symbol="GASUSDT",
#     exchange="binance",
#     screener="crypto",
#     interval=Interval.INTERVAL_2_HOURS,
#     timeout=None
# )
#
# print(handler.get_analysis().summary)
# print(handler.get_analysis().oscillators)
# print(handler.get_analysis().oscillators["COMPUTE"]["STOCH.K"])
# print(handler.get_analysis().oscillators["COMPUTE"]["Mom"])
# print(handler.get_analysis().oscillators["COMPUTE"]["CCI"])
# print(handler.get_analysis().oscillators["COMPUTE"]["RSI"])
# print(handler.get_analysis().oscillators["COMPUTE"]["MACD"])



# def sql_del():
#     try:
#         connection = pymysql.connect(host='127.0.0.1', port=3306, user='banan_user',
#                                      password='warlight123',
#                                      database='banans',
#                                      cursorclass=pymysql.cursors.DictCursor)
#         try:
#             with connection.cursor() as cursor:
#                 insert_query = "DELETE FROM `1h_info`"
#                 cursor.execute(insert_query)
#                 connection.commit()
#         finally:
#             connection.close()
#
#     except Exception as e:
#         print(e)

def sql_req_high():
    try:
        connection = pymysql.connect(host='127.0.0.1', port=3306, user='banan_user', password='warlight123',
                                             database='banans',
                                             cursorclass=pymysql.cursors.DictCursor)
        try:
            with connection.cursor() as cursor:
                cursor.execute("SELECT title, count(price_high)  FROM banans.new_table WHERE price_high >= 1.15 GROUP BY title")
                result = cursor.fetchall()
        finally:
            connection.close()

        return sorted([[i["title"], i["count(price_high)"]] for i in result])

    except Exception as e:
        telebot.TeleBot(telega_token).send_message(-695765690, f"SQL ERROR get top cripto connect: {e}\n")

def sql_req_low():
    try:
        connection = pymysql.connect(host='127.0.0.1', port=3306, user='banan_user', password='warlight123',
                                             database='banans',
                                           cursorclass=pymysql.cursors.DictCursor)
        try:
            with connection.cursor() as cursor:
                cursor.execute("SELECT title, count(price_high)  FROM banans.new_table WHERE price_high < 1.15 GROUP BY title")
                result = cursor.fetchall()
        finally:
            connection.close()

        return sorted([[i["title"], i["count(price_high)"]] for i in result])

    except Exception as e:
        telebot.TeleBot(telega_token).send_message(-695765690, f"SQL ERROR get top cripto connect: {e}\n")

# high = sql_req_high()
# low = sql_req_low()
#
# gf = []
# for i in high:
#     for j in low:
#         if i[0] == j[0]:
#             if j[1] == 0:
#                 gf.append([i[0], i[1], j[1], i[1]])
#             else:
#                 gf.append([i[0], i[1], j[1], round(i[1]/j[1], 2)])
#
# print(gf)
# print(sorted(gf, key=lambda x: -x[3]))


# hhhhh = []
# ddd = {}
# sql_del()
# for d in x:
#     data = []
#     try:
#         data_token = last_data(d, "4h", "600000")
#
#         open = data_token.open_price
#
#         close = data_token.close_price
#
#
#         low = data_token.low_price
#
#         high = data_token.high_price
#
#         close_it = list(map(lambda x: round((x[1]/x[0] * 100 - 100), 2), zip(open, close)))
#
#         high_it = list(map(lambda x: abs(round((x[1]/x[0] * 100 - 100), 2)), zip(high, open)))
#
#         print(d, close_it)
#         for i in range(1, len(close_it)-4):
#
#              # if it[i] < - 3.1 and high_it[i + 1] < 1:
#              #     print(it[i], high_it[i+1], d)
#
#              if close_it[i] < -4:
#                  if d not in ddd:
#                      ddd[d] = [close_it[i], high_it[i+1]]
#                      print(close_it[i], high_it[i+1], d)
#                      hhhhh.append(high_it[i+1])
#                      values = (d, close_it[i], high_it[i+1], close_it[i+1], high_it[i+2], close_it[i+2],
#                                high_it[i+3], close_it[i+3], high_it[i+4], close_it[i+4])
#
#                      try:
#                          connection = pymysql.connect(host='127.0.0.1', port=3306, user='banan_user',
#                                                       password='warlight123',
#                                                       database='banans',
#                                                       cursorclass=pymysql.cursors.DictCursor)
#                          try:
#                              with connection.cursor() as cursor:
#                                  insert_query = "INSERT INTO `1h_info` (title, price_loss, price_high, price_close, price_next_high, price_next_close," \
#                                                 "price_2next_high, price_2next_close, price_3next_high, price_3next_close) " \
#                                                 "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
#                                  cursor.execute(insert_query, (values))
#                                  connection.commit()
#                          except Exception as e:
#                              print(e)
#                          finally:
#                              connection.close()
#                      except Exception as e:
#                          print(e)
#
#                  else:
#                      ddd[d] += close_it[i], high_it[i + 1]
#                      values = (d, close_it[i], high_it[i+1], close_it[i+1],
#                                high_it[i+2], close_it[i+2], high_it[i+3], close_it[i+3], high_it[i+4], close_it[i+4])
#
#                      try:
#                          connection = pymysql.connect(host='127.0.0.1', port=3306, user='banan_user',
#                                                       password='warlight123',
#                                                       database='banans',
#                                                       cursorclass=pymysql.cursors.DictCursor)
#                          try:
#                              with connection.cursor() as cursor:
#                                  insert_query = "INSERT INTO `1h_info` (title, price_loss, price_high, price_close, price_next_high, price_next_close, " \
#                                                 "price_2next_high, price_2next_close, price_3next_high, price_3next_close) " \
#                                                 "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
#                                  cursor.execute(insert_query, (values))
#                                  connection.commit()
#                          except Exception as e:
#                              print(e)
#                          finally:
#                              connection.close()
#                      except Exception as e:
#                          print(e)
#     except Exception as e:
#         print(e)
#
# print(ddd)

# start_time_check = time.time()
# '''Заглушка для ожидания конца таймфрейма 15 мин'''
# while time.localtime(start_time_check).tm_min % 15 != 14 or time.localtime(start_time_check).tm_sec < 48:
#     start_time_check = time.time()
#     time.sleep(1)
#     print(time.localtime(start_time_check).tm_min, time.localtime(start_time_check).tm_sec)
#
#
# if time.localtime(time.time()).tm_min == 59:
#     print("4aCoBuk")
# else:
#     print("15 min")
# bd_cript = get_top_crypto()
# reit_bd_cript = []
# all_cript = [['SYSUSDT', 28, 1, 2.76], ['PHBUSDT', 30, 2, 5.87]]
# print(bd_cript)
#
# for i in all_cript:
#     for j in bd_cript:
#         if i[0] == j['name_cript']:
#             reit_bd_cript.append([j['name_cript'], i[3], j["res"]])
#
# if -30 < sorted(reit_bd_cript, key=lambda x: x[2])[0][2] < -20:
#     top = sorted(reit_bd_cript, key=lambda x: [x[2], -x[1]])[0][0]
#     sell_pr = 103
#
# elif sorted(reit_bd_cript, key=lambda x: x[2])[0][2] < -30:
#     top = sorted(reit_bd_cript, key=lambda x: [x[2], -x[1]])[0][0]
#     sell_pr = 105
#
# else:
#     top = sorted(reit_bd_cript, key=lambda x: -x[1])[0][0]
#     sell_pr = 101.15
"""Алгоритм сбора данных """
# hhhhh = []
# ddd = {}
# data = []
# data_token = last_data("NTRNUSDT", "4h", "4440")
# open = data_token.open_price
#
# close = data_token.close_price
#
# low = data_token.low_price
#
# high = data_token.high_price
#
# high_it = list(map(lambda x: abs(round((x[1]/x[0] * 100 - 100), 2)), zip(high, open)))
#
# close_it = list(map(lambda x: round((x[1]/x[0] * 100 - 100), 2), zip(open, close)))
#
# #low_it = list(map(lambda x: round((x[0] / x[1] * 100 - 100), 2), zip(low, open)))
#
# print(list(zip(close_it, high_it)))

# for i in range(1, len(it)-2):
#
#     # if it[i] < - 3.1 and high_it[i + 1] < 1:
#     #     print(it[i], high_it[i+1], d)
#
#     if it[i] < -3:
#         if d not in ddd:
#             ddd[d] = [it[i], high_it[i+1]]
#             print(it[i], high_it[i+1], d)
#             hhhhh.append(high_it[i+1])
#             values = (d, it[i-1], it[i], high_it[i+1], close_it[i+1], low_it[i+1], it.index(it[i]),
#                                close_it[i+2])

# i = "ARDRUSDT"
# data_token = last_data(i, "1h", "150000")
# open_price_1 = 7262
# close_price_1 = 6705
#
# open_price_2 = 6739
# close_price_2 = 7262
#
# res: float = round(close_price_1 / open_price_1 * 100 - 100, 2)
# res_before: float = round(close_price_2 / open_price_2 * 100 - 100, 2)
#
# print(res)
# print(res_before)
# x = -6.2
# y = 39.32
# print(abs(x) / y)
# print(abs(res) / res_before)


# sql_del()
# # equal('WOOUSDT', -4.09, 1, 11.37, 0.5)
# # equal('FRONTUSDT', -5.91, 1, -0.76, 1.5)
# # equal('UNIUSDT', -7.19, 1, -16.96, 3.0)
# # equal('SCUSDT', 0, 1, 100, 0.2)
#
# bd_cript = [['VIDTUSDT', -7.96, 16.59, 3.4], ['REEFUSDT', -6.94, 23.55, 3.77], ['AUDIOUSDT', -6.62, 16.93, 3.83], ['AMBUSDT', -5.39, 21.52, 3.36], ['ARDRUSDT', -5.14, 9.86, 2.67], ['COMBOUSDT', -5.02, 23.24, 3.9], ['GLMUSDT', -4.64, 83.14, 8.13], ['SYSUSDT', -4.45, 34.48, 6.06], ['PROSUSDT', -4.29, 0.53, 1.18], ['PERPUSDT', -4.13, 20.74, 3.64], ['FILUSDT', -4.12, 20.6, 3.41], ['MOBUSDT', -4.04, 6.95, 2.43], ['PDAUSDT', -4.04, 21.52, 8.63], ['ELFUSDT', -4.03, 6.27, 1.92]]
#
# '''Проверка на наилучший объект и работа с ним дальше'''
# reit_bd_cript = []
#
# for j in bd_cript:
#     reit_bd_cript.append([j[0], j[1], j[2], j[3]])
# print(sorted(reit_bd_cript, key=lambda x: (-x[3], x[1])))
# print(sorted(reit_bd_cript, key=lambda x: x[2])[0][0])


# d =  [['SPELLUSDT', -8.17, 3.69], ['PHAUSDT', -7.09, -11.45], ['JASMYUSDT', -6.17, 14.42], ['COTIUSDT', -6.16, -14.97], ['VGXUSDT', -5.42, 3.49], ['OMUSDT', -5.15, 13.52], ['LDOUSDT', -4.29, -2.8], ['STXUSDT', -4.16, 1.9]]
# k = [i[0] for i in sorted(d, key=lambda x: x[1])]
# m = [i[0] for i in sorted(d, key=lambda x: x[2])]
# #[['PYTHUSDT', -8.61, 27.21], ['TFUELUSDT', -7.08, 7.81], ['XVGUSDT', -6.37, -0.75], ['HOTUSDT', -6.2, 10.28]]
# #[['XVGUSDT', -6.37, -0.75], ['TFUELUSDT', -7.08, 7.81], ['HOTUSDT', -6.2, 10.28], ['PYTHUSDT', -8.61, 27.21]]
# itog = []
# for i in k:
#     itog.append([i, k.index(i), m.index(i)])
# print(sorted([[i[0], i[1]+i[2]] for i in itog], key=lambda x: x[1]))


# data_token: Dataset = last_data("COTIUSDT", "4h", "1440")
# res_now: float = round(data_token.close_price[-1] / data_token.open_price[-1] * 100 - 100, 2)
# res_past: float = round(data_token.high_price[-1] / data_token.close_price[-2] * 100 - 100, 2)
# print(res_past)

# import numpy as np
# import pandas as pd
# import matplotlib.pyplot as plt
# import yfinance as yf
# from sklearn.preprocessing import MinMaxScaler
# from keras.layers import Dense, Dropout, LSTM
# from keras.models import Sequential
#
# start = "2023-12-25"
# end = "2024-02-13"
# stock = "CHR-USD"
#
# data = yf.download(stock, start, end, interval="15m")
# data.reset_index(inplace=True)
#
# data.dropna(inplace=True)
#
# data_train = pd.DataFrame(data.Close[0:int(len(data)*0.75)])
# data_test = pd.DataFrame(data.Close[int(len(data)*0.75):len(data)])
#
# scaler = MinMaxScaler(feature_range=(0,1))
# data_train_scale = scaler.fit_transform(data_train)
# x = []
# y = []
# for i in range(100, data_train_scale.shape[0]):
#     x.append(data_train_scale[i-100:i])
#     y.append(data_train_scale[i, 0])
#
# x, y = np.array(x), np.array(y)
#
#
# model = Sequential()
# model.add(LSTM(units=50, activation="relu", return_sequences=True, input_shape=(x.shape[1], 1)))
# model.add(Dropout(0.2))
#
# model.add(LSTM(units=60, activation="relu", return_sequences=True))
# model.add(Dropout(0.3))
#
# model.add(LSTM(units=80, activation="relu", return_sequences=True))
# model.add(Dropout(0.4))
#
# model.add(LSTM(units=120, activation="relu"))
# model.add(Dropout(0.2))
#
# model.add(Dense(units=1))
#
# model.compile(optimizer="adam", loss="mean_squared_error")
# model.fit(x, y, epochs=50, batch_size=32, verbose=1)
# model.save('15min_CHR.h5')
# #model = keras.models.load_model('16_model_2.h5')
# pas_100_days = data_train.tail(100)
# data_test = pd.concat([pas_100_days, data_test], ignore_index=True)
# data_test_scale = scaler.fit_transform(data_test)
# x = []
# y = []
#
# for i in range(100, data_test_scale.shape[0]):
#     x.append(data_train_scale[i-100:i])
#     y.append(data_train_scale[i, 0])
#
# x, y = np.array(x), np.array(y)
# y_predict = model.predict(x)
#
# scale = 1/scaler.scale_
# y_predict = y_predict * scale
# y = y * scale
# plt.figure(figsize=(10, 8))
# plt.plot(y_predict, "r", label="Predicted Price")
# plt.plot(y, "g", label="Original Price")
# plt.xlabel("Time")
# plt.ylabel("Price")
# plt.legend()
# plt.show()
#equal("jopa_4h", -1.0, 1.5, -3.2, 2.2, 2.2, 5.3)

