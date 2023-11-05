import time
from datetime import datetime
from decimal import Decimal, ROUND_FLOOR
from threading import Thread

import pymysql
from binance.client import Client, AsyncClient
from binance.exceptions import BinanceAPIException
from sql_request import sql_req
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

def last_data(symbol, interval, lookback):
    frame = pd.DataFrame(client.get_historical_klines(symbol, interval, lookback + 'min ago UTC'))
    frame = frame.iloc[:, :6]
    frame.columns = ['Time', 'Open', 'High', 'Low', 'Close', 'Volume']
    frame = frame.set_index('Time')
    frame.index = pd.to_datetime(frame.index, unit='ms')
    frame = frame.astype(float)
    # frame.to_csv('file1.csv')
    # print(frame["Volume"].sum())
    return Dataset(high_price=[i.High for i in frame.itertuples()], volume=[i.Volume for i in frame.itertuples()], close_price=[i.Close for i in
                                                                                          frame.itertuples()], open_price=[i.Open for i in
                                                                                          frame.itertuples()])


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

one = ['1INCHUSDT', 'AAVEUSDT', 'ACAUSDT', 'ACHUSDT', 'ACMUSDT', 'ADAUSDT', 'ADXUSDT', 'AERGOUSDT', 'AGIXUSDT',
       'AGLDUSDT', 'AKROUSDT', 'ALCXUSDT', 'ALGOUSDT', 'ALICEUSDT', 'ALPACAUSDT', 'ALPHAUSDT', 'ALPINEUSDT', 'AMBUSDT',
       'AMPUSDT', 'ANKRUSDT', 'ANTUSDT', 'APEUSDT', 'API3USDT']

two = ['APTUSDT', 'ARBUSDT', 'ARDRUSDT', 'ARKMUSDT', 'ARPAUSDT', 'ARUSDT', 'ASRUSDT', 'ASTRUSDT', 'ASTUSDT', 'ATAUSDT',
       'ATMUSDT', 'ATOMUSDT', 'AUCTIONUSDT', 'AUDIOUSDT', 'AVAUSDT', 'AVAXUSDT', 'AXSUSDT', 'BADGERUSDT', 'BAKEUSDT',
       'BALUSDT', 'BANDUSDT', 'BARUSDT', 'BATUSDT']

three = ['BCHUSDT', 'BELUSDT', 'BETAUSDT', 'BETHUSDT', 'BICOUSDT', 'BIFIUSDT', 'BLZUSDT', 'BNTUSDT', 'BNXUSDT',
         'BONDUSDT', 'BSWUSDT', 'BTSUSDT', 'YGGUSDT', 'ZECUSDT', 'ZENUSDT', 'ZILUSDT', 'ZRXUSDT', 'BURGERUSDT',
         'BUSDUSDT', 'C98USDT', 'CAKEUSDT', 'CELOUSDT', 'CELRUSDT', 'CFXUSDT', 'CHESSUSDT', 'CHRUSDT', 'CHZUSDT']

four = ['CITYUSDT', 'CKBUSDT', 'CLVUSDT', 'COMBOUSDT', 'COMPUSDT', 'COSUSDT', 'COTIUSDT', 'CRVUSDT', 'CTKUSDT',
        'CTSIUSDT', 'CTXCUSDT', 'CVCUSDT', 'CVPUSDT', 'CVXUSDT', 'CYBERUSDT', 'DARUSDT', 'DASHUSDT', 'DATAUSDT',
        'DCRUSDT', 'DEGOUSDT', 'DENTUSDT', 'DEXEUSDT', 'DFUSDT']

five = ['DGBUSDT', 'DIAUSDT', 'DOCKUSDT', 'DODOUSDT', 'DOGEUSDT', 'DOTUSDT', 'DREPUSDT', 'DUSKUSDT', 'DYDXUSDT',
        'EDUUSDT', 'EGLDUSDT', 'ELFUSDT', 'ENJUSDT', 'ENSUSDT', 'EPXUSDT', 'ERNUSDT', 'ETCUSDT', 'EURUSDT', 'FARMUSDT',
        'FDUSDUSDT', 'FETUSDT', 'FIDAUSDT']

