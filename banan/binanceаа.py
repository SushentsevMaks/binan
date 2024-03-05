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

onemop = ['AMPUSDT', 'ANKRUSDT', 'APEUSDT', 'API3USDT', 'AIUSDT']

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

ninegop = ['MASKUSDT', 'MATICUSDT', 'MAVUSDT', 'MBLUSDT', 'MBOXUSDT', "COMBOUSDT"]

ninedop = ['MDTUSDT', 'MINAUSDT', 'MKRUSDT', 'MLNUSDT', 'MOBUSDT', 'IQUSDT']

ninemop = ['MOVRUSDT', 'MTLUSDT', 'NEARUSDT', 'MEMEUSDT', 'PIVXUSDT']

ten = ['NEOUSDT', 'NKNUSDT', 'NMRUSDT', 'NULSUSDT', 'OAXUSDT', 'OCEANUSDT']

tengop = ['OGNUSDT', 'OGUSDT', 'OMGUSDT', 'OMUSDT', 'ONEUSDT', 'ORDIUSDT']

tendop = ['ONGUSDT', 'ONTUSDT', 'OOKIUSDT', 'OPUSDT', 'ORNUSDT', 'VICUSDT']

tenmop = ['OSMOUSDT', 'OXTUSDT', 'PENDLEUSDT', 'PEOPLEUSDT', 'NTRNUSDT', 'BLURUSDT']

eleven = ['PERPUSDT', 'PHAUSDT', 'PHBUSDT', 'PNTUSDT', "VANRYUSDT"]

elevengop = ['POLSUSDT', 'POLYXUSDT', 'PORTOUSDT', 'POWRUSDT', 'PROMUSDT', 'AEURUSDT']

elevendop = ['PROSUSDT', 'PSGUSDT', 'PUNDIXUSDT', 'PYRUSDT', 'RIFUSDT', 'JTOUSDT']

elevenmop = ['QKCUSDT', 'QTUMUSDT', 'QUICKUSDT', 'RADUSDT', 'RLCUSDT', '1000SATSUSDT']

twelve = ['RAYUSDT', 'RDNTUSDT', 'REEFUSDT', 'REIUSDT', 'RENUSDT', 'REQUSDT']

twelvegop = ['RNDRUSDT', 'ROSEUSDT', 'RPLUSDT', 'RSRUSDT', 'RUNEUSDT', "BONKUSDT"]

twelvedop = ['RVNUSDT', 'SANDUSDT', 'SANTOSUSDT', 'SCRTUSDT', 'SCUSDT', "ACEUSDT"]

twelvemop = ['SEIUSDT', 'SFPUSDT', 'SHIBUSDT', 'SKLUSDT', 'SLPUSDT', "PIXELUSDT"]

thirteenth = ['SNTUSDT', 'SNXUSDT', 'SOLUSDT', 'SPELLUSDT', 'SSVUSDT', 'STEEMUSDT']

thirteenthgop = ['STORJUSDT', 'STPTUSDT', 'STRAXUSDT', 'STXUSDT', 'SUIUSDT', "STRKUSDT"]

thirteenthdop = ['SUPERUSDT', 'SUSHIUSDT', 'SXPUSDT', 'SYNUSDT', 'SYSUSDT', "HIFIUSDT"]

thirteenthmop = ['TFUELUSDT', 'THETAUSDT', 'TKOUSDT', 'TLMUSDT', 'TIAUSDT', 'YFIUSDT']

fourteenth = ['TRBUSDT', 'TROYUSDT', 'TRUUSDT', 'TRXUSDT', 'TUSDT', 'STGUSDT']

fourteenthgop = ['TWTUSDT', 'UFTUSDT', 'UMAUSDT', 'UNFIUSDT', 'QIUSDT']

fourteenthdop = ['UNIUSDT', 'USTCUSDT', 'VETUSDT', 'VGXUSDT', 'XVGUSDT', "CREAMUSDT"]

fourteenthmop = ['VIBUSDT', 'VIDTUSDT', 'VITEUSDT', 'VOXELUSDT', "PEPEUSDT", "PORTALUSDT"]

fifteenth = ['WANUSDT', 'WAVESUSDT', 'WAXPUSDT', 'WBETHUSDT', 'JUPUSDT', "PDAUSDT"]

