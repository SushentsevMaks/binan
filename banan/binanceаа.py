import time
from datetime import datetime
from decimal import Decimal, ROUND_FLOOR
from threading import Thread

import pymysql
import requests
from binance.client import Client, AsyncClient
from binance.exceptions import BinanceAPIException
import keys
import pandas as pd
import telebot
from tradingview_ta import TA_Handler, Interval, Exchange

import re

from binan.banan.sql_request import get_crypto, equal, sql_del

telega_token = "5926919919:AAFCHFocMt_pdnlAgDo-13wLe4h_tHO0-GE"
import asyncio

client = Client(keys.api_key, keys.api_secret)

trading_pairss = ['1INCHUSDT', 'AAVEUSDT', 'ACAUSDT', 'ACHUSDT', 'ACMUSDT', 'ADAUSDT', 'ADXUSDT', 'AERGOUSDT',
                  'AGIXUSDT', 'AGLDUSDT', 'AKROUSDT', 'ALCXUSDT', 'ALGOUSDT', 'ALICEUSDT', 'ALPACAUSDT', 'ALPHAUSDT',
                  'ALPINEUSDT', 'AMBUSDT', 'AMPUSDT', 'ANKRUSDT', 'ANTUSDT', 'APEUSDT', 'API3USDT', 'APTUSDT',
                  'ARBUSDT', 'ARDRUSDT', 'ARKMUSDT', 'ARPAUSDT', 'ARUSDT', 'ASRUSDT', 'ASTRUSDT', 'ASTUSDT', 'ATAUSDT',
                  'ATMUSDT', 'ATOMUSDT', 'AUCTIONUSDT', 'AUDIOUSDT', 'AVAUSDT', 'AVAXUSDT', 'AXSUSDT', 'BADGERUSDT',
                  'BAKEUSDT', 'BALUSDT', 'BANDUSDT', 'BARUSDT', 'BATUSDT', 'BCHUSDT', 'BELUSDT', 'BETAUSDT', 'BETHUSDT',
                  'BICOUSDT', 'BIFIUSDT', 'BLZUSDT', 'BNTUSDT', 'BNXUSDT', 'BONDUSDT', 'BSWUSDT', 'BTSUSDT', 'YGGUSDT',
                  'ZECUSDT', 'ZENUSDT', 'ZILUSDT', 'ZRXUSDT', 'BURGERUSDT', 'BUSDUSDT', 'C98USDT', 'CAKEUSDT',
                  'CELOUSDT', 'CELRUSDT', 'CFXUSDT', 'CHESSUSDT', 'CHRUSDT', 'CHZUSDT', 'CITYUSDT', 'CKBUSDT',
                  'CLVUSDT', 'COMBOUSDT', 'COMPUSDT', 'COSUSDT', 'COTIUSDT', 'CRVUSDT', 'CTKUSDT', 'CTSIUSDT',
                  'CTXCUSDT', 'CVCUSDT', 'CVPUSDT', 'CVXUSDT', 'CYBERUSDT', 'DARUSDT', 'DASHUSDT', 'DATAUSDT',
                  'DCRUSDT', 'DEGOUSDT', 'DENTUSDT', 'DEXEUSDT', 'DFUSDT', 'DGBUSDT', 'DIAUSDT', 'DOCKUSDT', 'DODOUSDT',
                  'DOGEUSDT', 'DOTUSDT', 'DREPUSDT', 'DUSKUSDT', 'DYDXUSDT', 'EDUUSDT', 'EGLDUSDT', 'ELFUSDT',
                  'ENJUSDT', 'ENSUSDT', 'EPXUSDT', 'ERNUSDT', 'ETCUSDT', 'EURUSDT', 'FARMUSDT', 'FDUSDUSDT', 'FETUSDT',
                  'FIDAUSDT', 'FILUSDT', 'FIOUSDT', 'FIROUSDT', 'FISUSDT', 'FLMUSDT', 'FLOKIUSDT', 'FLOWUSDT',
                  'FLUXUSDT', 'FORTHUSDT', 'FORUSDT', 'FRONTUSDT', 'FTMUSDT', 'FUNUSDT', 'FXSUSDT', 'GALAUSDT',
                  'GALUSDT', 'GASUSDT', 'GBPUSDT', 'GHSTUSDT', 'GLMRUSDT', 'GLMUSDT', 'GMTUSDT', 'GMXUSDT', 'GNOUSDT',
                  'GNSUSDT', 'GRTUSDT', 'GTCUSDT', 'HARDUSDT', 'HBARUSDT', 'HFTUSDT', 'HIFIUSDT', 'HIGHUSDT',
                  'HIVEUSDT', 'HOOKUSDT', 'HOTUSDT', 'ICPUSDT', 'ICXUSDT', 'IDEXUSDT', 'IDUSDT', 'ILVUSDT', 'IMXUSDT',
                  'INJUSDT', 'IOSTUSDT', 'IOTAUSDT', 'IOTXUSDT', 'IRISUSDT', 'JASMYUSDT', 'JOEUSDT', 'JSTUSDT',
                  'JUVUSDT', 'KAVAUSDT', 'KDAUSDT', 'KEYUSDT', 'KLAYUSDT', 'KMDUSDT', 'KNCUSDT', 'KP3RUSDT', 'KSMUSDT',
                  'LAZIOUSDT', 'LDOUSDT', 'LEVERUSDT', 'LINAUSDT', 'LINKUSDT', 'LITUSDT', 'LOKAUSDT', 'LOOMUSDT',
                  'LPTUSDT', 'LQTYUSDT', 'LRCUSDT', 'LSKUSDT', 'LTCUSDT', 'LTOUSDT', 'LUNAUSDT', 'LUNCUSDT',
                  'MAGICUSDT', 'MANAUSDT', 'MASKUSDT', 'MATICUSDT', 'MAVUSDT', 'MBLUSDT', 'MBOXUSDT', 'MCUSDT',
                  'MDTUSDT', 'MDXUSDT', 'MINAUSDT', 'MKRUSDT', 'MLNUSDT', 'MOBUSDT', 'MOVRUSDT', 'MTLUSDT', 'MULTIUSDT',
                  'NEARUSDT', 'NEOUSDT', 'NEXOUSDT', 'NKNUSDT', 'NMRUSDT', 'NULSUSDT', 'OAXUSDT', 'OCEANUSDT',
                  'OGNUSDT', 'OGUSDT', 'OMGUSDT', 'OMUSDT', 'ONEUSDT', 'ONGUSDT', 'ONTUSDT', 'OOKIUSDT', 'OPUSDT',
                  'ORNUSDT', 'OSMOUSDT', 'OXTUSDT', 'PAXGUSDT', 'PENDLEUSDT', 'PEOPLEUSDT', 'PERLUSDT', 'PERPUSDT',
                  'PHAUSDT', 'PHBUSDT', 'PLAUSDT', 'PNTUSDT', 'POLSUSDT', 'POLYXUSDT', 'PONDUSDT', 'PORTOUSDT',
                  'POWRUSDT', 'PROMUSDT', 'PROSUSDT', 'PSGUSDT', 'PUNDIXUSDT', 'PYRUSDT', 'QIUSDT', 'QKCUSDT',
                  'QNTUSDT', 'QTUMUSDT', 'QUICKUSDT', 'RADUSDT', 'RAREUSDT', 'RAYUSDT', 'RDNTUSDT', 'REEFUSDT',
                  'REIUSDT', 'RENUSDT', 'REQUSDT', 'RIFUSDT', 'RLCUSDT', 'RNDRUSDT', 'ROSEUSDT', 'RPLUSDT', 'RSRUSDT',
                  'RUNEUSDT', 'RVNUSDT', 'SANDUSDT', 'SANTOSUSDT', 'SCRTUSDT', 'SCUSDT', 'SEIUSDT', 'SFPUSDT',
                  'SHIBUSDT', 'SKLUSDT', 'SLPUSDT', 'SNTUSDT', 'SNXUSDT', 'SOLUSDT', 'SPELLUSDT', 'SSVUSDT',
                  'STEEMUSDT', 'STGUSDT', 'STMXUSDT', 'STORJUSDT', 'STPTUSDT', 'STRAXUSDT', 'STXUSDT', 'SUIUSDT',
                  'SUNUSDT', 'SUPERUSDT', 'SUSHIUSDT', 'SXPUSDT', 'SYNUSDT', 'SYSUSDT', 'TFUELUSDT', 'THETAUSDT',
                  'TKOUSDT', 'TLMUSDT', 'TOMOUSDT', 'TRBUSDT', 'TROYUSDT', 'TRUUSDT', 'TRXUSDT', 'TUSDT', 'TUSDUSDT',
                  'TVKUSDT', 'TWTUSDT', 'UFTUSDT', 'UMAUSDT', 'UNFIUSDT', 'UNIUSDT', 'USDCUSDT', 'USDPUSDT', 'USTCUSDT',
                  'UTKUSDT', 'VETUSDT', 'VGXUSDT', 'VIBUSDT', 'VIDTUSDT', 'VITEUSDT', 'VOXELUSDT', 'VTHOUSDT',
                  'WANUSDT', 'WAVESUSDT', 'WAXPUSDT', 'WBETHUSDT', 'WBTCUSDT', 'WINGUSDT', 'WINUSDT', 'WLDUSDT',
                  'WNXMUSDT', 'WOOUSDT', 'WRXUSDT', 'WTCUSDT', 'XECUSDT', 'XEMUSDT', 'XLMUSDT', 'XMRUSDT', 'XNOUSDT',
                  'XRPUSDT', 'XVGUSDT', 'XVSUSDT', 'YFIUSDT']

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