six = ['FILUSDT', 'FIOUSDT', 'FIROUSDT', 'FISUSDT', 'FLMUSDT', 'FLOKIUSDT', 'FLOWUSDT', 'FLUXUSDT', 'FORTHUSDT',
       'FORUSDT', 'FRONTUSDT', 'FTMUSDT', 'FUNUSDT', 'FXSUSDT', 'GALAUSDT', 'GALUSDT', 'GASUSDT', 'GBPUSDT', 'GHSTUSDT',
       'GLMRUSDT', 'GLMUSDT', 'GMTUSDT', 'GMXUSDT']

seven = ['GNOUSDT', 'GNSUSDT', 'GRTUSDT', 'GTCUSDT', 'HARDUSDT', 'HBARUSDT', 'HFTUSDT', 'HIFIUSDT', 'HIGHUSDT',
         'HIVEUSDT', 'HOOKUSDT', 'HOTUSDT', 'ICPUSDT', 'ICXUSDT', 'IDEXUSDT', 'IDUSDT', 'ILVUSDT', 'IMXUSDT', 'INJUSDT',
         'IOSTUSDT', 'IOTAUSDT', 'IOTXUSDT', 'IRISUSDT']

eight = ['JASMYUSDT', 'JOEUSDT', 'JSTUSDT', 'JUVUSDT', 'KAVAUSDT', 'KDAUSDT', 'KEYUSDT', 'KLAYUSDT', 'KMDUSDT',
         'KNCUSDT', 'KP3RUSDT', 'KSMUSDT', 'LAZIOUSDT', 'LDOUSDT', 'LEVERUSDT', 'LINAUSDT', 'LINKUSDT', 'LITUSDT',
         'LOKAUSDT', 'LOOMUSDT', 'LPTUSDT', 'LQTYUSDT', 'LRCUSDT']

nine = ['LSKUSDT', 'LTCUSDT', 'LTOUSDT', 'LUNAUSDT', 'LUNCUSDT', 'MAGICUSDT', 'MANAUSDT', 'MASKUSDT', 'MATICUSDT',
        'MAVUSDT', 'MBLUSDT', 'MBOXUSDT', 'MCUSDT', 'MDTUSDT', 'MDXUSDT', 'MINAUSDT', 'MKRUSDT', 'MLNUSDT', 'MOBUSDT',
        'MOVRUSDT', 'MTLUSDT', 'MULTIUSDT', 'NEARUSDT']

ten = ['NEOUSDT', 'NEXOUSDT', 'NKNUSDT', 'NMRUSDT', 'NULSUSDT', 'OAXUSDT', 'OCEANUSDT', 'OGNUSDT', 'OGUSDT', 'OMGUSDT',
       'OMUSDT', 'ONEUSDT', 'ONGUSDT', 'ONTUSDT', 'OOKIUSDT', 'OPUSDT', 'ORNUSDT', 'OSMOUSDT', 'OXTUSDT', 'PAXGUSDT',
       'PENDLEUSDT', 'PEOPLEUSDT']

eleven = ['PERLUSDT', 'PERPUSDT', 'PHAUSDT', 'PHBUSDT', 'PLAUSDT', 'PNTUSDT', 'POLSUSDT', 'POLYXUSDT', 'PONDUSDT',
          'PORTOUSDT', 'POWRUSDT', 'PROMUSDT', 'PROSUSDT', 'PSGUSDT', 'PUNDIXUSDT', 'PYRUSDT', 'QIUSDT', 'QKCUSDT',
          'QNTUSDT', 'QTUMUSDT', 'QUICKUSDT', 'RADUSDT', 'RAREUSDT']

twelve = ['RAYUSDT', 'RDNTUSDT', 'REEFUSDT', 'REIUSDT', 'RENUSDT', 'REQUSDT', 'RIFUSDT', 'RLCUSDT', 'RNDRUSDT',
          'ROSEUSDT', 'RPLUSDT', 'RSRUSDT', 'RUNEUSDT', 'RVNUSDT', 'SANDUSDT', 'SANTOSUSDT', 'SCRTUSDT', 'SCUSDT',
          'SEIUSDT', 'SFPUSDT', 'SHIBUSDT', 'SKLUSDT', 'SLPUSDT']