fifteenthgop = ['WLDUSDT', 'WNXMUSDT', 'WOOUSDT', "NTRNUSDT", 'WRXUSDT']

fifteenthdop = ['XECUSDT', 'XEMUSDT', 'XLMUSDT', 'XRPUSDT', "AXLUSDT"]

izg = []

x = one + two + three + four + five + six + seven + eight + nine + ten + eleven + twelve + thirteenth + fourteenth + fifteenth + izg + \
    onedop + twodop + threedop + fourdop + fivedop + sixdop + sevendop + eightdop + ninedop + tendop + elevendop + twelvedop + \
    thirteenthdop + fourteenthdop + fifteenthdop + onemop + twomop + threemop + fourmop + fivemop + sixmop + sevenmop + \
    eightmop + ninemop + tenmop + elevenmop + twelvemop + thirteenthmop + fourteenthmop + \
    onegop + twogop + threegop + fourgop + fivegop + sixgop + sevengop + eightgop + ninegop + tengop + elevengop + \
    twelvegop + thirteenthgop + fourteenthgop + fifteenthgop


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
    j = []
    for name_cript_check in trading_pairs:
        try:
            # print(name_cript_check)
            # print(last_data(name_cript_check, "3m", "300"))
            data_token: Dataset = last_data(name_cript_check, "4h", "4320")
            volume_per_5h = sum([int(i * data_token.high_price[-1]) for i in data_token.volume]) / len(
                data_token.volume)
            res: float = round(data_token.close_price[-1] / data_token.open_price[-1] * 100 - 100, 2)
            res_before: float = round(data_token.close_price[-2] / data_token.open_price[-2] * 100 - 100, 2)
            high_frames = list(map(lambda x: round(x[1] / x[0] * 100 - 100, 2), zip(data_token.open_price, data_token.high_price)))

            print(name_cript_check, res, len([i for i in high_frames if i > 1.5]))
            j.append([name_cript_check, res, len([i for i in high_frames if i > 1.5])])
            # print(name_cript_check)

            # if 2 > res:
            #     buy_qty = round(11 / data_token.close_price[-1], 1)
            #
            #     telebot.TeleBot(telega_token).send_message(chat_id, f"RABOTAEM - {name_cript_check}\n"
            #                                                         f"Количество покупаемого - {buy_qty}, Цена - {data_token.high_price[-1]}\n"
            #                                                         f"Цены {data_token.high_price[-9:]}\n"
            #                                                         f"Объемы {int(volume_per_5h)}\n"
            #                                                         f"Цена упала на {res}%\n")
        except:
            pass
    print(j)