trading_pairs_fut = ['LEVERUSDT', 'USDCUSDT', 'AVAXUSDT', 'ATAUSDT', 'ACHUSDT', 'ARPAUSDT', 'CYBERUSDT', 'CHZUSDT',
                     'RNDRUSDT',
                     'MASKUSDT', 'MTLUSDT', 'XTZUSDT', 'BTCUSDT', 'XRPUSDT', 'CFXUSDT', 'ASTRUSDT', 'NEARUSDT',
                     'AGIXUSDT',
                     'API3USDT', 'EOSUSDT', 'IDEXUSDT', 'WLDUSDT', 'RAYUSDT', 'THETAUSDT', 'FTMUSDT', 'XMRUSDT',
                     'BATUSDT',
                     'ENSUSDT', 'FILUSDT', 'ALGOUSDT', 'SEIUSDT', 'STGUSDT', 'ROSEUSDT', 'INJUSDT', 'TUSDT', 'SOLUSDT',
                     'HIGHUSDT',
                     'YGGUSDT', 'TRBUSDT', 'UNIUSDT', 'FLMUSDT', 'LQTYUSDT', 'ARKMUSDT', 'YFIUSDT', 'PEOPLEUSDT',
                     'IOSTUSDT',
                     'COMBOUSDT', 'MATICUSDT', 'DUSKUSDT', 'JASMYUSDT', 'CTKUSDT', 'TLMUSDT', 'WOOUSDT', 'NEOUSDT',
                     'KAVAUSDT',
                     'MAVUSDT', 'PHBUSDT', 'CKBUSDT', 'CVCUSDT', 'IOTAUSDT', 'SFPUSDT', 'COTIUSDT', 'CELOUSDT',
                     'MINAUSDT',
                     'LTCUSDT', 'NKNUSDT', 'FLOWUSDT', 'ETCUSDT', 'GMTUSDT', 'GTCUSDT', 'SNXUSDT', 'TRXUSDT',
                     'EGLDUSDT',
                     'CELRUSDT', 'IDUSDT', 'GALAUSDT', 'LITUSDT', 'ADAUSDT', 'CRVUSDT', 'DYDXUSDT', 'DOGEUSDT',
                     'GALUSDT',
                     'FETUSDT', 'MKRUSDT', 'CTSIUSDT', 'ATOMUSDT', 'ICPUSDT', 'AUDIOUSDT', 'RLCUSDT', 'LDOUSDT',
                     'AMBUSDT',
                     'OCEANUSDT', 'RDNTUSDT', 'STMXUSDT', 'OMGUSDT', 'APTUSDT', 'HOOKUSDT', 'STORJUSDT', 'CVXUSDT',
                     'ONTUSDT',
                     'BLZUSDT', 'PERPUSDT', 'SKLUSDT', 'LRCUSDT', 'BNBUSDT', 'BCHUSDT', 'EDUUSDT', 'SPELLUSDT',
                     '1INCHUSDT',
                     'DENTUSDT', 'ZECUSDT', 'CHRUSDT', 'TOMOUSDT', 'KLAYUSDT', 'XEMUSDT', 'RSRUSDT', 'RENUSDT',
                     'ICXUSDT',
                     'BANDUSDT', 'GMXUSDT', 'ARBUSDT', 'KNCUSDT', 'DASHUSDT', 'TRUUSDT', 'HBARUSDT', 'RUNEUSDT',
                     'SCUSDT',
                     'DGBUSDT', 'BAKEUSDT', 'SUSHIUSDT', 'HOTUSDT', 'RADUSDT', 'BELUSDT', 'XLMUSDT', 'BTSUSDT',
                     'QNTUSDT',
                     'MAGICUSDT', 'VETUSDT', 'APEUSDT', 'DARUSDT', 'LINAUSDT', 'NMRUSDT', 'MDTUSDT', 'OPUSDT',
                     'ANKRUSDT',
                     'SANDUSDT', 'ONEUSDT', 'ARUSDT', 'SXPUSDT', 'ZILUSDT', 'OXTUSDT', 'BALUSDT', 'IMXUSDT', 'DOTUSDT',
                     'XVGUSDT',
                     'LPTUSDT', 'WAVESUSDT', 'ZENUSDT', 'BNXUSDT', 'ALPHAUSDT', 'COMPUSDT', 'ZRXUSDT', 'SSVUSDT',
                     'UMAUSDT',
                     'PENDLEUSDT', 'AGLDUSDT', 'UNFIUSDT', 'LINKUSDT', 'ALICEUSDT', 'OGNUSDT', 'REEFUSDT', 'BNTUSDT',
                     'GRTUSDT',
                     'HFTUSDT', 'STXUSDT', 'IOTXUSDT', 'ANTUSDT', 'C98USDT', 'AXSUSDT', 'AAVEUSDT', 'ENJUSDT',
                     'RVNUSDT',
                     'MANAUSDT', 'XVSUSDT', 'FXSUSDT', 'SUIUSDT', 'KSMUSDT', 'JOEUSDT', 'KEYUSDT', 'ETHUSDT',
                     'QTUMUSDT']

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

