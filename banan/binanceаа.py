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

one = ['1INCHUSDT', 'AAVEUSDT', 'ACHUSDT', 'ACMUSDT', 'ADAUSDT', 'AERGOUSDT', 'AGIXUSDT',
       'AGLDUSDT', 'ALCXUSDT', 'ALGOUSDT']

onedop = ['ALICEUSDT', 'ALPACAUSDT', 'ALPHAUSDT', 'ALPINEUSDT', 'AMBUSDT', 'AMPUSDT', 'ANKRUSDT', 'ANTUSDT', 'APEUSDT', 'API3USDT']

two = ['APTUSDT', 'ARBUSDT', 'ARDRUSDT', 'ARKMUSDT', 'ARPAUSDT', 'ARUSDT', 'ASRUSDT',
       'ATMUSDT', 'ATOMUSDT', 'AUCTIONUSDT']

twodop = ['AUDIOUSDT', 'AVAXUSDT', 'AXSUSDT', 'BADGERUSDT', 'BAKEUSDT',
       'BALUSDT', 'BANDUSDT', 'BARUSDT', 'BATUSDT', 'ARKUSDT']

three = ["BEAMXUSDT", 'BCHUSDT', 'BELUSDT', 'BETAUSDT', 'BICOUSDT', 'BIFIUSDT', 'BLZUSDT', 'BNXUSDT',
         'BONDUSDT', 'YGGUSDT']

threedop = ['ZECUSDT', 'ZENUSDT', 'ZILUSDT', 'ZRXUSDT', 'BURGERUSDT',
         'C98USDT', 'CAKEUSDT', 'CELRUSDT', 'CFXUSDT', 'CHESSUSDT', 'CHRUSDT', 'CHZUSDT']

four = ['CITYUSDT', 'CKBUSDT', 'CLVUSDT', 'COMPUSDT', 'COTIUSDT', 'CRVUSDT',
        'CTSIUSDT', 'CTXCUSDT', 'CVCUSDT']

fourdop = ['CVPUSDT', 'CVXUSDT', 'CYBERUSDT', 'DARUSDT', 'DASHUSDT', 'DATAUSDT',
        'DCRUSDT', 'DEGOUSDT', 'DENTUSDT', 'DEXEUSDT', 'DFUSDT']

five = ['DIAUSDT', 'DODOUSDT', 'DOGEUSDT', 'DOTUSDT', 'DREPUSDT', 'DUSKUSDT', 'DYDXUSDT',
        'EDUUSDT', 'EGLDUSDT', 'ELFUSDT']

fivedop = ['ENJUSDT', 'ENSUSDT', 'EPXUSDT', 'ETCUSDT', 'FARMUSDT',
        'FETUSDT', 'FIDAUSDT', 'GFTUSDT']

six = ["FTTUSDT", 'FILUSDT', 'FIOUSDT', 'FIROUSDT', 'FISUSDT', 'FLOKIUSDT', 'FLUXUSDT', 'FORTHUSDT',
       'FORUSDT', 'FRONTUSDT']

sixdop = ['FTMUSDT', 'FUNUSDT', 'FXSUSDT', 'GALAUSDT', 'GALUSDT',
       'GLMRUSDT', 'GLMUSDT', 'GMTUSDT', 'GMXUSDT', 'GASUSDT']

seven = ['GNSUSDT', 'GRTUSDT', 'HARDUSDT', 'HBARUSDT', 'HFTUSDT', 'HIGHUSDT',
         'HIVEUSDT', 'HOOKUSDT', 'HOTUSDT', 'ICPUSDT']

sevendop = ['ICXUSDT', 'IDEXUSDT', 'IDUSDT', 'ILVUSDT', 'IMXUSDT', 'INJUSDT',
         'IOTAUSDT', 'IOTXUSDT', 'IRISUSDT']

eight = ['JASMYUSDT', 'JOEUSDT', 'JSTUSDT', 'JUVUSDT', 'KAVAUSDT', 'KEYUSDT', 'KLAYUSDT', 'KMDUSDT',
         'KP3RUSDT', 'KSMUSDT']

eightdop = ['LAZIOUSDT', 'LDOUSDT', 'LEVERUSDT', 'LINAUSDT', 'LINKUSDT', 'LITUSDT',
         'LOKAUSDT', 'LOOMUSDT', 'LQTYUSDT', 'LRCUSDT']

nine = ['LSKUSDT', 'LTCUSDT', 'LUNAUSDT', 'LUNCUSDT', 'MAGICUSDT', 'MANAUSDT', 'MASKUSDT', 'MATICUSDT',
        'MAVUSDT', 'MBLUSDT', 'MBOXUSDT']

ninedop = ['MDTUSDT', 'MINAUSDT', 'MKRUSDT', 'MLNUSDT', 'MOBUSDT',
        'MOVRUSDT', 'MTLUSDT', 'MULTIUSDT', 'NEARUSDT', 'MEMEUSDT']

ten = ['NEOUSDT', 'NKNUSDT', 'NMRUSDT', 'NULSUSDT', 'OAXUSDT', 'OCEANUSDT', 'OGNUSDT', 'OGUSDT', 'OMGUSDT',
       'OMUSDT', 'ONEUSDT', 'ORDIUSDT']

tendop = ['ONGUSDT', 'ONTUSDT', 'OOKIUSDT', 'OPUSDT', 'ORNUSDT', 'OSMOUSDT', 'OXTUSDT',
       'PENDLEUSDT', 'PEOPLEUSDT', 'NTRNUSDT']

eleven = ['PERLUSDT', 'PERPUSDT', 'PHAUSDT', 'PHBUSDT', 'PNTUSDT', 'POLSUSDT', 'POLYXUSDT',
          'PORTOUSDT', 'POWRUSDT', 'PROMUSDT']

elevendop = ['PROSUSDT', 'PSGUSDT', 'PUNDIXUSDT', 'PYRUSDT', 'QKCUSDT',
          'QTUMUSDT', 'QUICKUSDT', 'RADUSDT']

twelve = ['RAYUSDT', 'RDNTUSDT', 'REEFUSDT', 'REIUSDT', 'RENUSDT', 'REQUSDT', 'RIFUSDT', 'RLCUSDT', 'RNDRUSDT',
          'ROSEUSDT', 'RPLUSDT', 'RSRUSDT', 'RUNEUSDT']

twelvedop = ['RVNUSDT', 'SANDUSDT', 'SANTOSUSDT', 'SCRTUSDT', 'SCUSDT',
          'SEIUSDT', 'SFPUSDT', 'SHIBUSDT', 'SKLUSDT', 'SLPUSDT']