tt = [['1INCHUSDT', 0.55, 14], ['AAVEUSDT', 0.74, 9], ['ACHUSDT', 3.4, 9], ['ACMUSDT', 0.63, 8], ['ADAUSDT', 3.63, 12], ['MANTAUSDT', 0.39, 12], ['APTUSDT', 0.61, 11], ['ARBUSDT', 0.58, 9], ['ARDRUSDT', -0.51, 11], ['ARKMUSDT', -1.07, 14], ['ARPAUSDT', 1.22, 11], ['XAIUSDT', 1.59, 9], ['BEAMXUSDT', 1.58, 10], ['BCHUSDT', 2.11, 15], ['BELUSDT', 0.4, 7], ['BETAUSDT', 0.67, 12], ['BICOUSDT', -0.53, 13], ['NFPUSDT', 1.15, 8], ['CITYUSDT', 0.18, 5], ['CKBUSDT', 1.54, 12], ['CLVUSDT', 2.11, 14], ['COMPUSDT', 0.7, 8], ['COTIUSDT', -2.89, 12], ['DIAUSDT', 0.49, 7], ['DODOUSDT', 2.01, 12], ['DOGEUSDT', 4.14, 16], ['DOTUSDT', 1.44, 12], ['DREPUSDT', -0.45, 7], ['ALTUSDT', 1.61, 12], ['FTTUSDT', -1.65, 14], ['FILUSDT', 0.68, 16], ['FIOUSDT', 0.28, 6], ['FIROUSDT', 1.85, 9], ['FISUSDT', -1.22, 10], ['GNSUSDT', -0.73, 2], ['GRTUSDT', 0.64, 8], ['HARDUSDT', 0.27, 11], ['HBARUSDT', 0.0, 7], ['HFTUSDT', 0.16, 12], ['JASMYUSDT', 1.17, 15], ['JOEUSDT', 1.24, 5], ['JSTUSDT', -0.13, 5], ['JUVUSDT', 0.87, 8], ['KAVAUSDT', 1.87, 9], ['LSKUSDT', 0.63, 12], ['LTCUSDT', 0.45, 8], ['LUNAUSDT', 3.53, 13], ['LUNCUSDT', 6.47, 14], ['MAGICUSDT', 1.1, 10], ['MANAUSDT', 0.82, 12], ['NEOUSDT', 0.31, 11], ['NKNUSDT', 1.66, 9], ['NMRUSDT', 0.64, 9], ['NULSUSDT', 1.31, 9], ['OAXUSDT', 1.3, 10], ['OCEANUSDT', 0.05, 13], ['PERPUSDT', 2.77, 14], ['PHAUSDT', 1.67, 10], ['PHBUSDT', 0.08, 12], ['PNTUSDT', -0.34, 10], ['VANRYUSDT', 1.37, 15], ['RAYUSDT', -1.11, 10], ['RDNTUSDT', 0.67, 9], ['REEFUSDT', 0.45, 16], ['REIUSDT', 0.07, 10], ['RENUSDT', 2.7, 12], ['REQUSDT', -0.08, 6], ['SNTUSDT', 0.56, 9], ['SNXUSDT', 0.95, 10], ['SOLUSDT', 0.13, 6], ['SPELLUSDT', 0.72, 15], ['SSVUSDT', 0.17, 10], ['STEEMUSDT', -0.2, 7], ['TRBUSDT', 1.08, 9], ['TROYUSDT', 0.33, 10], ['TRUUSDT', 2.23, 12], ['TRXUSDT', 0.05, 0], ['TUSDT', 0.21, 8], ['STGUSDT', 1.07, 5], ['WANUSDT', 0.4, 10], ['WAVESUSDT', 2.1, 11], ['WAXPUSDT', 0.29, 5], ['WBETHUSDT', -0.14, 2], ['JUPUSDT', 0.26, 12], ['PDAUSDT', 2.38, 13], ['ALICEUSDT', 3.5, 15], ['ALPACAUSDT', 1.04, 9], ['ALPHAUSDT', 2.31, 13], ['ALPINEUSDT', -0.04, 7], ['AMBUSDT', 2.69, 13], ['AUDIOUSDT', 1.1, 10], ['AVAXUSDT', 0.4, 8], ['AXSUSDT', 1.49, 9], ['BADGERUSDT', 1.11, 12], ['BAKEUSDT', 2.14, 9], ['ZECUSDT', 0.86, 11], ['ZENUSDT', 0.81, 10], ['ZILUSDT', 1.83, 10], ['ZRXUSDT', -1.22, 12], ['BURGERUSDT', 0.6, 11], ['C98USDT', -0.58, 10], ['CAKEUSDT', -0.27, 8], ['CVPUSDT', 0.21, 13], ['CVXUSDT', 0.7, 5], ['CYBERUSDT', 0.65, 9], ['DARUSDT', 1.73, 10], ['DASHUSDT', 1.24, 11], ['DATAUSDT', 1.13, 9], ['ENJUSDT', 1.46, 13], ['ENSUSDT', 1.35, 10], ['EPXUSDT', 4.72, 14], ['ETCUSDT', 1.68, 11], ['RONINUSDT', 0.98, 9], ['FTMUSDT', -4.27, 15], ['FUNUSDT', 0.17, 9], ['FXSUSDT', 1.1, 4], ['GALAUSDT', 3.3, 12], ['GALUSDT', 1.24, 8], ['ICXUSDT', 0.16, 10], ['IDEXUSDT', 1.4, 11], ['IDUSDT', -0.82, 10], ['ILVUSDT', -0.05, 11], ['IMXUSDT', 0.58, 5], ['LAZIOUSDT', 0.78, 6], ['LDOUSDT', 0.57, 6], ['LEVERUSDT', 5.08, 11], ['LINAUSDT', 0.06, 13], ['LINKUSDT', -0.14, 7], ['MDTUSDT', 0.57, 13], ['MINAUSDT', 0.46, 11], ['MKRUSDT', 0.68, 0], ['MLNUSDT', 0.9, 7], ['MOBUSDT', 1.87, 12], ['IQUSDT', 0.09, 13], ['ONGUSDT', 0.37, 8], ['ONTUSDT', 0.7, 9], ['OOKIUSDT', 0.92, 9], ['OPUSDT', 0.74, 8], ['ORNUSDT', 5.0, 7], ['VICUSDT', 0.92, 9], ['PROSUSDT', -0.33, 4], ['PSGUSDT', 1.39, 11], ['PUNDIXUSDT', 0.07, 11], ['PYRUSDT', -1.13, 13], ['RIFUSDT', 8.01, 9], ['JTOUSDT', 0.1, 8], ['RVNUSDT', 1.04, 12], ['SANDUSDT', 0.92, 9], ['SANTOSUSDT', -2.53, 11], ['SCRTUSDT', -0.42, 11], ['SCUSDT', -0.48, 6], ['ACEUSDT', 3.89, 10], ['SUPERUSDT', 1.92, 13], ['SUSHIUSDT', 0.17, 14], ['SXPUSDT', 1.43, 12], ['SYNUSDT', 0.46, 11], ['SYSUSDT', 3.75, 12], ['HIFIUSDT', 1.0, 7], ['UNIUSDT', 0.97, 11], ['USTCUSDT', 3.04, 13], ['VETUSDT', 0.7, 7], ['VGXUSDT', -0.08, 9], ['XVGUSDT', 1.2, 10], ['CREAMUSDT', 0.28, 10], ['XECUSDT', 1.93, 15], ['XEMUSDT', 0.96, 9], ['XLMUSDT', 2.19, 10], ['XRPUSDT', -1.17, 9], ['AXLUSDT', 0.89, 15], ['AMPUSDT', 0.23, 10], ['ANKRUSDT', -0.22, 10], ['APEUSDT', 2.76, 12], ['API3USDT', 0.13, 7], ['AIUSDT', 0.53, 11], ['BALUSDT', 0.41, 5], ['BANDUSDT', 1.51, 10], ['BARUSDT', 0.39, 4], ['BATUSDT', 1.57, 11], ['ARKUSDT', 2.27, 8], ['CELRUSDT', 6.03, 12], ['CFXUSDT', 6.99, 11], ['CHESSUSDT', -0.74, 14], ['CHRUSDT', 1.0, 6], ['CHZUSDT', 0.24, 11], ['DCRUSDT', 0.32, 15], ['DEGOUSDT', 1.54, 13], ['DENTUSDT', 0.76, 13], ['DEXEUSDT', 0.64, 11], ['DFUSDT', -0.36, 7], ['FARMUSDT', 0.02, 10], ['FETUSDT', 1.46, 12], ['FIDAUSDT', 2.75, 10], ['GFTUSDT', 2.38, 11], ['PYTHUSDT', 0.2, 11], ['GLMRUSDT', 1.03, 13], ['GLMUSDT', 0.58, 16], ['GMTUSDT', 1.22, 10], ['GMXUSDT', -0.12, 6], ['GASUSDT', -0.57, 12], ['INJUSDT', -0.13, 11], ['IOTAUSDT', 1.24, 12], ['IOTXUSDT', 1.78, 10], ['IRISUSDT', 1.03, 7], ['STMXUSDT', -1.32, 13], ['LITUSDT', 3.2, 11], ['LOKAUSDT', 1.1, 13], ['LOOMUSDT', 0.16, 12], ['LQTYUSDT', 8.46, 6], ['LRCUSDT', -0.06, 10], ['MOVRUSDT', -0.32, 10], ['MTLUSDT', -3.12, 8], ['NEARUSDT', -0.44, 11], ['MEMEUSDT', 0.95, 17], ['PIVXUSDT', -0.2, 11], ['OSMOUSDT', 0.27, 1], ['OXTUSDT', 3.48, 7], ['PENDLEUSDT', 1.08, 9], ['PEOPLEUSDT', 5.99, 12], ['NTRNUSDT', -1.03, 10], ['BLURUSDT', 1.34, 7], ['QKCUSDT', 0.67, 12], ['QTUMUSDT', 1.56, 15], ['QUICKUSDT', 0.69, 14], ['RADUSDT', 2.51, 11], ['RLCUSDT', 1.39, 9], ['1000SATSUSDT', 0.99, 16], ['SEIUSDT', 0.82, 6], ['SFPUSDT', 0.75, 3], ['SHIBUSDT', 10.63, 18], ['SKLUSDT', 0.64, 11], ['SLPUSDT', 2.41, 15], ['PIXELUSDT', 1.24, 11], ['TFUELUSDT', -1.16, 13], ['THETAUSDT', 0.13, 13], ['TKOUSDT', 0.37, 9], ['TLMUSDT', -0.18, 16], ['TIAUSDT', -0.81, 4], ['YFIUSDT', 2.06, 12], ['VIBUSDT', 0.13, 6], ['VIDTUSDT', -0.62, 10], ['VITEUSDT', 0.03, 14], ['VOXELUSDT', 0.35, 14], ['PEPEUSDT', 2.8, 18], ['PORTALUSDT', -2.08, 11], ['AERGOUSDT', -0.6, 9], ['AGIXUSDT', -1.62, 13], ['AGLDUSDT', 1.43, 11], ['ALCXUSDT', 1.66, 12], ['ALGOUSDT', 2.01, 13], ['ARUSDT', -1.25, 12], ['ASRUSDT', 1.89, 11], ['ATMUSDT', 1.94, 7], ['ATOMUSDT', 0.38, 6], ['AUCTIONUSDT', 0.04, 13], ['BIFIUSDT', 0.41, 10], ['BLZUSDT', 0.55, 5], ['BNXUSDT', -0.06, 12], ['BONDUSDT', 1.27, 8], ['YGGUSDT', 0.93, 11], ['CRVUSDT', 2.34, 10], ['CTSIUSDT', -0.05, 10], ['CTXCUSDT', -0.37, 7], ['CVCUSDT', 0.6, 10], ['DYMUSDT', 0.68, 10], ['DUSKUSDT', 1.11, 9], ['DYDXUSDT', 1.41, 12], ['EDUUSDT', 1.77, 7], ['EGLDUSDT', 0.55, 12], ['ELFUSDT', 0.78, 7], ['FLOKIUSDT', 2.23, 18], ['FLUXUSDT', 0.84, 7], ['FORTHUSDT', -0.55, 6], ['FORUSDT', -0.85, 7], ['FRONTUSDT', 0.65, 14], ['HIGHUSDT', 3.52, 11], ['HIVEUSDT', -3.81, 10], ['HOOKUSDT', 0.92, 10], ['HOTUSDT', 1.06, 15], ['ICPUSDT', 3.08, 13], ['KEYUSDT', 3.82, 6], ['KLAYUSDT', 1.92, 14], ['KMDUSDT', -0.23, 6], ['KP3RUSDT', -0.09, 10], ['KSMUSDT', 0.98, 12], ['MASKUSDT', 4.06, 12], ['MATICUSDT', -0.58, 8], ['MAVUSDT', 1.11, 11], ['MBLUSDT', 0.23, 7], ['MBOXUSDT', 0.41, 11], ['COMBOUSDT', 0.31, 12], ['OGNUSDT', 4.68, 10], ['OGUSDT', -0.87, 7], ['OMGUSDT', 1.3, 15], ['OMUSDT', -1.17, 9], ['ONEUSDT', -1.24, 17], ['ORDIUSDT', 2.3, 13], ['POLSUSDT', 0.68, 4], ['POLYXUSDT', 1.72, 11], ['PORTOUSDT', 1.02, 9], ['POWRUSDT', 0.82, 7], ['PROMUSDT', 0.54, 9], ['AEURUSDT', 0.06, 0], ['RNDRUSDT', -0.85, 11], ['ROSEUSDT', 1.79, 14], ['RPLUSDT', -0.32, 7], ['RSRUSDT', -1.68, 9], ['RUNEUSDT', -0.39, 7], ['BONKUSDT', 8.46, 16], ['STORJUSDT', 0.31, 10], ['STPTUSDT', 0.07, 7], ['STRAXUSDT', 1.09, 11], ['STXUSDT', -0.36, 7], ['SUIUSDT', 0.44, 3], ['STRKUSDT', 0.5, 11], ['TWTUSDT', 0.6, 7], ['UFTUSDT', 0.21, 7], ['UMAUSDT', 2.4, 9], ['UNFIUSDT', 0.54, 9], ['QIUSDT', 1.52, 12], ['WLDUSDT', -0.88, 14], ['WNXMUSDT', 0.65, 4], ['WOOUSDT', 1.23, 10], ['NTRNUSDT', -0.89, 10], ['WRXUSDT', -4.38, 11]]