# one = ['1INCHUSDT', 'AAVEUSDT', 'ACAUSDT', 'ACHUSDT', 'ACMUSDT', 'ADAUSDT', 'ADXUSDT', 'AERGOUSDT', 'AGIXUSDT',
#        'AGLDUSDT', 'AKROUSDT', 'ALCXUSDT', 'ALGOUSDT', 'ALICEUSDT', 'ALPACAUSDT', 'ALPHAUSDT', 'ALPINEUSDT', 'AMBUSDT',
#        'AMPUSDT', 'ANKRUSDT', 'ANTUSDT', 'APEUSDT', 'API3USDT']
#
# two = ['APTUSDT', 'ARBUSDT', 'ARDRUSDT', 'ARKMUSDT', 'ARPAUSDT', 'ARUSDT', 'ASRUSDT', 'ASTRUSDT', 'ASTUSDT', 'ATAUSDT',
#        'ATMUSDT', 'ATOMUSDT', 'AUCTIONUSDT', 'AUDIOUSDT', 'AVAUSDT', 'AVAXUSDT', 'AXSUSDT', 'BADGERUSDT', 'BAKEUSDT',
#        'BALUSDT', 'BANDUSDT', 'BARUSDT', 'BATUSDT']
#
# three = ['BCHUSDT', 'BELUSDT', 'BETAUSDT', 'BETHUSDT', 'BICOUSDT', 'BIFIUSDT', 'BLZUSDT', 'BNTUSDT', 'BNXUSDT',
#          'BONDUSDT', 'BSWUSDT', 'BTSUSDT', 'YGGUSDT', 'ZECUSDT', 'ZENUSDT', 'ZILUSDT', 'ZRXUSDT', 'BURGERUSDT',
#          'C98USDT', 'CAKEUSDT', 'CELOUSDT', 'CELRUSDT', 'CFXUSDT', 'CHESSUSDT', 'CHRUSDT', 'CHZUSDT']
#
# four = ['CITYUSDT', 'CKBUSDT', 'CLVUSDT', 'COMBOUSDT', 'COMPUSDT', 'COSUSDT', 'COTIUSDT', 'CRVUSDT', 'CTKUSDT',
#         'CTSIUSDT', 'CTXCUSDT', 'CVCUSDT', 'CVPUSDT', 'CVXUSDT', 'CYBERUSDT', 'DARUSDT', 'DASHUSDT', 'DATAUSDT',
#         'DCRUSDT', 'DEGOUSDT', 'DENTUSDT', 'DEXEUSDT', 'DFUSDT']
#
# five = ['DGBUSDT', 'DIAUSDT', 'DOCKUSDT', 'DODOUSDT', 'DOGEUSDT', 'DOTUSDT', 'DREPUSDT', 'DUSKUSDT', 'DYDXUSDT',
#         'EDUUSDT', 'EGLDUSDT', 'ELFUSDT', 'ENJUSDT', 'ENSUSDT', 'EPXUSDT', 'ERNUSDT', 'ETCUSDT', 'FARMUSDT',
#         'FETUSDT', 'FIDAUSDT']
#
# six = ['FILUSDT', 'FIOUSDT', 'FIROUSDT', 'FISUSDT', 'FLMUSDT', 'FLOKIUSDT', 'FLOWUSDT', 'FLUXUSDT', 'FORTHUSDT',
#        'FORUSDT', 'FRONTUSDT', 'FTMUSDT', "FTTUSDT", 'FUNUSDT', 'FXSUSDT', 'GALAUSDT', 'GALUSDT', 'GASUSDT', 'GHSTUSDT',
#        'GLMRUSDT', 'GLMUSDT', 'GMTUSDT', 'GMXUSDT']
#
# seven = ['GNOUSDT', 'GNSUSDT', 'GRTUSDT', 'GTCUSDT', 'HARDUSDT', 'HBARUSDT', 'HFTUSDT', 'HIFIUSDT', 'HIGHUSDT',
#          'HIVEUSDT', 'HOOKUSDT', 'HOTUSDT', 'ICPUSDT', 'ICXUSDT', 'IDEXUSDT', 'IDUSDT', 'ILVUSDT', 'IMXUSDT', 'INJUSDT',
#          'IOSTUSDT', 'IOTAUSDT', 'IOTXUSDT', 'IRISUSDT']
#
# eight = ['JASMYUSDT', 'JOEUSDT', 'JSTUSDT', 'JUVUSDT', 'KAVAUSDT', 'KDAUSDT', 'KEYUSDT', 'KLAYUSDT', 'KMDUSDT',
#          'KNCUSDT', 'KP3RUSDT', 'KSMUSDT', 'LAZIOUSDT', 'LDOUSDT', 'LEVERUSDT', 'LINAUSDT', 'LINKUSDT', 'LITUSDT',
#          'LOKAUSDT', 'LOOMUSDT', 'LPTUSDT', 'LQTYUSDT', 'LRCUSDT']
#
# nine = ['LSKUSDT', 'LTCUSDT', 'LTOUSDT', 'LUNAUSDT', 'LUNCUSDT', 'MAGICUSDT', 'MANAUSDT', 'MASKUSDT', 'MATICUSDT',
#         'MAVUSDT', 'MBLUSDT', 'MBOXUSDT', 'MCUSDT', 'MDTUSDT', 'MDXUSDT', 'MINAUSDT', 'MKRUSDT', 'MLNUSDT', 'MOBUSDT',
#         'MOVRUSDT', 'MTLUSDT', 'MULTIUSDT', 'NEARUSDT']
#
# ten = ['NEOUSDT', 'NEXOUSDT', 'NKNUSDT', 'NMRUSDT', 'NULSUSDT', 'OAXUSDT', 'OCEANUSDT', 'OGNUSDT', 'OGUSDT', 'OMGUSDT',
#        'OMUSDT', 'ONEUSDT', 'ONGUSDT', 'ONTUSDT', 'OOKIUSDT', 'OPUSDT', 'ORNUSDT', 'OSMOUSDT', 'OXTUSDT', 'PAXGUSDT',
#        'PENDLEUSDT', 'PEOPLEUSDT']
#
# eleven = ['PERLUSDT', 'PERPUSDT', 'PHAUSDT', 'PHBUSDT', 'PLAUSDT', 'PNTUSDT', 'POLSUSDT', 'POLYXUSDT', 'PONDUSDT',
#           'PORTOUSDT', 'POWRUSDT', 'PROMUSDT', 'PROSUSDT', 'PSGUSDT', 'PUNDIXUSDT', 'PYRUSDT', 'QIUSDT', 'QKCUSDT',
#           'QNTUSDT', 'QTUMUSDT', 'QUICKUSDT', 'RADUSDT', 'RAREUSDT']
#
# twelve = ['RAYUSDT', 'RDNTUSDT', 'REEFUSDT', 'REIUSDT', 'RENUSDT', 'REQUSDT', 'RIFUSDT', 'RLCUSDT', 'RNDRUSDT',
#           'ROSEUSDT', 'RPLUSDT', 'RSRUSDT', 'RUNEUSDT', 'RVNUSDT', 'SANDUSDT', 'SANTOSUSDT', 'SCRTUSDT', 'SCUSDT',
#           'SEIUSDT', 'SFPUSDT', 'SHIBUSDT', 'SKLUSDT', 'SLPUSDT']
#
# thirteenth = ['SNTUSDT', 'SNXUSDT', 'SOLUSDT', 'SPELLUSDT', 'SSVUSDT', 'STEEMUSDT', 'STGUSDT', 'STMXUSDT', 'STORJUSDT',
#               'STPTUSDT', 'STRAXUSDT', 'STXUSDT', 'SUIUSDT', 'SUNUSDT', 'SUPERUSDT', 'SUSHIUSDT', 'SXPUSDT', 'SYNUSDT',
#               'SYSUSDT', 'TFUELUSDT', 'THETAUSDT', 'TKOUSDT', 'TLMUSDT']
#
# fourteenth = ['TOMOUSDT', 'TRBUSDT', 'TROYUSDT', 'TRUUSDT', 'TRXUSDT', 'TUSDT', 'TVKUSDT', 'TWTUSDT',
#               'UFTUSDT', 'UMAUSDT', 'UNFIUSDT', 'UNIUSDT', 'USTCUSDT', 'UTKUSDT', 'VETUSDT',
#               'VGXUSDT', 'VIBUSDT', 'VIDTUSDT', 'VITEUSDT', 'VOXELUSDT']
#
# fifteenth = ['VTHOUSDT', 'WANUSDT', 'WAVESUSDT', 'WAXPUSDT', 'WBETHUSDT', 'WINGUSDT', 'WINUSDT', 'WLDUSDT', 'WNXMUSDT',
#              'WOOUSDT', 'WRXUSDT', 'WTCUSDT', 'XECUSDT', 'XEMUSDT', 'XLMUSDT', 'XMRUSDT', 'XNOUSDT', 'XRPUSDT',
#              'XVGUSDT', 'XVSUSDT', 'YFIUSDT']