thirteenth = ['SNTUSDT', 'SNXUSDT', 'SOLUSDT', 'SPELLUSDT', 'SSVUSDT', 'STEEMUSDT', 'STGUSDT', 'STMXUSDT', 'STORJUSDT',
              'STPTUSDT', 'STRAXUSDT', 'STXUSDT', 'SUIUSDT']

thirteenthdop = ['SUPERUSDT', 'SUSHIUSDT', 'SXPUSDT', 'SYNUSDT',
              'SYSUSDT', 'TFUELUSDT', 'THETAUSDT', 'TKOUSDT', 'TLMUSDT', 'TIAUSDT']

fourteenth = ['TOMOUSDT', 'TRBUSDT', 'TROYUSDT', 'TRUUSDT', 'TRXUSDT', 'TUSDT', 'TVKUSDT', 'TWTUSDT',
              'UFTUSDT', 'UMAUSDT', 'UNFIUSDT']

fourteenthdop = ['UNIUSDT', 'USTCUSDT', 'VETUSDT',
              'VGXUSDT', 'VIBUSDT', 'VIDTUSDT', 'VITEUSDT', 'VOXELUSDT']

fifteenth = ['WANUSDT', 'WAVESUSDT', 'WAXPUSDT', 'WBETHUSDT', 'WLDUSDT', 'WNXMUSDT',
             'WOOUSDT', 'WRXUSDT', 'WTCUSDT']

fifteenthdop = ['XECUSDT', 'XEMUSDT', 'XLMUSDT', 'XMRUSDT', 'XRPUSDT',
             'XVGUSDT', 'YFIUSDT']

izg = ["HIFIUSDT", "CREAMUSDT", "QIUSDT"]

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


i = "DOGEUSDT"
data_token = last_data(i, "1h", "1440")



def sql_del():
    try:
        connection = pymysql.connect(host='127.0.0.1', port=3306, user='banan_user',
                                     password='warlight123',
                                     database='banans',
                                     cursorclass=pymysql.cursors.DictCursor)
        try:
            with connection.cursor() as cursor:
                insert_query = "DELETE FROM `new_table`"
                cursor.execute(insert_query)
                connection.commit()
        finally:
            connection.close()

    except Exception as e:
        print(e)



hhhhh = []
ddd = {}
sql_del()
for d in x:
    data = []
    try:
        data_token = last_data(d, "1h", "9440")
        open = data_token.open_price

        close = data_token.close_price

        low = data_token.low_price

        high = data_token.high_price

        it = list(map(lambda x: -round((x[0]/x[1] * 100 - 100), 2) if x[0] > x[1] else round((100 - x[0]/x[1] *100), 2), zip(open, close)))

        high_it = list(map(lambda x: abs(round((x[1]/x[0] * 100 - 100), 2)), zip(high, open)))

        close_it = list(map(lambda x: -round((x[0] / x[1] * 100 - 100), 2), zip(open, close)))

        low_it = list(map(lambda x: round((x[0] / x[1] * 100 - 100), 2), zip(low, open)))


        for i in range(0, len(it)-1):

             # if it[i] < - 3.1 and high_it[i + 1] < 1:
             #     print(it[i], high_it[i+1], d)

             if it[i] < - 4:
                 if d not in ddd:
                     ddd[d] = [it[i], high_it[i+1]]
                     print(it[i], high_it[i+1], d)
                     hhhhh.append(high_it[i+1])
                     values = (d, it[i], high_it[i+1], close_it[i+1], low_it[i+1], it.index(it[i]),
                               close_it[i+1])

                     try:
                         connection = pymysql.connect(host='127.0.0.1', port=3306, user='banan_user',
                                                      password='warlight123',
                                                      database='banans',
                                                      cursorclass=pymysql.cursors.DictCursor)
                         try:
                             with connection.cursor() as cursor:
                                 insert_query = "INSERT INTO `new_table` (title, price_loss, price_high, price_close, price_low, indexx, price_next_close) " \
                                                "VALUES (%s, %s, %s, %s, %s, %s, %s)"
                                 cursor.execute(insert_query, (values))
                                 connection.commit()
                         finally:
                             connection.close()
                     except Exception as e:
                         print(e)

                 else:
                     ddd[d] += it[i], high_it[i + 1]
                     values = (d, it[i], high_it[i+1], close_it[i+1], low_it[i+1], it.index(it[i]),
                               close_it[i+1])

                     try:
                         connection = pymysql.connect(host='127.0.0.1', port=3306, user='banan_user',
                                                      password='warlight123',
                                                      database='banans',
                                                      cursorclass=pymysql.cursors.DictCursor)
                         try:
                             with connection.cursor() as cursor:
                                 insert_query = "INSERT INTO `new_table` (title, price_loss, price_high, price_close, price_low, indexx, price_next_close) " \
                                                "VALUES (%s, %s, %s, %s, %s, %s, %s)"
                                 cursor.execute(insert_query, (values))
                                 connection.commit()
                         finally:
                             connection.close()
                     except Exception as e:
                         print(e)
    except:
        pass