thirteenth = ['SNTUSDT', 'SNXUSDT', 'SOLUSDT', 'SPELLUSDT', 'SSVUSDT', 'STEEMUSDT', 'STGUSDT', 'STMXUSDT', 'STORJUSDT',
              'STPTUSDT', 'STRAXUSDT', 'STXUSDT', 'SUIUSDT', 'SUNUSDT', 'SUPERUSDT', 'SUSHIUSDT', 'SXPUSDT', 'SYNUSDT',
              'SYSUSDT', 'TFUELUSDT', 'THETAUSDT', 'TKOUSDT', 'TLMUSDT']

fourteenth = ['TOMOUSDT', 'TRBUSDT', 'TROYUSDT', 'TRUUSDT', 'TRXUSDT', 'TUSDT', 'TUSDUSDT', 'TVKUSDT', 'TWTUSDT',
              'UFTUSDT', 'UMAUSDT', 'UNFIUSDT', 'UNIUSDT', 'USDCUSDT', 'USDPUSDT', 'USTCUSDT', 'UTKUSDT', 'VETUSDT',
              'VGXUSDT', 'VIBUSDT', 'VIDTUSDT', 'VITEUSDT', 'VOXELUSDT']

fifteenth = ['VTHOUSDT', 'WANUSDT', 'WAVESUSDT', 'WAXPUSDT', 'WBETHUSDT', 'WBTCUSDT', 'WINGUSDT', 'WINUSDT', 'WLDUSDT',
             'WNXMUSDT', 'WOOUSDT', 'WRXUSDT', 'WTCUSDT', 'XECUSDT', 'XEMUSDT', 'XLMUSDT', 'XMRUSDT', 'XNOUSDT',
             'XRPUSDT', 'XVGUSDT', 'XVSUSDT', 'YFIUSDT']



x = one + two + three + four + five + six + seven + eight + nine + ten + eleven + twelve + thirteenth + fourteenth + fifteenth
r = ['EPX', 'DUSK', 'SYN', 'PROS', 'FRONT', 'AUCTION', 'REI', 'NEXO', 'UNFI', 'FORTH', 'AMP', 'FIDA', 'VITE', 'MTL',
     'BLZ', 'YGG', 'TWT', 'AKRO', 'MDX', 'NMR', 'LOOM', 'JST', 'VTHO',
     'MULTI', 'AGLD', 'HIFI', 'OAX', 'GHST', 'ARDR', 'PHA', 'STMX', 'KEY', 'UFT', 'APT', 'ANKR', 'ACA', 'IOTA', 'STORJ',
     'AST', 'MAV', 'WLD', 'EDU', 'QUICK', 'STRAX', 'TRB', 'WAXP', 'SLP', 'LPT', 'PNT', 'GALA', 'BCH', 'VET', 'KMD']