one = ['1INCHUSDT', 'AAVEUSDT', 'ACHUSDT', 'ACMUSDT', 'ADAUSDT', 'MANTAUSDT']

onegop = ['AERGOUSDT', 'AGIXUSDT', 'AGLDUSDT', 'ALCXUSDT', 'ALGOUSDT']

onedop = ['ALICEUSDT', 'ALPACAUSDT', 'ALPHAUSDT', 'ALPINEUSDT', 'AMBUSDT']

onemop = ['AMPUSDT', 'ANKRUSDT', 'ANTUSDT', 'APEUSDT', 'API3USDT', 'AIUSDT']

two = ['APTUSDT', 'ARBUSDT', 'ARDRUSDT', 'ARKMUSDT', 'ARPAUSDT', 'XAIUSDT']

twogop = ['ARUSDT', 'ASRUSDT', 'ATMUSDT', 'ATOMUSDT', 'AUCTIONUSDT']

twodop = ['AUDIOUSDT', 'AVAXUSDT', 'AXSUSDT', 'BADGERUSDT', 'BAKEUSDT']

twomop = ['BALUSDT', 'BANDUSDT', 'BARUSDT', 'BATUSDT', 'ARKUSDT']

three = ["BEAMXUSDT", 'BCHUSDT', 'BELUSDT', 'BETAUSDT', 'BICOUSDT', 'NFPUSDT']