# mm = [['1INCHUSDT', 2.12], ['AAVEUSDT', 1.64], ['ACHUSDT', 1.93], ['ACMUSDT', 2.58], ['ADAUSDT', 1.98], ['MANTAUSDT', 2.02], ['APTUSDT', 1.59], ['ARBUSDT', 1.63], ['ARDRUSDT', 2.67], ['ARKMUSDT', 5.75], ['ARPAUSDT', 1.52], ['XAIUSDT', 1.95], ['BEAMXUSDT', 2.19], ['BCHUSDT', 5.29], ['BELUSDT', 1.38], ['BETAUSDT', 3.75], ['BICOUSDT', 5.38], ['NFPUSDT', 2.84], ['CITYUSDT', 1.38], ['CKBUSDT', 2.48], ['CLVUSDT', 2.71], ['COMPUSDT', 1.7], ['COTIUSDT', 2.56], ['DIAUSDT', 1.7], ['DODOUSDT', 2.65], ['DOGEUSDT', 4.27], ['DOTUSDT', 2.08], ['DREPUSDT', 2.03], ['ALTUSDT', 2.44], ['FTTUSDT', 4.74], ['FILUSDT', 3.37], ['FIOUSDT', 1.62], ['FIROUSDT', 1.78], ['FISUSDT', 1.8], ['GNSUSDT', 0.85], ['GRTUSDT', 2.9], ['HARDUSDT', 2.71], ['HBARUSDT', 1.21], ['HFTUSDT', 3.36], ['JASMYUSDT', 3.88], ['JOEUSDT', 1.53], ['JSTUSDT', 1.73], ['JUVUSDT', 2.08], ['KAVAUSDT', 2.26], ['LSKUSDT', 1.99], ['LTCUSDT', 2.15], ['LUNAUSDT', 3.53], ['LUNCUSDT', 5.17], ['MAGICUSDT', 2.32], ['MANAUSDT', 2.52], ['NEOUSDT', 2.97], ['NKNUSDT', 1.86], ['NMRUSDT', 2.71], ['NULSUSDT', 1.69], ['OAXUSDT', 2.22], ['OCEANUSDT', 4.44], ['PERPUSDT', 3.72], ['PHAUSDT', 2.59], ['PHBUSDT', 3.33], ['PNTUSDT', 1.68], ['VANRYUSDT', 9.96], ['RAYUSDT', 3.08], ['RDNTUSDT', 1.76], ['REEFUSDT', 3.07], ['REIUSDT', 2.2], ['RENUSDT', 2.08], ['REQUSDT', 1.58], ['SNTUSDT', 3.08], ['SNXUSDT', 2.01], ['SOLUSDT', 1.82], ['SPELLUSDT', 6.84], ['SSVUSDT', 2.21], ['STEEMUSDT', 1.47], ['TRBUSDT', 1.86], ['TROYUSDT', 2.35], ['TRUUSDT', 1.79], ['TRXUSDT', 0.2], ['TUSDT', 1.53], ['STGUSDT', 1.49], ['WANUSDT', 2.12], ['WAVESUSDT', 2.52], ['WAXPUSDT', 1.86], ['WBETHUSDT', 0.89], ['JUPUSDT', 3.17], ['PDAUSDT', 9.4], ['ALICEUSDT', 2.3], ['ALPACAUSDT', 1.58], ['ALPHAUSDT', 2.44], ['ALPINEUSDT', 1.89], ['AMBUSDT', 3.03], ['AUDIOUSDT', 2.2], ['AVAXUSDT', 1.66], ['AXSUSDT', 2.55], ['BADGERUSDT', 5.0], ['BAKEUSDT', 2.39], ['ZECUSDT', 2.03], ['ZENUSDT', 1.88], ['ZILUSDT', 1.83], ['ZRXUSDT', 2.0], ['BURGERUSDT', 2.22], ['C98USDT', 2.14], ['CAKEUSDT', 1.74], ['CVPUSDT', 2.09], ['CVXUSDT', 1.12], ['CYBERUSDT', 3.49], ['DARUSDT', 2.37], ['DASHUSDT', 2.41], ['DATAUSDT', 2.22], ['ENJUSDT', 3.32], ['ENSUSDT', 1.81], ['EPXUSDT', 5.71], ['ETCUSDT', 2.64], ['RONINUSDT', 1.86], ['FTMUSDT', 3.13], ['FUNUSDT', 1.67], ['FXSUSDT', 1.2], ['GALAUSDT', 2.97], ['GALUSDT', 2.2], ['ICXUSDT', 2.23], ['IDEXUSDT', 1.55], ['IDUSDT', 3.81], ['ILVUSDT', 2.02], ['IMXUSDT', 1.17], ['LAZIOUSDT', 1.63], ['LDOUSDT', 1.44], ['LEVERUSDT', 2.45], ['LINAUSDT', 3.1], ['LINKUSDT', 1.49], ['MDTUSDT', 5.54], ['MINAUSDT', 1.63], ['MKRUSDT', 0.79], ['MLNUSDT', 1.41], ['MOBUSDT', 2.32], ['IQUSDT', 4.36], ['ONGUSDT', 1.38], ['ONTUSDT', 1.54], ['OOKIUSDT', 2.98], ['OPUSDT', 1.93], ['ORNUSDT', 1.59], ['VICUSDT', 1.75], ['PROSUSDT', 1.24], ['PSGUSDT', 2.61], ['PUNDIXUSDT', 1.62], ['PYRUSDT', 2.51], ['RIFUSDT', 1.97], ['JTOUSDT', 2.79], ['RVNUSDT', 2.03], ['SANDUSDT', 2.65], ['SANTOSUSDT', 2.78], ['SCRTUSDT', 1.99], ['SCUSDT', 1.31], ['ACEUSDT', 2.57], ['SUPERUSDT', 3.11], ['SUSHIUSDT', 2.63], ['SXPUSDT', 1.79], ['SYNUSDT', 2.3], ['SYSUSDT', 6.23], ['HIFIUSDT', 1.8], ['UNIUSDT', 3.18], ['USTCUSDT', 3.49], ['VETUSDT', 1.39], ['VGXUSDT', 2.41], ['XVGUSDT', 2.05], ['CREAMUSDT', 1.65], ['XECUSDT', 3.8], ['XEMUSDT', 2.1], ['XLMUSDT', 1.48], ['XRPUSDT', 1.5], ['AXLUSDT', 13.58], ['AMPUSDT', 2.03], ['ANKRUSDT', 3.39], ['APEUSDT', 3.14], ['API3USDT', 1.46], ['AIUSDT', 3.12], ['BALUSDT', 1.29], ['BANDUSDT', 2.09], ['BARUSDT', 1.46], ['BATUSDT', 2.76], ['ARKUSDT', 2.15], ['CELRUSDT', 2.08], ['CFXUSDT', 1.71], ['CHESSUSDT', 2.08], ['CHRUSDT', 1.47], ['CHZUSDT', 2.44], ['DCRUSDT', 3.13], ['DEGOUSDT', 2.49], ['DENTUSDT', 3.54], ['DEXEUSDT', 4.28], ['DFUSDT', 1.73], ['FARMUSDT', 1.67], ['FETUSDT', 4.79], ['FIDAUSDT', 2.03], ['GFTUSDT', 2.95], ['PYTHUSDT', 1.8], ['GLMRUSDT', 1.89], ['GLMUSDT', 7.81], ['GMTUSDT', 1.84], ['GMXUSDT', 2.09], ['GASUSDT', 2.52], ['INJUSDT', 1.8], ['IOTAUSDT', 2.07], ['IOTXUSDT', 1.89], ['IRISUSDT', 1.52], ['STMXUSDT', 3.27], ['LITUSDT', 2.6], ['LOKAUSDT', 3.29], ['LOOMUSDT', 1.83], ['LQTYUSDT', 1.32], ['LRCUSDT', 2.48], ['MOVRUSDT', 2.25], ['MTLUSDT', 1.61], ['NEARUSDT', 2.31], ['MEMEUSDT', 7.52], ['PIVXUSDT', 2.07], ['OSMOUSDT', 0.81], ['OXTUSDT', 1.63], ['PENDLEUSDT', 2.34], ['PEOPLEUSDT', 5.21], ['NTRNUSDT', 2.21], ['BLURUSDT', 1.21], ['QKCUSDT', 1.75], ['QTUMUSDT', 2.61], ['QUICKUSDT', 7.98], ['RADUSDT', 1.83], ['RLCUSDT', 1.81], ['1000SATSUSDT', 4.44], ['SEIUSDT', 1.38], ['SFPUSDT', 1.17], ['SHIBUSDT', 7.98], ['SKLUSDT', 3.43], ['SLPUSDT', 6.74], ['PIXELUSDT', 2.59], ['TFUELUSDT', 4.26], ['THETAUSDT', 4.66], ['TKOUSDT', 2.81], ['TLMUSDT', 5.4], ['TIAUSDT', 1.31], ['YFIUSDT', 2.21], ['VIBUSDT', 1.44], ['VIDTUSDT', 3.78], ['VITEUSDT', 2.71], ['VOXELUSDT', 2.92], ['PEPEUSDT', 10.2], ['PORTALUSDT', 3.64], ['AERGOUSDT', 1.8], ['AGIXUSDT', 6.0], ['AGLDUSDT', 1.95], ['ALCXUSDT', 2.11], ['ALGOUSDT', 2.0], ['ARUSDT', 4.48], ['ASRUSDT', 5.26], ['ATMUSDT', 1.88], ['ATOMUSDT', 1.24], ['AUCTIONUSDT', 1.58], ['BIFIUSDT', 1.64], ['BLZUSDT', 1.36], ['BNXUSDT', 2.73], ['BONDUSDT', 1.69], ['YGGUSDT', 3.11], ['CRVUSDT', 2.09], ['CTSIUSDT', 2.07], ['CTXCUSDT', 1.85], ['CVCUSDT', 2.02], ['DYMUSDT', 2.01], ['DUSKUSDT', 1.67], ['DYDXUSDT', 2.3], ['EDUUSDT', 1.58], ['EGLDUSDT', 2.45], ['ELFUSDT', 1.96], ['FLOKIUSDT', 13.45], ['FLUXUSDT', 3.16], ['FORTHUSDT', 1.57], ['FORUSDT', 2.43], ['FRONTUSDT', 2.64], ['HIGHUSDT', 2.66], ['HIVEUSDT', 1.58], ['HOOKUSDT', 2.84], ['HOTUSDT', 6.4], ['ICPUSDT', 1.94], ['KEYUSDT', 1.57], ['KLAYUSDT', 2.91], ['KMDUSDT', 1.38], ['KP3RUSDT', 2.06], ['KSMUSDT', 2.06], ['MASKUSDT', 1.69], ['MATICUSDT', 1.75], ['MAVUSDT', 2.87], ['MBLUSDT', 2.91], ['MBOXUSDT', 4.25], ['COMBOUSDT', 3.93], ['OGNUSDT', 2.03], ['OGUSDT', 1.98], ['OMGUSDT', 5.32], ['OMUSDT', 2.45], ['ONEUSDT', 2.67], ['ORDIUSDT', 3.45], ['POLSUSDT', 1.02], ['POLYXUSDT', 1.75], ['PORTOUSDT', 1.97], ['POWRUSDT', 1.49], ['PROMUSDT', 2.24], ['AEURUSDT', 0.15], ['RNDRUSDT', 2.33], ['ROSEUSDT', 2.37], ['RPLUSDT', 1.42], ['RSRUSDT', 2.07], ['RUNEUSDT', 1.17], ['BONKUSDT', 7.42], ['STORJUSDT', 2.03], ['STPTUSDT', 1.94], ['STRAXUSDT', 3.6], ['STXUSDT', 1.73], ['SUIUSDT', 1.25], ['STRKUSDT', 1.85], ['TWTUSDT', 1.53], ['UFTUSDT', 1.26], ['UMAUSDT', 1.64], ['UNFIUSDT', 1.68], ['QIUSDT', 2.79], ['WLDUSDT', 4.25], ['WNXMUSDT', 0.97], ['WOOUSDT', 2.98], ['NTRNUSDT', 2.21], ['WRXUSDT', 2.09]]

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

# data_token = last_data("EPXUSDT", "4h", "1440")
# price_change_percent_24h: float = round(((data_token.close_price[-1] / data_token.close_price[0]) * 100) - 100, 2)
# print(data_token.close_price[-1], data_token.close_price[0])
# print(price_change_percent_24h)