print(ddd)
h4 = {'1INCHUSDT': [-4.27, 0.64, -4.58, 2.06, -5.85, 3.15, -4.13, 1.13], 'AAVEUSDT': [-4.26, 0.92, -4.64, 2.47], 'ACHUSDT': [-4.15, 1.51], 'ADAUSDT': [-4.33, 1.66, -4.87, 3.61], 'AERGOUSDT': [-7.76, 7.97, -11.51, 3.06, -5.0, 2.99, -5.68, 2.9, -7.85, 3.19], 'AGIXUSDT': [-6.04, 0.41, -7.88, 3.91], 'AGLDUSDT': [-4.81, 0.23, -4.8, 2.46, -10.04, 4.42], 'ALCXUSDT': [-4.02, 1.77], 'ALGOUSDT': [-5.48, 1.48, -4.13, 1.64, -4.74, 3.52], 'APTUSDT': [-4.55, 0.61, -5.18, 4.24], 'ARBUSDT': [-4.45, 0.14, -4.46, 1.19, -4.64, 3.44], 'ARDRUSDT': [-12.24, 1.82], 'ARKMUSDT': [-4.95, 2.88, -4.97, 2.7, -5.77, 1.53, -6.92, 2.91, -4.15, 4.01, -4.58, 0.85], 'ARPAUSDT': [-5.58, 0.39], 'ARUSDT': [-4.27, 3.59, -6.32, 4.46], 'ATMUSDT': [-6.04, 0.98], 'ATOMUSDT': [-6.36, 2.04, -4.42, 1.35, -4.88, 2.81], 'BEAMXUSDT': [-10.13, 10.04, -7.5, 9.63, -8.85, 2.43, -7.05, 7.6], 'BELUSDT': [-4.08, 0.06, -4.24, 4.49, -4.02, 1.55, -4.09, 4.04], 'BETAUSDT': [-5.04, 1.47], 'BICOUSDT': [-5.44, 1.11, -4.01, 2.33, -5.12, 3.99], 'BIFIUSDT': [-4.95, 1.84, -4.64, 3.48], 'BLZUSDT': [-5.96, 0.65, -6.04, 2.73], 'BNXUSDT': [-4.72, 4.54, -4.8, 7.74, -6.51, 2.39], 'BONDUSDT': [-7.0, 2.57, -10.09, 1.97, -5.3, 2.79], 'YGGUSDT': [-4.71, 1.74, -5.12, 2.66, -5.27, 5.21, -4.03, 0.05, -4.99, 1.84, -6.96, 5.43, -4.25, 0.83], 'CKBUSDT': [-4.68, 3.03, -6.16, 2.64, -4.05, 0.89], 'CLVUSDT': [-4.54, 0.0], 'COMPUSDT': [-4.69, 1.63, -4.57, 2.44], 'COTIUSDT': [-6.7, 0.47, -4.59, 2.58], 'CRVUSDT': [-5.6, 2.05, -4.76, 4.22], 'CTSIUSDT': [-4.88, 0.12, -6.59, 2.85, -4.03, 3.55], 'CTXCUSDT': [-4.79, 1.53, -5.06, 3.29, -14.97, 3.09, -7.76, 2.08], 'CVCUSDT': [-5.46, 7.43, -39.46, 4.21], 'DODOUSDT': [-5.15, 0.33, -4.4, 3.32], 'DOGEUSDT': [-5.25, 5.0, -4.8, 4.87], 'DOTUSDT': [-4.61, 3.72], 'DYDXUSDT': [-4.36, 2.88, -4.26, 8.25, -5.17, 5.89, -4.93, 1.41, -4.88, 6.48, -9.19, 3.32, -4.19, 1.06], 'EDUUSDT': [-5.67, 0.32, -5.27, 6.45, -4.48, 2.42, -4.72, 6.64], 'EGLDUSDT': [-4.56, 3.52, -4.73, 3.36, -4.53, 4.06, -6.0, 0.02, -4.61, 1.06, -4.5, 1.02], 'FTTUSDT': [-11.75, 11.27, -5.81, 1.98, -9.02, 8.96, -12.72, 9.46, -6.39, 7.0, -5.08, 1.51, -6.63, 3.42, -5.14, 7.14, -5.37, 1.87], 'FILUSDT': [-5.31, 1.75, -4.35, 3.62, -4.41, 1.64, -4.38, 3.66], 'FIROUSDT': [-4.36, 2.54], 'FISUSDT': [-6.04, 2.09, -4.1, 1.6, -4.17, 4.1], 'FLOKIUSDT': [-6.08, 1.02, -4.7, 2.81, -7.54, 1.17, -5.53, 3.44], 'FLUXUSDT': [-4.16, 0.3, -4.3, 3.24, -4.34, 1.15], 'FORTHUSDT': [-5.07, 1.06, -4.05, 0.77], 'FORUSDT': [-4.49, 2.55], 'FRONTUSDT': [-4.52, 0.19, -7.39, 3.58], 'GRTUSDT': [-5.24, 0.96, -5.3, 3.67], 'HBARUSDT': [-5.16, 4.3], 'HFTUSDT': [-5.88, 0.83, -6.29, 3.15, -4.01, 3.79, -5.4, 4.07, -4.2, 0.98], 'HIGHUSDT': [-6.22, 0.56, -5.37, 2.89, -4.64, 3.38], 'HOOKUSDT': [-5.17, 0.59, -6.76, 3.93, -4.3, 1.33, -4.29, 3.76], 'HOTUSDT': [-5.73, 0.13, -4.19, 2.55, -4.74, 3.99], 'ICPUSDT': [-5.01, 0.53, -4.79, 3.74, -5.07, 1.87], 'JASMYUSDT': [-4.71, 4.37, -5.96, 0.36], 'JOEUSDT': [-6.77, 2.48, -5.01, 7.43, -4.84, 2.32, -4.06, 6.02, -8.75, 1.57], 'JUVUSDT': [-11.82, 10.01, -4.12, 3.46, -5.56, 0.77], 'KAVAUSDT': [-4.12, 3.95], 'KEYUSDT': [-4.47, 0.43], 'KLAYUSDT': [-4.71, 1.62, -4.5, 1.04, -4.62, 4.42], 'KMDUSDT': [-7.19, 0.0], 'KP3RUSDT': [-21.31, 5.23, -11.19, 4.21, -5.38, 4.14, -7.51, 4.66, -4.44, 2.55, -5.9, 7.73, -11.08, 0.96], 'KSMUSDT': [-6.11, 0.94, -5.0, 0.64, -4.25, 3.16, -4.28, 4.65], 'LSKUSDT': [-4.03, 3.53], 'LUNAUSDT': [-7.27, 6.0, -5.68, 4.87, -5.55, 2.49, -5.35, 0.16, -5.0, 2.22, -4.44, 3.32], 'LUNCUSDT': [-4.93, 0.76], 'MAGICUSDT': [-5.57, 1.27, -4.68, 3.06, -5.27, 1.88, -4.85, 3.73, -4.02, 1.8], 'MANAUSDT': [-6.12, 0.54, -4.57, 3.87, -5.38, 3.76], 'MASKUSDT': [-7.77, 5.59, -5.32, 0.93], 'MATICUSDT': [-5.71, 3.01, -4.13, 0.26, -5.1, 1.59, -4.24, 4.25], 'MAVUSDT': [-5.27, 1.14, -5.31, 1.64, -6.58, 4.37, -5.6, 2.79, -4.47, 3.94], 'MBLUSDT': [-9.75, 3.24, -8.55, 4.55, -4.37, 9.11, -5.22, 5.0, -4.04, 1.27, -5.76, 0.99, -4.1, 4.17, -5.84, 1.65], 'MBOXUSDT': [-6.85, 1.88], 'NEOUSDT': [-5.08, 0.94, -4.07, 2.08, -5.75, 3.9], 'NKNUSDT': [-4.93, 1.24], 'NMRUSDT': [-4.28, 0.41], 'NULSUSDT': [-4.31, 0.98], 'OAXUSDT': [-10.0, 0.79], 'OCEANUSDT': [-5.99, 0.44, -7.68, 3.53, -4.09, 0.93], 'OGNUSDT': [-5.1, 0.4, -4.34, 3.61], 'OGUSDT': [-5.76, 5.38], 'OMGUSDT': [-5.93, 0.64, -16.96, 2.61, -4.19, 1.04], 'ONEUSDT': [-7.75, 0.43, -4.73, 3.7, -4.41, 4.5, -5.85, 3.35, -4.53, 1.16], 'ORDIUSDT': [-5.7, 4.65, -5.57, 4.91, -6.42, 3.42, -4.06, 6.99, -8.43, 2.13, -4.39, 1.47], 'PERPUSDT': [-5.17, 0.3, -4.44, 2.83, -4.93, 4.51, -4.16, 1.75, -4.54, 3.63], 'PHBUSDT': [-4.5, 0.69, -4.83, 2.88, -4.96, 2.04, -5.76, 4.34], 'PNTUSDT': [-13.8, 0.06], 'POLSUSDT': [-4.11, 3.23], 'POLYXUSDT': [-4.94, 4.53], 'POWRUSDT': [-4.21, 6.5, -5.61, 1.73], 'RAYUSDT': [-5.69, 3.93, -4.81, 3.77, -5.12, 4.77, -5.26, 7.26, -5.64, 2.07, -5.08, 4.59, -4.67, 1.69], 'RDNTUSDT': [-4.89, 1.53, -4.36, 3.57], 'REEFUSDT': [-6.03, 0.43, -4.86, 4.1], 'RENUSDT': [-5.05, 0.59, -4.54, 3.33, -4.02, 4.41], 'REQUSDT': [-4.06, 0.12], 'RIFUSDT': [-4.06, 1.94, -5.19, 5.5], 'RLCUSDT': [-5.44, 0.24, -4.66, 2.74, -4.06, 2.48, -6.73, 4.97], 'RNDRUSDT': [-7.21, 0.3, -4.98, 4.5, -5.51, 1.93, -4.09, 5.17], 'ROSEUSDT': [-4.19, 1.45, -4.04, 2.38], 'RPLUSDT': [-7.65, 0.07, -4.46, 0.64], 'RSRUSDT': [-4.31, 0.62, -4.82, 1.37, -5.39, 3.87, -4.26, 2.18, -4.36, 3.66], 'RUNEUSDT': [-4.33, 2.97, -7.35, 8.71, -5.45, 0.97], 'SNTUSDT': [-4.92, 3.72], 'SNXUSDT': [-6.28, 2.51, -5.98, 0.5, -6.95, 8.07], 'SOLUSDT': [-4.64, 2.69, -5.89, 5.91, -4.77, 9.21, -7.85, 4.56, -5.63, 6.63], 'SPELLUSDT': [-5.51, 0.39], 'SSVUSDT': [-8.2, 1.36, -5.83, 3.39, -4.54, 3.9], 'STEEMUSDT': [-5.33, 2.85], 'STGUSDT': [-5.27, 0.18, -6.16, 2.45], 'STMXUSDT': [-5.76, 0.98, -5.15, 4.1], 'STORJUSDT': [-4.99, 2.28, -9.02, 4.42, -4.35, 2.67], 'STRAXUSDT': [-5.5, 3.1, -5.08, 0.98], 'STXUSDT': [-6.32, 2.62], 'SUIUSDT': [-4.24, 4.23, -5.9, 0.61, -6.84, 5.98, -4.88, 1.96, -6.1, 1.59, -4.81, 4.05], 'TOMOUSDT': [-5.18, 1.67], 'TRBUSDT': [-4.66, 6.36], 'TRUUSDT': [-6.1, 0.93, -4.7, 2.99, -7.21, 5.76, -4.46, 1.04], 'TVKUSDT': [-5.51, 3.55, -4.01, 6.89, -4.77, 0.33, -4.78, 8.06, -4.97, 4.24, -10.79, 11.78, -4.84, 3.39], 'UFTUSDT': [-4.82, 3.61], 'UMAUSDT': [-5.28, 0.56, -4.19, 1.97, -4.56, 6.67], 'UNFIUSDT': [-4.41, 0.22], 'WAVESUSDT': [-4.32, 0.14, -4.11, 3.68], 'WAXPUSDT': [-4.64, 3.7], 'WLDUSDT': [-7.32, 0.09, -5.58, 4.92, -4.79, 3.63, -9.36, 2.09, -4.84, 0.43, -5.44, 1.77], 'WOOUSDT': [-6.32, 0.25, -5.44, 3.74, -7.46, 4.64], 'WTCUSDT': [-4.09, 0.18], 'HIFIUSDT': [-14.47, 2.68, -4.68, 5.99, -5.17, 5.91, -4.16, 0.99], 'CREAMUSDT': [-11.0, 2.36, -4.27, 1.33], 'QIUSDT': [-5.78, 4.01, -4.23, 1.02, -7.85, 0.43, -7.3, 3.6, -11.91, 6.97, -13.51, 1.88, -4.72, 1.85, -4.85, 1.55, -4.29, 5.48], 'ALICEUSDT': [-5.8, 0.21, -4.24, 5.8], 'ALPHAUSDT': [-5.09, 0.35, -9.43, 7.22], 'AMBUSDT': [-4.83, 1.66, -4.67, 3.3, -6.31, 1.98, -4.34, 0.68, -4.91, 4.56], 'AMPUSDT': [-4.17, 0.5, -6.88, 7.83, -4.27, 0.75], 'ANKRUSDT': [-5.18, 3.99], 'ANTUSDT': [-4.05, 1.4], 'APEUSDT': [-5.34, 1.02, -6.0, 3.11, -5.3, 3.77], 'API3USDT': [-4.21, 0.14, -4.16, 3.26], 'AUDIOUSDT': [-5.03, 0.37, -4.25, 0.0], 'AVAXUSDT': [-4.29, 1.68, -7.01, 4.05, -4.22, 2.33, -8.09, 7.27, -5.43, 2.12], 'AXSUSDT': [-5.2, 0.97, -4.22, 3.11, -4.94, 3.8, -4.81, 1.15], 'BADGERUSDT': [-4.28, 9.29, -4.56, 2.08, -4.63, 2.96, -4.71, 4.71, -4.9, 3.26, -6.52, 1.21, -5.11, 0.78], 'BAKEUSDT': [-6.47, 0.62, -5.68, 3.65, -4.47, 1.67], 'BANDUSDT': [-5.95, 0.75, -4.92, 5.71], 'BARUSDT': [-5.56, 0.87], 'BATUSDT': [-4.13, 3.0, -4.55, 2.02], 'ARKUSDT': [-8.28, 10.99, -12.67, 0.43, -4.81, 0.82, -15.71, 0.4], 'ZENUSDT': [-5.31, 2.33, -4.51, 2.56, -4.71, 3.76], 'ZRXUSDT': [-10.21, 1.72, -5.35, 3.92, -5.66, 8.28, -4.82, 2.27, -4.63, 4.26, -11.25, 1.18, -7.88, 0.02, -6.51, 2.38, -7.32, 5.23, -6.62, 0.86, -4.09, 2.03], 'BURGERUSDT': [-7.41, 0.53], 'C98USDT': [-5.07, 1.96, -4.06, 4.12], 'CAKEUSDT': [-6.86, 1.34, -4.4, 2.44, -4.63, 2.32, -6.06, 3.84, -4.59, 1.08], 'CELRUSDT': [-5.63, 0.52, -4.46, 2.28, -5.4, 2.63, -6.44, 3.38], 'CFXUSDT': [-4.76, 1.22, -4.05, 2.43, -5.09, 1.59, -5.74, 4.3, -4.11, 1.55], 'CHESSUSDT': [-4.84, 0.18, -4.55, 4.35, -4.16, 3.99], 'CHZUSDT': [-5.22, 0.8, -4.12, 3.11], 'CVXUSDT': [-4.23, 2.97], 'CYBERUSDT': [-9.34, 1.48, -5.0, 4.15, -4.61, 5.0, -6.88, 0.01, -4.97, 1.92, -5.76, 3.71, -4.04, 1.06], 'DARUSDT': [-4.13, 2.94, -4.04, 3.06, -4.1, 1.17, -5.59, 3.93], 'DCRUSDT': [-4.86, 3.85], 'DEGOUSDT': [-4.89, 0.41], 'DENTUSDT': [-5.46, 0.36], 'DEXEUSDT': [-9.12, 2.51, -5.92, 2.89, -13.94, 7.81, -4.07, 1.37], 'ENJUSDT': [-5.94, 0.47, -4.56, 1.87, -4.75, 4.53], 'ENSUSDT': [-5.02, 0.57, -4.49, 3.64, -6.21, 3.73], 'ETCUSDT': [-4.41, 0.65, -4.58, 3.49], 'FARMUSDT': [-19.33, 2.17, -9.85, 8.64, -7.15, 2.0], 'FETUSDT': [-4.15, 4.37, -4.25, 0.82, -7.62, 1.32, -4.8, 4.55, -4.1, 3.37, -6.34, 6.66, -6.13, 1.02], 'FIDAUSDT': [-4.49, 0.56, -4.62, 4.08, -4.04, 3.23], 'GFTUSDT': [-9.48, 8.97, -6.65, 4.01, -5.34, 2.63], 'FTMUSDT': [-4.04, 5.9, -6.01, 3.92, -5.68, 4.68, -5.17, 0.55], 'FUNUSDT': [-5.7, 2.2], 'FXSUSDT': [-7.17, 4.72, -4.96, 4.08, -4.65, 2.26], 'GALAUSDT': [-6.65, 0.58, -5.62, 6.39, -6.66, 1.88], 'GALUSDT': [-5.62, 0.27, -5.13, 1.63, -4.28, 0.72], 'GLMRUSDT': [-5.01, 0.35, -4.63, 3.92], 'GLMUSDT': [-6.17, 8.65, -4.85, 16.05, -12.73, 2.73, -5.27, 1.93], 'GMTUSDT': [-4.7, 3.59, -6.02, 3.8, -6.57, 1.19], 'GMXUSDT': [-4.11, 0.66], 'GASUSDT': [-26.82, 5.47, -4.13, 3.66, -5.55, 5.23, -4.93, 4.98, -4.07, 0.06], 'ICXUSDT': [-7.77, 4.99, -10.41, 3.42, -4.64, 1.53, -4.79, 1.18, -4.23, 3.03, -5.16, 5.87], 'IDEXUSDT': [-5.01, 0.39, -4.04, 2.85, -4.65, 3.47], 'IDUSDT': [-5.92, 0.46, -6.1, 3.62, -4.48, 2.12, -6.28, 0.82, -4.21, 0.94, -4.89, 4.58], 'ILVUSDT': [-10.12, 2.84, -4.6, 2.92, -6.19, 2.57, -5.2, 3.69], 'IMXUSDT': [-4.74, 4.08, -5.7, 0.72, -6.96, 2.36, -5.65, 3.27, -5.47, 5.67, -5.67, 1.19], 'INJUSDT': [-4.91, 2.85, -5.09, 1.43, -4.08, 1.39], 'IOTXUSDT': [-6.21, 1.27, -4.64, 4.52], 'IRISUSDT': [-4.02, 1.69], 'LDOUSDT': [-10.29, 0.71, -5.23, 0.21], 'LEVERUSDT': [-5.23, 0.21, -5.24, 3.1, -4.75, 0.07, -4.17, 3.3], 'LINAUSDT': [-5.26, 5.56, -5.06, 2.59, -4.19, 3.35], 'LINKUSDT': [-4.21, 3.39, -5.52, 2.77], 'LITUSDT': [-5.25, 0.37, -4.35, 3.46, -5.01, 4.19], 'LOKAUSDT': [-5.38, 1.15, -4.49, 3.42], 'LOOMUSDT': [-5.92, 1.65, -4.87, 2.23, -5.06, 3.32, -4.1, 3.83], 'LQTYUSDT': [-4.26, 1.84], 'LRCUSDT': [-5.53, 1.05, -4.29, 2.69], 'MDTUSDT': [-4.94, 1.13, -4.49, 2.59, -4.07, 2.21], 'MINAUSDT': [-4.92, 2.86, -4.15, 2.11], 'MOBUSDT': [-6.76, 3.19, -4.2, 2.49, -4.1, 1.29], 'MULTIUSDT': [-4.08, 2.08], 'NEARUSDT': [-4.71, 1.76, -8.93, 1.67, -4.67, 3.39, -4.82, 0.45, -4.6, 5.02, -6.79, 1.02], 'MEMEUSDT': [-5.04, 5.76, -4.65, 2.34, -7.53, 10.2, -7.77, 13.05, -12.78, 6.24, -7.34, 1.72, -5.67, 2.29, -14.22, 5.66, -6.35, 2.71], 'ONGUSDT': [-7.06, 2.5], 'ONTUSDT': [-4.35, 1.95, -4.08, 3.44], 'OOKIUSDT': [-5.03, 0.85, -4.71, 1.57], 'OPUSDT': [-4.3, 0.67], 'ORNUSDT': [-13.61, 2.15, -6.16, 4.3, -5.12, 3.55], 'OSMOUSDT': [-7.43, 2.39], 'OXTUSDT': [-5.94, 0.55], 'PENDLEUSDT': [-4.79, 0.31, -4.19, 1.16, -7.56, 4.22], 'PEOPLEUSDT': [-5.55, 0.52, -4.56, 3.36, -6.45, 2.75], 'NTRNUSDT': [-5.92, 7.12, -10.37, 5.14, -5.89, 5.13, -17.62, 20.88, -9.91, 14.36, -8.23, 5.91, -4.72, 0.8, -7.1, 1.44, -5.54, 2.02, -4.07, 2.38, -5.14, 1.76, -5.15, 4.97, -4.87, 1.65, -4.74, 2.48], 'PROSUSDT': [-5.55, 3.92], 'PYRUSDT': [-4.58, 3.85, -4.03, 4.78, -4.02, 6.31, -9.58, 3.33, -5.63, 1.83, -5.54, 8.51, -4.21, 0.13, -4.66, 1.44, -5.35, 6.3, -4.57, 2.55], 'QTUMUSDT': [-5.03, 3.78], 'QUICKUSDT': [-4.77, 1.0], 'RADUSDT': [-4.52, 0.13, -4.23, 2.0], 'RVNUSDT': [-5.0, 0.81, -4.1, 2.98, -4.32, 3.17], 'SANDUSDT': [-4.48, 1.22, -4.16, 2.86, -4.83, 2.83, -6.86, 4.05, -4.06, 1.06], 'SCRTUSDT': [-4.19, 1.97, -6.9, 1.8, -5.99, 2.74], 'SEIUSDT': [-4.3, 5.6, -6.43, 4.72, -4.34, 3.91, -5.79, 2.38, -6.23, 2.59, -5.64, 1.57, -4.28, 3.63], 'SFPUSDT': [-4.12, 1.03], 'SHIBUSDT': [-4.38, 3.43], 'SKLUSDT': [-5.81, 0.68, -4.52, 3.74, -6.82, 6.07, -5.36, 2.32], 'SLPUSDT': [-4.18, 3.54], 'SUPERUSDT': [-9.78, 2.36, -4.03, 0.34, -4.84, 0.09, -4.09, 2.67], 'SUSHIUSDT': [-6.04, 1.72, -5.07, 0.62, -4.27, 4.29, -4.17, 2.88, -8.1, 2.09, -10.06, 2.03], 'SXPUSDT': [-4.16, 2.67, -4.25, 1.91, -4.13, 0.85, -4.43, 3.41], 'SYNUSDT': [-5.68, 0.51, -9.1, 0.58, -4.35, 3.02, -7.85, 4.9, -4.47, 2.44], 'SYSUSDT': [-4.77, 0.2], 'THETAUSDT': [-4.64, 3.56, -6.21, 2.59], 'TKOUSDT': [-4.8, 2.3, -4.39, 3.05], 'TLMUSDT': [-5.02, 0.3, -4.56, 3.68], 'TIAUSDT': [-18.83, 14.16, -4.3, 0.8, -4.26, 6.95, -5.86, 8.68, -6.39, 5.94, -5.7, 4.95], 'UNIUSDT': [-5.11, 0.61, -4.31, 2.52, -4.16, 2.39, -4.89, 3.85], 'VETUSDT': [-4.62, 2.63], 'VGXUSDT': [-11.65, 4.11, -4.1, 1.67, -5.23, 4.19, -4.54, 0.44], 'VIBUSDT': [-7.68, 4.16, -5.98, 13.5, -6.86, 3.81], 'VIDTUSDT': [-4.05, 1.26, -7.61, 0.29, -4.48, 3.09, -4.57, 2.46, -4.54, 5.07], 'VITEUSDT': [-4.16, 0.13, -4.13, 1.36], 'VOXELUSDT': [-4.31, 0.1, -5.88, 1.33, -4.16, 4.31], 'XECUSDT': [-4.91, 3.47], 'XEMUSDT': [-4.95, 2.03, -4.99, 4.11], 'XRPUSDT': [-5.01, 1.71], 'XVGUSDT': [-6.17, 0.51, -4.8, 2.9, -5.88, 4.08], 'YFIUSDT': [-9.39, 5.26, -8.24, 6.12, -7.79, 6.56, -6.28, 7.91, -14.95, 2.03, -38.36, 1.65]}