threegop = ['BIFIUSDT', 'BLZUSDT', 'BNXUSDT', 'BONDUSDT', 'YGGUSDT']

threedop = ['ZECUSDT', 'ZENUSDT', 'ZILUSDT', 'ZRXUSDT', 'BURGERUSDT', 'C98USDT', 'CAKEUSDT']

threemop = ['CELRUSDT', 'CFXUSDT', 'CHESSUSDT', 'CHRUSDT', 'CHZUSDT']

four = ['CITYUSDT', 'CKBUSDT', 'CLVUSDT', 'COMPUSDT', 'COTIUSDT']

fourgop = ['CRVUSDT', 'CTSIUSDT', 'CTXCUSDT', 'CVCUSDT', 'DYMUSDT']

fourdop = ['CVPUSDT', 'CVXUSDT', 'CYBERUSDT', 'DARUSDT', 'DASHUSDT', 'DATAUSDT']

fourmop = ['DCRUSDT', 'DEGOUSDT', 'DENTUSDT', 'DEXEUSDT', 'DFUSDT']

five = ['DIAUSDT', 'DODOUSDT', 'DOGEUSDT', 'DOTUSDT', 'DREPUSDT', 'ALTUSDT']

fivegop = ['DUSKUSDT', 'DYDXUSDT', 'EDUUSDT', 'EGLDUSDT', 'ELFUSDT']