#i = "WANUSDT"
#data_token = last_data(i, "1m", "1440")
# d = []
# for i in x:
#     try:
#         data_token = last_data(i, "1m", "600")
#         x = list(map(lambda x: round(x[0] / x[1] * 100 - 100, 2), zip(data_token.high_price, data_token.low_price)))
#         print(f"{i} ----- {round(sum(x)/len(x), 2)}")
#         d.append([i, round(sum(x)/len(x), 2)])
#     except:
#         pass
# print(d)
s = [['1INCHUSDT', 0.25], ['AAVEUSDT', 0.15], ['ACAUSDT', 0.17], ['ACHUSDT', 0.09], ['ACMUSDT', 0.02], ['ADAUSDT', 0.11], ['ADXUSDT', 0.02], ['AERGOUSDT', 0.08], ['AGIXUSDT', 0.18], ['AGLDUSDT', 0.07], ['AKROUSDT', 0.06], ['ALCXUSDT', 0.07], ['ALGOUSDT', 0.17], ['ALICEUSDT', 0.07], ['ALPACAUSDT', 0.15], ['ALPHAUSDT', 0.08], ['ALPINEUSDT', 0.04], ['AMBUSDT', 0.12], ['AMPUSDT', 0.05], ['ANKRUSDT', 0.07], ['ANTUSDT', 0.04], ['APEUSDT', 0.18], ['API3USDT', 0.15], ['APTUSDT', 0.12], ['ARBUSDT', 0.14], ['ARDRUSDT', 0.03], ['ARKMUSDT', 0.11], ['ARPAUSDT', 0.07], ['ARUSDT', 0.15], ['ASRUSDT', 0.02], ['ASTRUSDT', 0.07], ['ASTUSDT', 0.05], ['ATAUSDT', 0.04], ['ATMUSDT', 0.02], ['ATOMUSDT', 0.16], ['AUCTIONUSDT', 0.07], ['AUDIOUSDT', 0.06], ['AVAUSDT', 0.07], ['AVAXUSDT', 0.14], ['AXSUSDT', 0.17], ['BADGERUSDT', 0.12], ['BAKEUSDT', 0.37], ['BALUSDT', 0.14], ['BANDUSDT', 0.12], ['BARUSDT', 0.02], ['BATUSDT', 0.06], ['BCHUSDT', 0.05], ['BELUSDT', 0.07], ['BETAUSDT', 0.06], ['BICOUSDT', 0.09], ['BIFIUSDT', 0.03], ['BLZUSDT', 0.21], ['BNTUSDT', 0.05], ['BNXUSDT', 0.08], ['BONDUSDT', 0.13], ['BSWUSDT', 0.25], ['BTSUSDT', 0.03], ['YGGUSDT', 0.1], ['ZECUSDT', 0.05], ['ZENUSDT', 0.06], ['ZILUSDT', 0.08], ['ZRXUSDT', 0.09], ['BURGERUSDT', 0.41], ['BUSDUSDT', 0.01], ['C98USDT', 0.08], ['CAKEUSDT', 0.51], ['CELOUSDT', 0.08], ['CELRUSDT', 0.15], ['CFXUSDT', 0.13], ['CHESSUSDT', 0.12], ['CHRUSDT', 0.06], ['CHZUSDT', 0.12], ['CITYUSDT', 0.02], ['CKBUSDT', 0.09], ['CLVUSDT', 0.07], ['COMBOUSDT', 0.07], ['COMPUSDT', 0.12], ['COSUSDT', 0.05], ['COTIUSDT', 0.1], ['CRVUSDT', 0.12], ['CTKUSDT', 0.06], ['CTSIUSDT', 0.21], ['CTXCUSDT', 0.06], ['CVCUSDT', 0.03], ['CVPUSDT', 0.05], ['CVXUSDT', 0.06], ['CYBERUSDT', 0.21], ['DARUSDT', 0.12], ['DASHUSDT', 0.07], ['DATAUSDT', 0.04], ['DCRUSDT', 0.05], ['DEGOUSDT', 0.13], ['DENTUSDT', 0.05], ['DEXEUSDT', 0.04], ['DFUSDT', 0.03], ['DGBUSDT', 0.04], ['DIAUSDT', 0.03], ['DOCKUSDT', 0.02], ['DODOUSDT', 0.27], ['DOGEUSDT', 0.08], ['DOTUSDT', 0.11], ['DREPUSDT', 0.04], ['DUSKUSDT', 0.14], ['DYDXUSDT', 0.12], ['EDUUSDT', 0.12], ['EGLDUSDT', 0.79], ['ELFUSDT', 0.01], ['ENJUSDT', 0.11], ['ENSUSDT', 0.08], ['EPXUSDT', 0.05], ['ERNUSDT', 0.26], ['ETCUSDT', 0.08], ['EURUSDT', 0.01], ['FARMUSDT', 0.02], ['FDUSDUSDT', 0.01], ['FETUSDT', 0.14], ['FIDAUSDT', 0.1], ['FILUSDT', 0.11], ['FIOUSDT', 0.03], ['FIROUSDT', 0.06], ['FISUSDT', 0.05], ['FLMUSDT', 0.13], ['FLOKIUSDT', 0.14], ['FLOWUSDT', 0.23], ['FLUXUSDT', 0.07], ['FORTHUSDT', 0.13], ['FORUSDT', 0.03], ['FRONTUSDT', 0.13], ['FTMUSDT', 0.19], ['FUNUSDT', 0.03], ['FXSUSDT', 0.08], ['GALAUSDT', 0.16], ['GALUSDT', 0.18], ['GASUSDT', 0.5], ['GBPUSDT', 0.01], ['GHSTUSDT', 0.02], ['GLMRUSDT', 0.09], ['GLMUSDT', 0.02], ['GMTUSDT', 0.11], ['GMXUSDT', 0.06], ['GNOUSDT', 0.02], ['GNSUSDT', 0.06], ['GRTUSDT', 0.29], ['GTCUSDT', 0.09], ['HARDUSDT', 0.04], ['HBARUSDT', 0.13], ['HFTUSDT', 0.12], ['HIFIUSDT', 0.07], ['HIGHUSDT', 0.1], ['HIVEUSDT', 0.03], ['HOOKUSDT', 0.14], ['HOTUSDT', 0.05], ['ICPUSDT', 0.14], ['ICXUSDT', 0.06], ['IDEXUSDT', 0.09], ['IDUSDT', 0.11], ['ILVUSDT', 0.33], ['IMXUSDT', 0.56], ['INJUSDT', 0.18], ['IOSTUSDT', 0.05], ['IOTAUSDT', 0.09], ['IOTXUSDT', 0.17], ['IRISUSDT', 0.04], ['JASMYUSDT', 0.1], ['JOEUSDT', 0.09], ['JSTUSDT', 0.09], ['JUVUSDT', 0.02], ['KAVAUSDT', 0.15], ['KDAUSDT', 0.09], ['KEYUSDT', 0.06], ['KLAYUSDT', 0.05], ['KMDUSDT', 0.05], ['KNCUSDT', 0.1], ['KP3RUSDT', 0.07], ['KSMUSDT', 0.12], ['LAZIOUSDT', 0.06], ['LDOUSDT', 0.11], ['LEVERUSDT', 0.06], ['LINAUSDT', 0.09], ['LINKUSDT', 0.23], ['LITUSDT', 0.05], ['LOKAUSDT', 0.1], ['LOOMUSDT', 0.1], ['LPTUSDT', 0.05], ['LQTYUSDT', 0.12], ['LRCUSDT', 0.1], ['LSKUSDT', 0.16], ['LTCUSDT', 0.09], ['LTOUSDT', 0.03], ['LUNAUSDT', 0.11], ['LUNCUSDT', 0.08], ['MAGICUSDT', 0.16], ['MANAUSDT', 0.12], ['MASKUSDT', 0.12], ['MATICUSDT', 0.09], ['MAVUSDT', 0.13], ['MBLUSDT', 0.27], ['MBOXUSDT', 0.15], ['MCUSDT', 0.08], ['MDTUSDT', 0.12], ['MDXUSDT', 0.17], ['MINAUSDT', 0.12], ['MKRUSDT', 0.06], ['MLNUSDT', 0.04], ['MOBUSDT', 0.08], ['MOVRUSDT', 0.09], ['MTLUSDT', 0.49], ['MULTIUSDT', 0.04], ['NEARUSDT', 0.23], ['NEOUSDT', 0.28], ['NEXOUSDT', 0.07], ['NKNUSDT', 0.06], ['NMRUSDT', 0.07], ['NULSUSDT', 0.03], ['OAXUSDT', 0.05], ['OCEANUSDT', 0.1], ['OGNUSDT', 0.06], ['OGUSDT', 0.05], ['OMGUSDT', 0.07], ['OMUSDT', 0.05], ['ONEUSDT', 0.14], ['ONGUSDT', 0.24], ['ONTUSDT', 0.1], ['OOKIUSDT', 0.09], ['OPUSDT', 0.16], ['ORNUSDT', 0.38], ['OSMOUSDT', 0.21], ['OXTUSDT', 0.05], ['PAXGUSDT', 0.04], ['PENDLEUSDT', 0.06], ['PEOPLEUSDT', 0.28], ['PERLUSDT', 0.06], ['PERPUSDT', 0.12], ['PHAUSDT', 0.04], ['PHBUSDT', 0.05], ['PLAUSDT', 0.05], ['PNTUSDT', 0.06], ['POLSUSDT', 0.03], ['POLYXUSDT', 0.14], ['PONDUSDT', 0.07], ['PORTOUSDT', 0.03], ['POWRUSDT', 0.06], ['PROMUSDT', 0.03], ['PROSUSDT', 0.06], ['PSGUSDT', 0.03], ['PUNDIXUSDT', 0.08], ['PYRUSDT', 0.27], ['QIUSDT', 0.06], ['QKCUSDT', 0.07], ['QNTUSDT', 0.05], ['QTUMUSDT', 0.13], ['QUICKUSDT', 0.07], ['RADUSDT', 0.07], ['RAREUSDT', 0.05], ['RAYUSDT', 0.21], ['RDNTUSDT', 0.11], ['REEFUSDT', 0.09], ['REIUSDT', 0.05], ['RENUSDT', 0.21], ['REQUSDT', 0.04], ['RIFUSDT', 0.13], ['RLCUSDT', 0.05], ['RNDRUSDT', 0.15], ['ROSEUSDT', 0.17], ['RPLUSDT', 0.04], ['RSRUSDT', 0.12], ['RUNEUSDT', 0.18], ['RVNUSDT', 0.07], ['SANDUSDT', 0.1], ['SANTOSUSDT', 0.04], ['SCRTUSDT', 0.04], ['SCUSDT', 0.04], ['SEIUSDT', 0.18], ['SFPUSDT', 0.06], ['SHIBUSDT', 0.19], ['SKLUSDT', 0.07], ['SLPUSDT', 0.12], ['SNTUSDT', 0.23], ['SNXUSDT', 0.09], ['SOLUSDT', 0.15], ['SPELLUSDT', 0.05], ['SSVUSDT', 0.08], ['STEEMUSDT', 0.08], ['STGUSDT', 0.13], ['STMXUSDT', 0.08], ['STORJUSDT', 0.08], ['STPTUSDT', 0.06], ['STRAXUSDT', 0.09], ['STXUSDT', 0.11], ['SUIUSDT', 0.22], ['SUNUSDT', 0.01], ['SUPERUSDT', 0.07], ['SUSHIUSDT', 0.2], ['SXPUSDT', 0.08], ['SYNUSDT', 0.08], ['SYSUSDT', 0.08], ['TFUELUSDT', 0.04], ['THETAUSDT', 0.1], ['TKOUSDT', 0.16], ['TLMUSDT', 0.09], ['TOMOUSDT', 0.13], ['TRBUSDT', 0.21], ['TROYUSDT', 0.03], ['TRUUSDT', 0.13], ['TRXUSDT', 0.03], ['TUSDT', 0.07], ['TUSDUSDT', 0.01], ['TVKUSDT', 0.07], ['TWTUSDT', 0.23], ['UFTUSDT', 0.05], ['UMAUSDT', 0.04], ['UNFIUSDT', 0.32], ['UNIUSDT', 0.14], ['USDCUSDT', 0.01], ['USDPUSDT', 0.0], ['USTCUSDT', 0.08], ['UTKUSDT', 0.24], ['VETUSDT', 0.08], ['VGXUSDT', 0.09], ['VIBUSDT', 0.18], ['VIDTUSDT', 0.07], ['VITEUSDT', 0.04], ['VOXELUSDT', 0.08], ['VTHOUSDT', 0.05], ['WANUSDT', 0.23], ['WAVESUSDT', 0.28], ['WAXPUSDT', 0.06], ['WBETHUSDT', 0.01], ['WBTCUSDT', 0.01], ['WINGUSDT', 0.08], ['WINUSDT', 0.05], ['WLDUSDT', 0.1], ['WNXMUSDT', 0.03], ['WOOUSDT', 0.08], ['WRXUSDT', 0.04], ['WTCUSDT', 0.04], ['XECUSDT', 0.06], ['XEMUSDT', 0.05], ['XLMUSDT', 0.11], ['XMRUSDT', 0.08], ['XNOUSDT', 0.03], ['XRPUSDT', 0.11], ['XVGUSDT', 0.15], ['XVSUSDT', 0.54], ['YFIUSDT', 0.06]]
print(sorted(s, key=lambda x: -x[1]))

start = time.time()


while time.localtime(start).tm_min % 15 != 14 or time.localtime(start).tm_sec < 55:
    start = time.time()
    print(time.localtime(start).tm_min, time.localtime(start).tm_sec)
    print(time.localtime(start).tm_min % 15)
    time.sleep(1)


data_token = last_data("CTSIUSDT", "15m", "1440")
print(round(data_token.close_price[-1] / data_token.open_price[-1] * 100 - 100, 2))