h1 = {'1INCHUSDT': [-4.64, 2.08], 'AAVEUSDT': [-4.07, 1.81], 'ADAUSDT': [-4.18, 1.99], 'AERGOUSDT': [-5.43, 11.5, -9.96, 5.97, -4.02, 1.52, -5.03, 0.26, -4.05, 0.62, -5.17, 3.19], 'APTUSDT': [-4.28, 2.05], 'ARDRUSDT': [-6.34, 1.46, -4.61, 1.63, -5.95, 8.95, -4.07, 0.0], 'ARKMUSDT': [-5.61, 2.49, -4.09, 3.05, -6.28, 1.8, -5.61, 3.27, -5.22, 0.28, -4.32, 0.32], 'ARPAUSDT': [-5.66, 1.45], 'ARUSDT': [-4.33, 1.21, -4.69, 1.09], 'ATMUSDT': [-4.39, 0.32], 'BEAMXUSDT': [-13.0, 6.92, -8.76, 3.61, -4.94, 6.02, -4.05, 4.55, -4.37, 1.32, -4.21, 3.27, -5.21, 4.62, -4.86, 0.16, -5.14, 3.16, -4.18, 2.05], 'BICOUSDT': [-5.09, 0.62], 'BLZUSDT': [-4.9, 2.7, -5.62, 2.25], 'BNXUSDT': [-6.5, 1.77], 'BONDUSDT': [-6.18, 2.24, -4.31, 0.45, -4.29, 0.58], 'YGGUSDT': [-4.07, 1.48, -4.39, 2.66, -4.62, 0.68], 'COMPUSDT': [-4.16, 1.47], 'COTIUSDT': [-4.45, 1.58], 'CRVUSDT': [-4.54, 2.49], 'CTSIUSDT': [-4.55, 1.41, -5.89, 1.26], 'CTXCUSDT': [-6.44, 8.13, -4.9, 4.02, -4.72, 2.53, -5.24, 2.25, -4.95, 1.37], 'CVCUSDT': [-5.84, 7.43, -9.21, 5.29, -6.73, 3.06, -16.01, 1.38, -15.15, 4.21], 'DYDXUSDT': [-4.55, 0.72, -4.36, 1.37, -7.24, 0.89, -5.77, 0.55, -6.34, 2.16, -4.24, 3.07], 'EDUUSDT': [-4.37, 1.63], 'EGLDUSDT': [-4.38, 1.11], 'ELFUSDT': [-4.41, 0.25], 'FTTUSDT': [-7.05, 9.82, -5.53, 1.91, -4.91, 4.12, -5.54, 1.45, -4.46, 6.88, -5.13, 0.0, -6.25, 2.47, -4.27, 4.32, -6.97, 0.97, -5.27, 1.42, -8.2, 3.27, -6.66, 3.24], 'FILUSDT': [-4.99, 1.97], 'FIROUSDT': [-5.02, 1.68], 'FLOKIUSDT': [-4.01, 1.7, -4.24, 0.97, -4.78, 4.09], 'FRONTUSDT': [-4.63, 1.52, -4.15, 1.76], 'GRTUSDT': [-4.26, 2.13], 'HOOKUSDT': [-5.06, 2.33], 'JASMYUSDT': [-5.18, 3.16], 'JOEUSDT': [-4.84, 1.69], 'JUVUSDT': [-7.76, 4.28, -4.56, 0.36, -4.45, 4.39], 'KAVAUSDT': [-4.38, 2.46], 'KLAYUSDT': [-5.4, 2.6], 'KP3RUSDT': [-8.12, 0.96, -4.86, 4.87, -7.2, 0.16, -4.55, 0.8, -5.21, 3.62, -8.25, 2.67, -7.03, 1.48], 'LUNAUSDT': [-8.72, 3.15, -5.67, 1.04, -4.98, 1.98], 'MAGICUSDT': [-5.06, 2.48], 'MANAUSDT': [-4.25, 2.5], 'MAVUSDT': [-6.46, 0.26, -4.08, 3.52, -6.0, 2.56], 'MBLUSDT': [-5.6, 2.65, -12.62, 1.49, -4.73, 3.1, -4.99, 1.32, -9.51, 5.71, -5.98, 1.33], 'MBOXUSDT': [-4.18, 0.61, -4.52, 0.39], 'NEOUSDT': [-4.05, 1.59, -4.68, 2.11], 'OAXUSDT': [-4.02, 1.84, -7.13, 0.79], 'OCEANUSDT': [-4.05, 1.64, -4.49, 4.69], 'OGUSDT': [-4.05, 6.89, -4.32, 0.56, -6.71, 0.89], 'OMGUSDT': [-9.47, 0.96, -4.51, 1.48], 'ONEUSDT': [-5.01, 1.89, -5.1, 2.19], 'ORDIUSDT': [-5.18, 0.28, -5.94, 1.87, -5.25, 2.61, -6.14, 8.97, -5.63, 1.59], 'PERPUSDT': [-4.08, 1.95, -5.84, 2.36], 'PHAUSDT': [-4.06, 2.24], 'PNTUSDT': [-5.05, 4.39, -4.02, 8.76, -5.04, 8.16, -6.17, 3.48, -10.32, 2.22, -4.71, 0.85], 'POLYXUSDT': [-4.05, 1.55], 'RAYUSDT': [-4.41, 3.54, -4.73, 1.83, -6.45, 0.53, -4.87, 3.16, -4.14, 1.91, -4.24, 0.71], 'REEFUSDT': [-4.19, 2.02], 'RENUSDT': [-4.43, 2.25, -4.94, 1.93], 'RIFUSDT': [-4.06, 1.55, -4.57, 2.76], 'RLCUSDT': [-4.11, 1.51], 'RNDRUSDT': [-4.8, 1.52, -4.3, 5.17], 'RSRUSDT': [-4.59, 1.52], 'RUNEUSDT': [-5.47, 3.43, -5.52, 2.25, -6.36, 4.34], 'SNTUSDT': [-4.66, 2.64], 'SOLUSDT': [-4.01, 2.51], 'SSVUSDT': [-4.67, 1.25], 'STEEMUSDT': [-5.92, 2.27, -5.82, 2.55, -4.15, 1.67], 'STMXUSDT': [-6.48, 2.34, -4.56, 1.7], 'STORJUSDT': [-4.61, 2.66, -5.36, 0.57, -8.99, 1.47], 'SUIUSDT': [-4.08, 2.14], 'TOMOUSDT': [-4.02, 2.25], 'TRBUSDT': [-4.06, 2.15], 'TRUUSDT': [-4.42, 1.12, -4.33, 1.82], 'TVKUSDT': [-4.45, 2.62, -5.48, 1.87, -5.18, 2.24], 'WAVESUSDT': [-4.02, 1.93, -4.44, 2.03], 'WLDUSDT': [-8.48, 5.2, -5.92, 3.2, -4.78, 1.9, -5.59, 1.17, -6.57, 2.91], 'WOOUSDT': [-4.59, 3.17], 'HIFIUSDT': [-12.85, 0.91, -5.78, 6.64, -4.68, 0.9, -4.55, 2.37], 'CREAMUSDT': [-9.41, 2.29, -4.01, 3.52, -8.5, 2.67, -8.53, 9.02], 'QIUSDT': [-5.57, 0.96, -5.02, 7.1, -4.44, 1.49, -5.06, 0.21, -4.06, 1.08, -7.35, 0.63, -4.5, 0.22, -4.09, 0.24], 'ALICEUSDT': [-4.11, 1.22, -5.25, 1.79, -4.05, 0.53], 'AMBUSDT': [-5.52, 1.77], 'AMPUSDT': [-4.12, 3.87, -5.4, 0.13], 'ANKRUSDT': [-4.55, 2.74], 'AUDIOUSDT': [-4.19, 1.35], 'AVAXUSDT': [-4.98, 1.03, -4.05, 3.3, -4.16, 2.88, -4.22, 2.75], 'AXSUSDT': [-4.07, 1.6, -4.08, 1.51], 'BADGERUSDT': [-6.47, 1.86, -5.41, 1.02, -5.97, 3.27, -4.96, 0.9], 'BAKEUSDT': [-5.22, 1.66], 'BATUSDT': [-4.17, 1.14], 'ARKUSDT': [-4.56, 0.99, -6.01, 2.08, -19.1, 5.58, -4.71, 2.9, -4.85, 5.03, -4.78, 4.08, -17.59, 3.77], 'ZRXUSDT': [-5.86, 0.13, -7.25, 2.48, -6.11, 3.06, -4.88, 1.05, -4.08, 7.77, -4.11, 1.96, -6.38, 0.93, -4.35, 1.18, -4.62, 0.02, -4.23, 0.35, -4.72, 3.16, -4.39, 1.44, -4.19, 0.67], 'BURGERUSDT': [-5.78, 0.75], 'CAKEUSDT': [-8.68, 3.5], 'CELRUSDT': [-4.18, 1.17], 'CFXUSDT': [-4.39, 2.06], 'CHESSUSDT': [-4.25, 1.92], 'CYBERUSDT': [-4.89, 1.0, -4.07, 3.57], 'DARUSDT': [-4.35, 1.26, -4.48, 1.94, -4.95, 1.24], 'DEXEUSDT': [-4.65, 0.0, -4.33, 0.38, -9.37, 2.23, -4.04, 1.95], 'ENJUSDT': [-4.05, 2.3], 'FARMUSDT': [-5.33, 0.62, -8.67, 0.92, -7.87, 2.82, -4.01, 1.6, -7.09, 1.88, -5.82, 5.48, -4.83, 0.27, -4.86, 3.48, -5.54, 3.89, -6.38, 4.16], 'FETUSDT': [-4.1, 1.14, -4.01, 3.9, -4.92, 0.11], 'FIDAUSDT': [-5.59, 1.32], 'GFTUSDT': [-4.37, 1.82, -5.95, 3.7, -9.09, 4.49, -4.96, 4.23, -4.49, 1.82], 'FTMUSDT': [-4.55, 2.17], 'FXSUSDT': [-6.02, 1.21], 'GALAUSDT': [-4.29, 1.79, -4.61, 0.8, -4.43, 1.11, -4.36, 2.47], 'GALUSDT': [-4.53, 1.44], 'GLMUSDT': [-4.37, 1.88, -5.0, 1.18, -4.13, 3.08, -25.4, 2.73, -6.69, 2.69], 'GASUSDT': [-8.65, 4.54, -12.87, 1.44, -6.05, 1.36, -8.76, 4.89, -12.55, 5.21, -6.58, 3.27, -5.25, 2.07, -4.76, 3.21, -6.18, 4.06, -5.55, 2.49], 'ICXUSDT': [-4.23, 20.98, -6.88, 4.16, -4.66, 0.1, -6.74, 3.03, -5.0, 1.42], 'IDEXUSDT': [-4.02, 2.14], 'IDUSDT': [-4.11, 2.23, -5.36, 2.89], 'ILVUSDT': [-5.23, 2.84, -4.44, 3.09], 'IMXUSDT': [-6.21, 1.76, -4.14, 2.58], 'IOTXUSDT': [-4.59, 0.71], 'LDOUSDT': [-4.65, 0.8, -6.26, 1.21, -4.07, 2.51, -4.66, 0.75], 'LEVERUSDT': [-4.39, 1.95], 'LINAUSDT': [-5.66, 1.09, -4.06, 1.59, -4.28, 1.07, -6.2, 2.96, -4.9, 4.52], 'LINKUSDT': [-4.68, 1.62], 'LOKAUSDT': [-4.13, 2.93], 'LOOMUSDT': [-5.07, 0.58], 'LQTYUSDT': [-4.35, 0.76, -4.25, 3.4], 'MINAUSDT': [-4.06, 1.18, -4.2, 2.16], 'MOBUSDT': [-5.3, 1.02], 'MTLUSDT': [-4.28, 3.18, -4.56, 2.14], 'MULTIUSDT': [-4.87, 1.54], 'NEARUSDT': [-5.85, 1.75], 'MEMEUSDT': [-6.18, 2.37, -4.12, 9.05, -5.42, 5.1, -15.34, 10.2, -4.3, 2.18, -5.01, 3.13, -5.38, 2.37, -4.47, 3.26, -4.23, 1.95, -4.58, 1.98, -4.03, 0.76, -4.9, 4.66, -8.47, 1.72, -4.11, 1.86, -7.89, 0.53, -5.51, 3.26, -6.38, 1.27], 'ONGUSDT': [-6.34, 1.54], 'OPUSDT': [-4.11, 2.1], 'ORNUSDT': [-6.43, 0.94, -4.14, 1.09, -4.18, 0.24], 'OXTUSDT': [-4.09, 0.81], 'PENDLEUSDT': [-4.01, 2.03], 'PEOPLEUSDT': [-5.11, 1.52], 'NTRNUSDT': [-4.88, 2.33, -9.61, 11.32, -9.03, 5.14, -6.55, 3.17, -5.38, 1.66, -8.57, 2.21, -6.75, 0.21, -11.66, 3.62, -4.94, 0.55, -4.08, 5.11, -5.96, 2.7, -4.47, 3.46, -4.59, 1.77, -4.03, 0.22, -9.14, 3.26], 'PUNDIXUSDT': [-4.23, 1.67], 'PYRUSDT': [-4.93, 0.95, -4.06, 1.16, -4.83, 5.92], 'QKCUSDT': [-5.67, 5.46, -6.26, 0.06], 'QTUMUSDT': [-4.09, 1.6], 'QUICKUSDT': [-4.33, 1.87, -4.22, 0.29], 'SANDUSDT': [-4.14, 1.94], 'SANTOSUSDT': [-4.98, 3.03], 'SCUSDT': [-5.9, 2.59, -7.1, 5.58], 'SEIUSDT': [-5.35, 2.21, -4.01, 1.21, -4.43, 2.13, -5.93, 2.67, -4.19, 1.09], 'SFPUSDT': [-4.18, 1.55], 'SUPERUSDT': [-4.19, 1.27, -5.95, 2.05], 'SUSHIUSDT': [-4.3, 0.94, -5.3, 0.09], 'SXPUSDT': [-4.15, 1.73], 'SYNUSDT': [-4.78, 0.64, -4.98, 0.82, -4.28, 1.02, -6.98, 0.08], 'TLMUSDT': [-4.17, 2.38], 'TIAUSDT': [-4.03, 11.35, -5.43, 3.99, -5.1, 1.6, -8.99, 4.78, -6.7, 2.31, -5.07, 3.59, -12.47, 4.11, -6.11, 5.63, -5.54, 2.25, -6.37, 0.93, -4.07, 6.74, -4.73, 3.81], 'UNIUSDT': [-4.05, 1.01], 'VETUSDT': [-4.67, 1.95], 'VGXUSDT': [-8.4, 0.07, -4.93, 2.17, -4.48, 2.06, -6.24, 2.35], 'VIBUSDT': [-4.41, 2.96, -4.01, 0.56], 'VIDTUSDT': [-4.33, 1.93], 'XEMUSDT': [-4.05, 1.19], 'XLMUSDT': [-8.02, 0.98], 'XRPUSDT': [-8.61, 0.86, -5.93, 2.2], 'XVGUSDT': [-4.36, 1.13, -4.27, 0.8], 'YFIUSDT': [-5.53, 1.83, -5.53, 1.46, -7.17, 4.09, -6.78, 2.03, -16.12, 2.91, -21.49, 5.98]}