fivedop = ['ENJUSDT', 'ENSUSDT', 'EPXUSDT', 'ETCUSDT', 'RONINUSDT']

fivemop = ['FARMUSDT', 'FETUSDT', 'FIDAUSDT', 'GFTUSDT', 'PYTHUSDT']

six = ["FTTUSDT", 'FILUSDT', 'FIOUSDT', 'FIROUSDT', 'FISUSDT']

sixgop = ['FLOKIUSDT', 'FLUXUSDT', 'FORTHUSDT', 'FORUSDT', 'FRONTUSDT']

sixdop = ['FTMUSDT', 'FUNUSDT', 'FXSUSDT', 'GALAUSDT', 'GALUSDT']

sixmop = ['GLMRUSDT', 'GLMUSDT', 'GMTUSDT', 'GMXUSDT', 'GASUSDT']

seven = ['GNSUSDT', 'GRTUSDT', 'HARDUSDT', 'HBARUSDT', 'HFTUSDT']

sevengop = ['HIGHUSDT', 'HIVEUSDT', 'HOOKUSDT', 'HOTUSDT', 'ICPUSDT']

sevendop = ['ICXUSDT', 'IDEXUSDT', 'IDUSDT', 'ILVUSDT', 'IMXUSDT']

sevenmop = ['INJUSDT', 'IOTAUSDT', 'IOTXUSDT', 'IRISUSDT', 'STMXUSDT']

eight = ['JASMYUSDT', 'JOEUSDT', 'JSTUSDT', 'JUVUSDT', 'KAVAUSDT']

eightgop = ['KEYUSDT', 'KLAYUSDT', 'KMDUSDT', 'KP3RUSDT', 'KSMUSDT']

eightdop = ['LAZIOUSDT', 'LDOUSDT', 'LEVERUSDT', 'LINAUSDT', 'LINKUSDT']

eightmop = ['LITUSDT', 'LOKAUSDT', 'LOOMUSDT', 'LQTYUSDT', 'LRCUSDT']

nine = ['LSKUSDT', 'LTCUSDT', 'LUNAUSDT', 'LUNCUSDT', 'MAGICUSDT', 'MANAUSDT']

ninegop = ['MASKUSDT', 'MATICUSDT', 'MAVUSDT', 'MBLUSDT', 'MBOXUSDT']

ninedop = ['MDTUSDT', 'MINAUSDT', 'MKRUSDT', 'MLNUSDT', 'MOBUSDT']

ninemop = ['MOVRUSDT', 'MTLUSDT', 'MULTIUSDT', 'NEARUSDT', 'MEMEUSDT']

ten = ['NEOUSDT', 'NKNUSDT', 'NMRUSDT', 'NULSUSDT', 'OAXUSDT', 'OCEANUSDT']

tengop = ['OGNUSDT', 'OGUSDT', 'OMGUSDT', 'OMUSDT', 'ONEUSDT', 'ORDIUSDT']

tendop = ['ONGUSDT', 'ONTUSDT', 'OOKIUSDT', 'OPUSDT', 'ORNUSDT']

tenmop = ['OSMOUSDT', 'OXTUSDT', 'PENDLEUSDT', 'PEOPLEUSDT', 'NTRNUSDT']

eleven = ['PERLUSDT', 'PERPUSDT', 'PHAUSDT', 'PHBUSDT', 'PNTUSDT']

elevengop = ['POLSUSDT', 'POLYXUSDT', 'PORTOUSDT', 'POWRUSDT', 'PROMUSDT']

elevendop = ['PROSUSDT', 'PSGUSDT', 'PUNDIXUSDT', 'PYRUSDT', 'RIFUSDT']

elevenmop = ['QKCUSDT', 'QTUMUSDT', 'QUICKUSDT', 'RADUSDT', 'RLCUSDT']

twelve = ['RAYUSDT', 'RDNTUSDT', 'REEFUSDT', 'REIUSDT', 'RENUSDT', 'REQUSDT']

twelvegop = ['RNDRUSDT', 'ROSEUSDT', 'RPLUSDT', 'RSRUSDT', 'RUNEUSDT']

twelvedop = ['RVNUSDT', 'SANDUSDT', 'SANTOSUSDT', 'SCRTUSDT', 'SCUSDT']

twelvemop = ['SEIUSDT', 'SFPUSDT', 'SHIBUSDT', 'SKLUSDT', 'SLPUSDT']

thirteenth = ['SNTUSDT', 'SNXUSDT', 'SOLUSDT', 'SPELLUSDT', 'SSVUSDT', 'STEEMUSDT', 'STGUSDT']

thirteenthgop = ['STORJUSDT', 'STPTUSDT', 'STRAXUSDT', 'STXUSDT', 'SUIUSDT']

thirteenthdop = ['SUPERUSDT', 'SUSHIUSDT', 'SXPUSDT', 'SYNUSDT', 'SYSUSDT']

thirteenthmop = ['TFUELUSDT', 'THETAUSDT', 'TKOUSDT', 'TLMUSDT', 'TIAUSDT']

fourteenth = ['TOMOUSDT', 'TRBUSDT', 'TROYUSDT', 'TRUUSDT', 'TRXUSDT', 'TUSDT']

fourteenthgop = ['TVKUSDT', 'TWTUSDT', 'UFTUSDT', 'UMAUSDT', 'UNFIUSDT']

fourteenthdop = ['UNIUSDT', 'USTCUSDT', 'VETUSDT', 'VGXUSDT', 'XVGUSDT', "CREAMUSDT"]

fourteenthmop = ['VIBUSDT', 'VIDTUSDT', 'VITEUSDT', 'VOXELUSDT', 'YFIUSDT']

fifteenth = ['WANUSDT', 'WAVESUSDT', 'WAXPUSDT', 'WBETHUSDT', 'JUPUSDT']

fifteenthgop = ['WLDUSDT', 'WNXMUSDT', 'WOOUSDT', 'WRXUSDT', 'WTCUSDT']

fifteenthdop = ['XECUSDT', 'XEMUSDT', 'XLMUSDT', 'XMRUSDT', "NTRNUSDT", 'XRPUSDT']

izg = ["HIFIUSDT", 'QIUSDT']

x = one + two + three + four + five + six + seven + eight + nine + ten + eleven + twelve + thirteenth + fourteenth + fifteenth + izg + \
    onedop + twodop + threedop + fourdop + fivedop + sixdop + sevendop + eightdop + ninedop + tendop + elevendop + twelvedop + \
    thirteenthdop + fourteenthdop + fifteenthdop

# url = "https://api.binance.com/api/v3/exchangeInfo"
# response = requests.get(url)
# data = response.json()
# symbols = [symbol["symbol"] for symbol in data["symbols"] if symbol['symbol'][-4:] == "USDT"]
# s = []
# for i in symbols:
#     if i not in x:
#         s.append(i)
# print(s[::-1])


def top_coin(trading_pairs: list):
    for name_cript_check in trading_pairs:
        try:
            # print(name_cript_check)
            # print(last_data(name_cript_check, "3m", "300"))
            data_token: Dataset = last_data(name_cript_check, "15m", "600")
            volume_per_5h = sum([int(i * data_token.high_price[-1]) for i in data_token.volume]) / len(
                data_token.volume)
            res = round(data_token.close_price[-1] / data_token.open_price[-1] * 100 - 100, 2)

            # print(name_cript_check)

            if 2 > res:
                buy_qty = round(11 / data_token.close_price[-1], 1)

                telebot.TeleBot(telega_token).send_message(chat_id, f"RABOTAEM - {name_cript_check}\n"
                                                                    f"Количество покупаемого - {buy_qty}, Цена - {data_token.high_price[-1]}\n"
                                                                    f"Цены {data_token.high_price[-9:]}\n"
                                                                    f"Объемы {int(volume_per_5h)}\n"
                                                                    f"Цена упала на {res}%\n")
        except Exception as e:
            print(e)


from binance import ThreadedWebsocketManager

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
# equal('WOOUSDT', -4.09, 1, 11.37)
# equal('FRONTUSDT', -5.91, 1, -0.76)
# equal('UNIUSDT', -7.19, 1, -16.96)
# equal('SCUSDT', 0, 1, 100)
#
# bd_cript = get_crypto()
# '''Проверка на наилучший объект и работа с ним дальше'''
# reit_bd_cript = []
#
# for j in bd_cript:
#     reit_bd_cript.append([j['name_cript'], j["res"], j["price_change_percent_24h"]])
# print(sorted(reit_bd_cript, key=lambda x: x[2]))
# print(sorted(reit_bd_cript, key=lambda x: x[2])[0][0])

d =  [['PYTHUSDT', -6.59, 7.53], ['PYTHUSDT', -6.4, -12.21], ['CKBUSDT', -5.52, -13.18], ['XAIUSDT', -5.46, -7.92], ['BEAMXUSDT', -4.02, -3.32]]
k = [i[0] for i in sorted(d, key=lambda x: x[1])]
m = [i[0] for i in sorted(d, key=lambda x: x[2])]
#[['PYTHUSDT', -8.61, 27.21], ['TFUELUSDT', -7.08, 7.81], ['XVGUSDT', -6.37, -0.75], ['HOTUSDT', -6.2, 10.28]]
#[['XVGUSDT', -6.37, -0.75], ['TFUELUSDT', -7.08, 7.81], ['HOTUSDT', -6.2, 10.28], ['PYTHUSDT', -8.61, 27.21]]
itog = []
for i in k:
    itog.append([i, k.index(i), m.index(i)])
print(sorted([[i[0], i[1]+i[2]] for i in itog], key=lambda x: x[1]))
all_work_crypt = sorted([[i[0], i[1]+i[2]] for i in itog], key=lambda x: x[1])[1:]

for i in all_work_crypt:
    data_token: Dataset = last_data(i[0], "4h", "1440")
    res_now: float = round(data_token.close_price[-1] / data_token.open_price[-1] * 100 - 100, 2)
    res_past: float = round(data_token.high_price[-1] / data_token.close_price[-2] * 100 - 100, 2)
    print(i[0], res_now, res_past)
    if res_now < 0 and res_past < 0.8:
        print(i[0], "proshel")
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

# data_token = last_data("EPXUSDT", "4h", "1440")
# price_change_percent_24h: float = round(((data_token.close_price[-1] / data_token.close_price[0]) * 100) - 100, 2)
# print(data_token.close_price[-1], data_token.close_price[0])
# print(price_change_percent_24h)