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

two = ['DASHUSDT', 'THETAUSDT', 'ENJUSDT', 'MATICUSDT', 'ATOMUSDT', 'TFUELUSDT', 'ONEUSDT', 'FTMUSDT', 'ALGOUSDT', 'DOGEUSDT', 'DUSKUSDT', 'ANKRUSDT']

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

ninedop = ['VIDTUSDT', 'GALAUSDT', 'ILVUSDT', 'YGGUSDT', 'SYSUSDT', 'DFUSDT', 'FIDAUSDT', 'FRONTUSDT', 'AGLDUSDT', 'RADUSDT', 'BETAUSDT']

ten = ['RAREUSDT', 'LAZIOUSDT', 'CHESSUSDT', 'ADXUSDT', 'AUCTIONUSDT', 'DARUSDT', 'BNXUSDT', 'MOVRUSDT', 'CITYUSDT', 'ENSUSDT', 'KP3RUSDT', 'QIUSDT']

tendop = ['PORTOUSDT', 'POWRUSDT', 'VGXUSDT', 'JASMYUSDT', 'AMPUSDT', 'PYRUSDT', 'ALCXUSDT', 'SANTOSUSDT', 'BICOUSDT', 'FLUXUSDT', 'FXSUSDT', 'VOXELUSDT']

eleven = ['HIGHUSDT', 'CVXUSDT', 'PEOPLEUSDT', 'OOKIUSDT', 'SPELLUSDT', 'JOEUSDT', "DOGSUSDT", 'ACHUSDT', 'IMXUSDT', 'GLMRUSDT', 'LOKAUSDT', 'SCRTUSDT', 'API3USDT']

elevendop = ['BTTCUSDT', 'ACAUSDT', 'XNOUSDT', 'WOOUSDT', 'ALPINEUSDT', 'TUSDT', 'ASTRUSDT', 'GMTUSDT', 'KDAUSDT', 'APEUSDT', 'BSWUSDT', 'BIFIUSDT', 'TONUSDT']

twelve = ['STEEMUSDT', 'NEXOUSDT', 'REIUSDT', 'LDOUSDT', 'EPXUSDT', 'OPUSDT', 'RENDERUSDT', 'LEVERUSDT', 'STGUSDT', 'LUNCUSDT', 'GMXUSDT', 'POLYXUSDT', 'APTUSDT', 'BANANAUSDT']

twelvedop = ['OSMOUSDT', 'HFTUSDT', 'PHBUSDT', 'HOOKUSDT', 'MAGICUSDT', 'HIFIUSDT', 'GUSDT', 'RPLUSDT', 'PROSUSDT', 'GNSUSDT', 'SYNUSDT', 'VIBUSDT', 'SSVUSDT', 'ZROUSDT']

thirteenth = ['LQTYUSDT', 'AMBUSDT', 'USTCUSDT', 'GASUSDT', 'GLMUSDT', 'PROMUSDT', 'LISTAUSDT', 'QKCUSDT', 'UFTUSDT', 'IDUSDT', 'ARBUSDT', 'LOOMUSDT', 'OAXUSDT', 'ZKUSDT']

thirteenthdop = ['RDNTUSDT', 'WBTCUSDT', 'EDUUSDT', 'SUIUSDT', 'AERGOUSDT', 'PEPEUSDT', 'IOUSDT', 'FLOKIUSDT', 'ASTUSDT', 'SNTUSDT', 'COMBOUSDT', 'MAVUSDT', 'PENDLEUSDT', 'NOTUSDT']

fourteenth = ['ARKMUSDT', 'WBETHUSDT', 'WLDUSDT', 'SEIUSDT', 'CYBERUSDT', 'ARKUSDT', 'BBUSDT', 'CREAMUSDT', 'GFTUSDT', 'IQUSDT', 'NTRNUSDT', 'TIAUSDT', 'MEMEUSDT', 'REZUSDT']

fourteenthdop = ['ORDIUSDT', 'BEAMXUSDT', 'PIVXUSDT', 'VICUSDT', 'BLURUSDT', 'VANRYUSDT', 'OMNIUSDT', 'JTOUSDT', '1000SATSUSDT', 'BONKUSDT', 'ACEUSDT', 'NFPUSDT', 'AIUSDT', 'TAOUSDT']

fifteenth = ['XAIUSDT', 'MANTAUSDT', 'ALTUSDT', 'JUPUSDT', 'PYTHUSDT', 'RONINUSDT', 'SAGAUSDT', 'DYMUSDT', 'PIXELUSDT', 'STRKUSDT', 'PORTALUSDT', 'PDAUSDT', 'AXLUSDT', 'TNSRUSDT']

fifteenthdop = ['WIFUSDT', 'METISUSDT', 'AEVOUSDT', 'BOMEUSDT', 'ETHFIUSDT', 'ENAUSDT', 'WUSDT']

izg = []

all_cripts_workss = one + two + three + four + five + six + seven + eight + nine + ten + eleven + twelve + thirteenth + fourteenth + fifteenth + izg + \
    onedop + twodop + threedop + fourdop + fivedop + sixdop + sevendop + eightdop + ninedop + tendop + elevendop + twelvedop + \
    thirteenthdop + fourteenthdop + fifteenthdop

very_good_cript_1hour = [['MEMEUSDT', 28, 1, 28.0], ['SEIUSDT', 20, 2, 10.0], ['BEAMXUSDT', 8, 1, 8.0], ['ORDIUSDT', 15, 2, 7.5], ['TIAUSDT', 14, 2, 7.0], ['CREAMUSDT', 18, 3, 6.0], ['DOGEUSDT', 259, 50, 5.18], ['RDNTUSDT', 15, 3, 5.0], ['NTRNUSDT', 19, 4, 4.75], ['ADAUSDT', 164, 35, 4.69], ['XRPUSDT', 183, 40, 4.58], ['SHIBUSDT', 172, 39, 4.41], ['SLPUSDT', 273, 62, 4.4], ['HFTUSDT', 70, 16, 4.38], ['CYBERUSDT', 30, 7, 4.29], ['OAXUSDT', 60, 14, 4.29], ['YFIUSDT', 226, 54, 4.19]]
very_good_cript_1hour_lst = [i[0] for i in very_good_cript_1hour]
good_cript_1hour = [['WBETHUSDT', 1, 0, 1], ['HOTUSDT', 263, 63, 4.17], ['VETUSDT', 235, 57, 4.12], ['MATICUSDT', 306, 76, 4.03], ['ARBUSDT', 16, 4, 4.0], ['ARKMUSDT', 16, 4, 4.0], ['DOTUSDT', 156, 39, 4.0], ['MINAUSDT', 132, 34, 3.88], ['COTIUSDT', 390, 102, 3.82], ['ETCUSDT', 195, 52, 3.75], ['TWTUSDT', 220, 59, 3.73], ['FLOKIUSDT', 18, 5, 3.6], ['LTCUSDT', 115, 32, 3.59], ['TLMUSDT', 307, 86, 3.57], ['DENTUSDT', 349, 98, 3.56], ['REEFUSDT', 256, 72, 3.56], ['PYRUSDT', 176, 50, 3.52], ['ROSEUSDT', 309, 88, 3.51], ['SUIUSDT', 14, 4, 3.5], ['KSMUSDT', 216, 62, 3.48], ['MANAUSDT', 264, 77, 3.43], ['CRVUSDT', 363, 106, 3.42], ['AVAXUSDT', 231, 68, 3.4], ['BURGERUSDT', 275, 81, 3.4], ['XMRUSDT', 105, 31, 3.39], ['FTTUSDT', 128, 38, 3.37], ['THETAUSDT', 241, 72, 3.35], ['WRXUSDT', 335, 100, 3.35], ['GRTUSDT', 243, 73, 3.33], ['IDUSDT', 30, 9, 3.33], ['TKOUSDT', 190, 57, 3.33], ['CELRUSDT', 385, 117, 3.29], ['XEMUSDT', 164, 50, 3.28], ['ALPINEUSDT', 131, 40, 3.27], ['FILUSDT', 143, 44, 3.25], ['LUNCUSDT', 55, 17, 3.24], ['SXPUSDT', 281, 87, 3.23], ['VGXUSDT', 257, 80, 3.21], ['SUPERUSDT', 277, 87, 3.18], ['GFTUSDT', 19, 6, 3.17], ['HBARUSDT', 244, 77, 3.17], ['LINKUSDT', 180, 57, 3.16], ['LUNAUSDT', 297, 94, 3.16], ['RUNEUSDT', 284, 90, 3.16], ['LITUSDT', 279, 89, 3.13], ['BANDUSDT', 374, 120, 3.12], ['FLUXUSDT', 118, 38, 3.11], ['XLMUSDT', 137, 44, 3.11], ['PORTOUSDT', 124, 40, 3.1], ['ACMUSDT', 201, 65, 3.09], ['ENJUSDT', 281, 91, 3.09], ['SCUSDT', 235, 76, 3.09], ['SOLUSDT', 237, 77, 3.08], ['FTMUSDT', 452, 147, 3.07], ['IDEXUSDT', 172, 56, 3.07], ['ZECUSDT', 169, 55, 3.07], ['CTSIUSDT', 370, 121, 3.06], ['CHRUSDT', 359, 118, 3.04], ['RENUSDT', 337, 111, 3.04], ['TVKUSDT', 146, 48, 3.04], ['PSGUSDT', 239, 79, 3.03], ['SUSHIUSDT', 314, 104, 3.02], ['ANKRUSDT', 318, 106, 3.0], ['DIAUSDT', 291, 97, 3.0], ['ALGOUSDT', 212, 71, 2.99], ['BARUSDT', 131, 44, 2.98], ['NEOUSDT', 173, 58, 2.98], ['ALPHAUSDT', 342, 115, 2.97], ['DEGOUSDT', 267, 90, 2.97], ['IOTAUSDT', 196, 66, 2.97], ['MAGICUSDT', 59, 20, 2.95], ['TFUELUSDT', 330, 112, 2.95], ['MULTIUSDT', 94, 32, 2.94], ['EGLDUSDT', 170, 58, 2.93], ['FETUSDT', 399, 136, 2.93], ['ONEUSDT', 349, 119, 2.93], ['OGUSDT', 364, 125, 2.91], ['PNTUSDT', 330, 114, 2.89], ['PROSUSDT', 26, 9, 2.89], ['REQUSDT', 121, 42, 2.88], ['1INCHUSDT', 201, 70, 2.87], ['RSRUSDT', 306, 107, 2.86], ['RVNUSDT', 232, 81, 2.86], ['ATOMUSDT', 193, 68, 2.84], ['CHZUSDT', 287, 101, 2.84], ['LSKUSDT', 261, 92, 2.84], ['SNTUSDT', 17, 6, 2.83], ['XVGUSDT', 133, 47, 2.83], ['KAVAUSDT', 279, 99, 2.82], ['OGNUSDT', 432, 153, 2.82], ['ATMUSDT', 233, 83, 2.81], ['LAZIOUSDT', 152, 54, 2.81], ['ONTUSDT', 179, 64, 2.8], ['ICPUSDT', 159, 57, 2.79], ['OXTUSDT', 215, 77, 2.79], ['FORTHUSDT', 203, 73, 2.78], ['BONDUSDT', 144, 52, 2.77], ['ALICEUSDT', 251, 91, 2.76], ['DODOUSDT', 221, 80, 2.76], ['SYSUSDT', 124, 45, 2.76], ['WTCUSDT', 298, 108, 2.76], ['AGIXUSDT', 22, 8, 2.75], ['TRBUSDT', 385, 140, 2.75], ['BATUSDT', 167, 61, 2.74], ['VIDTUSDT', 178, 65, 2.74], ['TOMOUSDT', 289, 106, 2.73], ['AAVEUSDT', 179, 66, 2.71], ['BAKEUSDT', 187, 69, 2.71], ['BELUSDT', 317, 117, 2.71], ['REIUSDT', 122, 45, 2.71], ['DATAUSDT', 299, 111, 2.69], ['BCHUSDT', 118, 44, 2.68], ['CAKEUSDT', 134, 50, 2.68], ['GLMRUSDT', 99, 37, 2.68], ['JASMYUSDT', 131, 49, 2.67], ['VITEUSDT', 371, 139, 2.67], ['ASRUSDT', 237, 89, 2.66], ['SANDUSDT', 339, 129, 2.63], ['CTXCUSDT', 356, 137, 2.6], ['LRCUSDT', 285, 110, 2.59], ['OMGUSDT', 227, 88, 2.58], ['VIBUSDT', 31, 12, 2.58], ['DREPUSDT', 394, 154, 2.56], ['OPUSDT', 92, 36, 2.56], ['ENSUSDT', 125, 49, 2.55], ['CFXUSDT', 208, 82, 2.54], ['INJUSDT', 277, 109, 2.54], ['KEYUSDT', 435, 172, 2.53], ['MDTUSDT', 349, 138, 2.53], ['OCEANUSDT', 253, 100, 2.53], ['COMPUSDT', 179, 71, 2.52], ['TRXUSDT', 106, 42, 2.52], ['FARMUSDT', 113, 45, 2.51], ['ARKUSDT', 20, 8, 2.5], ['GMXUSDT', 25, 10, 2.5], ['HOOKUSDT', 55, 22, 2.5], ['RLCUSDT', 318, 127, 2.5], ['ZILUSDT', 240, 96, 2.5], ['AXSUSDT', 306, 123, 2.49], ['ICXUSDT', 250, 101, 2.48], ['PERLUSDT', 427, 172, 2.48], ['SANTOSUSDT', 158, 64, 2.47], ['SNXUSDT', 237, 96, 2.47], ['DUSKUSDT', 317, 129, 2.46], ['STORJUSDT', 262, 107, 2.45], ['FUNUSDT', 205, 84, 2.44], ['IRISUSDT', 329, 135, 2.44], ['TRUUSDT', 253, 104, 2.43], ['APEUSDT', 87, 36, 2.42], ['DEXEUSDT', 138, 57, 2.42], ['WANUSDT', 241, 100, 2.41], ['GLMUSDT', 12, 5, 2.4], ['LOKAUSDT', 173, 72, 2.4], ['NMRUSDT', 214, 89, 2.4], ['UNFIUSDT', 369, 154, 2.4], ['WAVESUSDT', 230, 96, 2.4], ['EPXUSDT', 91, 38, 2.39], ['ORNUSDT', 210, 88, 2.39], ['WOOUSDT', 79, 33, 2.39], ['CKBUSDT', 194, 82, 2.37], ['OOKIUSDT', 140, 59, 2.37], ['UNIUSDT', 161, 68, 2.37], ['FIROUSDT', 183, 78, 2.35], ['ARUSDT', 200, 86, 2.33], ['POLYXUSDT', 63, 27, 2.33], ['NKNUSDT', 351, 151, 2.32], ['STXUSDT', 292, 126, 2.32], ['TROYUSDT', 387, 167, 2.32], ['PEOPLEUSDT', 166, 72, 2.31], ['RIFUSDT', 187, 81, 2.31], ['SPELLUSDT', 110, 48, 2.29], ['ALPACAUSDT', 89, 39, 2.28], ['AUDIOUSDT', 290, 128, 2.27], ['NEARUSDT', 193, 85, 2.27], ['SKLUSDT', 266, 117, 2.27], ['STRAXUSDT', 259, 114, 2.27], ['BETAUSDT', 154, 68, 2.26], ['CLVUSDT', 113, 50, 2.26], ['GALAUSDT', 156, 69, 2.26], ['HARDUSDT', 253, 112, 2.26], ['LINAUSDT', 215, 95, 2.26], ['MKRUSDT', 115, 51, 2.25], ['RAYUSDT', 108, 48, 2.25], ['ARPAUSDT', 323, 144, 2.24], ['DARUSDT', 152, 68, 2.24], ['KP3RUSDT', 118, 53, 2.23], ['RNDRUSDT', 185, 83, 2.23], ['BIFIUSDT', 73, 33, 2.21], ['ILVUSDT', 53, 24, 2.21], ['MASKUSDT', 212, 96, 2.21], ['OMUSDT', 192, 87, 2.21], ['BLZUSDT', 310, 141, 2.2], ['GASUSDT', 33, 15, 2.2], ['MAVUSDT', 22, 10, 2.2], ['QTUMUSDT', 191, 87, 2.2], ['ZRXUSDT', 227, 103, 2.2], ['MBLUSDT', 344, 157, 2.19], ['CVCUSDT', 261, 120, 2.17], ['ANTUSDT', 229, 106, 2.16], ['DASHUSDT', 125, 58, 2.16], ['SFPUSDT', 207, 96, 2.16], ['DFUSDT', 99, 46, 2.15], ['AMPUSDT', 60, 28, 2.14], ['MBOXUSDT', 120, 56, 2.14], ['OSMOUSDT', 15, 7, 2.14], ['SSVUSDT', 15, 7, 2.14], ['IMXUSDT', 96, 45, 2.13], ['STMXUSDT', 279, 131, 2.13], ['C98USDT', 121, 57, 2.12], ['JUVUSDT', 242, 114, 2.12], ['MTLUSDT', 289, 136, 2.12], ['TUSDT', 70, 33, 2.12], ['LEVERUSDT', 99, 47, 2.11], ['PHAUSDT', 116, 55, 2.11], ['FIOUSDT', 215, 104, 2.07], ['JSTUSDT', 151, 73, 2.07], ['FISUSDT', 235, 114, 2.06], ['XECUSDT', 78, 38, 2.05], ['UMAUSDT', 198, 97, 2.04], ['ZENUSDT', 206, 101, 2.04], ['CHESSUSDT', 121, 60, 2.02], ['CVPUSDT', 99, 49, 2.02], ['LQTYUSDT', 44, 22, 2.0], ['PROMUSDT', 10, 5, 2.0], ['WLDUSDT', 20, 10, 2.0], ['BICOUSDT', 93, 47, 1.98], ['PUNDIXUSDT', 160, 81, 1.98], ['QIUSDT', 129, 65, 1.98], ['GALUSDT', 106, 54, 1.96], ['BNXUSDT', 93, 48, 1.94], ['WNXMUSDT', 203, 105, 1.93], ['ACHUSDT', 117, 61, 1.92], ['MOVRUSDT', 69, 36, 1.92], ['NULSUSDT', 257, 134, 1.92], ['KMDUSDT', 241, 126, 1.91], ['ONGUSDT', 292, 154, 1.9], ['BALUSDT', 130, 69, 1.88], ['HIVEUSDT', 277, 147, 1.88], ['PHBUSDT', 58, 31, 1.87], ['STEEMUSDT', 65, 35, 1.86], ['RADUSDT', 126, 68, 1.85], ['API3USDT', 105, 57, 1.84], ['DCRUSDT', 105, 57, 1.84], ['AGLDUSDT', 139, 76, 1.83], ['APTUSDT', 44, 24, 1.83], ['STPTUSDT', 282, 156, 1.81], ['DYDXUSDT', 137, 76, 1.8], ['LOOMUSDT', 45, 25, 1.8], ['HIFIUSDT', 53, 30, 1.77], ['JOEUSDT', 99, 56, 1.77], ['PERPUSDT', 177, 100, 1.77], ['FIDAUSDT', 104, 59, 1.76], ['GMTUSDT', 127, 72, 1.76]]
good_cript_1hour_lst = [i[0] for i in good_cript_1hour]
bad_cript_1hour = [['CVXUSDT', 76, 33, 2.3], ['YGGUSDT', 145, 63, 2.3], ['MOBUSDT', 73, 32, 2.28], ['FRONTUSDT', 112, 50, 2.24], ['IOTXUSDT', 282, 126, 2.24], ['AMBUSDT', 33, 15, 2.2], ['UFTUSDT', 16, 8, 2.0], ['RPLUSDT', 21, 9, 2.33], ['ALCXUSDT', 86, 29, 2.97], ['LDOUSDT', 139, 47, 2.96], ['PERPUSDT', 207, 70, 2.96], ['WNXMUSDT', 230, 78, 2.95], ['FIDAUSDT', 121, 42, 2.88], ['JOEUSDT', 115, 40, 2.88], ['RADUSDT', 144, 50, 2.88], ['QUICKUSDT', 104, 37, 2.81], ['CITYUSDT', 78, 28, 2.79], ['ELFUSDT', 94, 34, 2.76], ['WAXPUSDT', 109, 40, 2.73], ['ACHUSDT', 130, 48, 2.71], ['POWRUSDT', 111, 41, 2.71], ['LOOMUSDT', 51, 19, 2.68], ['FORUSDT', 117, 45, 2.6], ['MLNUSDT', 93, 36, 2.58], ['POLSUSDT', 111, 43, 2.58], ['ARDRUSDT', 259, 103, 2.51], ['BADGERUSDT', 133, 53, 2.51], ['AGLDUSDT', 153, 62, 2.47]]
bad_cript_1hour_lst = [i[0] for i in bad_cript_1hour]
very_bad_cript_1hour = [['FXSUSDT', 51, 26, 1.96], ['AUCTIONUSDT', 131, 71, 1.85], ['SCRTUSDT', 48, 28, 1.71], ['QKCUSDT', 15, 10, 1.5]]

all_cript = [['MEMEUSDT', 28, 1, 28.0], ['SEIUSDT', 20, 2, 10.0], ['BEAMXUSDT', 8, 1, 8.0], ['ORDIUSDT', 15, 2, 7.5], ['TIAUSDT', 14, 2, 7.0], ['CREAMUSDT', 18, 3, 6.0], ['DOGEUSDT', 259, 50, 5.18], ['RDNTUSDT', 15, 3, 5.0], ['NTRNUSDT', 19, 4, 4.75], ['ADAUSDT', 164, 35, 4.69], ['XRPUSDT', 183, 40, 4.58], ['SHIBUSDT', 172, 39, 4.41], ['SLPUSDT', 273, 62, 4.4], ['HFTUSDT', 70, 16, 4.38], ['CYBERUSDT', 30, 7, 4.29], ['OAXUSDT', 60, 14, 4.29], ['YFIUSDT', 226, 54, 4.19], ['HOTUSDT', 263, 63, 4.17], ['VETUSDT', 235, 57, 4.12], ['MATICUSDT', 306, 76, 4.03], ['ARBUSDT', 16, 4, 4.0], ['ARKMUSDT', 16, 4, 4.0], ['DOTUSDT', 156, 39, 4.0], ['MINAUSDT', 132, 34, 3.88], ['COTIUSDT', 390, 102, 3.82], ['ETCUSDT', 195, 52, 3.75], ['TWTUSDT', 220, 59, 3.73], ['FLOKIUSDT', 18, 5, 3.6], ['LTCUSDT', 115, 32, 3.59], ['TLMUSDT', 307, 86, 3.57], ['DENTUSDT', 349, 98, 3.56], ['REEFUSDT', 256, 72, 3.56], ['PYRUSDT', 176, 50, 3.52], ['ROSEUSDT', 309, 88, 3.51], ['SUIUSDT', 14, 4, 3.5], ['KSMUSDT', 216, 62, 3.48], ['MANAUSDT', 264, 77, 3.43], ['CRVUSDT', 363, 106, 3.42], ['AVAXUSDT', 231, 68, 3.4], ['BURGERUSDT', 275, 81, 3.4], ['XMRUSDT', 105, 31, 3.39], ['FTTUSDT', 128, 38, 3.37], ['THETAUSDT', 241, 72, 3.35], ['WRXUSDT', 335, 100, 3.35], ['GRTUSDT', 243, 73, 3.33], ['IDUSDT', 30, 9, 3.33], ['TKOUSDT', 190, 57, 3.33], ['CELRUSDT', 385, 117, 3.29], ['XEMUSDT', 164, 50, 3.28], ['ALPINEUSDT', 131, 40, 3.27], ['FILUSDT', 143, 44, 3.25], ['LUNCUSDT', 55, 17, 3.24], ['SXPUSDT', 281, 87, 3.23], ['VGXUSDT', 257, 80, 3.21], ['SUPERUSDT', 277, 87, 3.18], ['GFTUSDT', 19, 6, 3.17], ['HBARUSDT', 244, 77, 3.17], ['LINKUSDT', 180, 57, 3.16], ['LUNAUSDT', 297, 94, 3.16], ['RUNEUSDT', 284, 90, 3.16], ['LITUSDT', 279, 89, 3.13], ['BANDUSDT', 374, 120, 3.12], ['FLUXUSDT', 118, 38, 3.11], ['XLMUSDT', 137, 44, 3.11], ['PORTOUSDT', 124, 40, 3.1], ['ACMUSDT', 201, 65, 3.09], ['ENJUSDT', 281, 91, 3.09], ['SCUSDT', 235, 76, 3.09], ['SOLUSDT', 237, 77, 3.08], ['FTMUSDT', 452, 147, 3.07], ['IDEXUSDT', 172, 56, 3.07], ['ZECUSDT', 169, 55, 3.07], ['CTSIUSDT', 370, 121, 3.06], ['CHRUSDT', 359, 118, 3.04], ['RENUSDT', 337, 111, 3.04], ['TVKUSDT', 146, 48, 3.04], ['PSGUSDT', 239, 79, 3.03], ['SUSHIUSDT', 314, 104, 3.02], ['ANKRUSDT', 318, 106, 3.0], ['DIAUSDT', 291, 97, 3.0], ['ALGOUSDT', 212, 71, 2.99], ['BARUSDT', 131, 44, 2.98], ['NEOUSDT', 173, 58, 2.98], ['ALPHAUSDT', 342, 115, 2.97], ['DEGOUSDT', 267, 90, 2.97], ['IOTAUSDT', 196, 66, 2.97], ['MAGICUSDT', 59, 20, 2.95], ['TFUELUSDT', 330, 112, 2.95], ['MULTIUSDT', 94, 32, 2.94], ['EGLDUSDT', 170, 58, 2.93], ['FETUSDT', 399, 136, 2.93], ['ONEUSDT', 349, 119, 2.93], ['OGUSDT', 364, 125, 2.91], ['PNTUSDT', 330, 114, 2.89], ['PROSUSDT', 26, 9, 2.89], ['REQUSDT', 121, 42, 2.88], ['1INCHUSDT', 201, 70, 2.87], ['RSRUSDT', 306, 107, 2.86], ['RVNUSDT', 232, 81, 2.86], ['ATOMUSDT', 193, 68, 2.84], ['CHZUSDT', 287, 101, 2.84], ['LSKUSDT', 261, 92, 2.84], ['SNTUSDT', 17, 6, 2.83], ['XVGUSDT', 133, 47, 2.83], ['KAVAUSDT', 279, 99, 2.82], ['OGNUSDT', 432, 153, 2.82], ['ATMUSDT', 233, 83, 2.81], ['LAZIOUSDT', 152, 54, 2.81], ['ONTUSDT', 179, 64, 2.8], ['ICPUSDT', 159, 57, 2.79], ['OXTUSDT', 215, 77, 2.79], ['FORTHUSDT', 203, 73, 2.78], ['BONDUSDT', 144, 52, 2.77], ['ALICEUSDT', 251, 91, 2.76], ['DODOUSDT', 221, 80, 2.76], ['SYSUSDT', 124, 45, 2.76], ['WTCUSDT', 298, 108, 2.76], ['AGIXUSDT', 22, 8, 2.75], ['TRBUSDT', 385, 140, 2.75], ['BATUSDT', 167, 61, 2.74], ['VIDTUSDT', 178, 65, 2.74], ['TOMOUSDT', 289, 106, 2.73], ['AAVEUSDT', 179, 66, 2.71], ['BAKEUSDT', 187, 69, 2.71], ['BELUSDT', 317, 117, 2.71], ['REIUSDT', 122, 45, 2.71], ['DATAUSDT', 299, 111, 2.69], ['BCHUSDT', 118, 44, 2.68], ['CAKEUSDT', 134, 50, 2.68], ['GLMRUSDT', 99, 37, 2.68], ['JASMYUSDT', 131, 49, 2.67], ['VITEUSDT', 371, 139, 2.67], ['ASRUSDT', 237, 89, 2.66], ['SANDUSDT', 339, 129, 2.63], ['CTXCUSDT', 356, 137, 2.6], ['LRCUSDT', 285, 110, 2.59], ['OMGUSDT', 227, 88, 2.58], ['VIBUSDT', 31, 12, 2.58], ['DREPUSDT', 394, 154, 2.56], ['OPUSDT', 92, 36, 2.56], ['ENSUSDT', 125, 49, 2.55], ['CFXUSDT', 208, 82, 2.54], ['INJUSDT', 277, 109, 2.54], ['KEYUSDT', 435, 172, 2.53], ['MDTUSDT', 349, 138, 2.53], ['OCEANUSDT', 253, 100, 2.53], ['COMPUSDT', 179, 71, 2.52], ['TRXUSDT', 106, 42, 2.52], ['FARMUSDT', 113, 45, 2.51], ['ARKUSDT', 20, 8, 2.5], ['GMXUSDT', 25, 10, 2.5], ['HOOKUSDT', 55, 22, 2.5], ['RLCUSDT', 318, 127, 2.5], ['ZILUSDT', 240, 96, 2.5], ['AXSUSDT', 306, 123, 2.49], ['ICXUSDT', 250, 101, 2.48], ['PERLUSDT', 427, 172, 2.48], ['SANTOSUSDT', 158, 64, 2.47], ['SNXUSDT', 237, 96, 2.47], ['DUSKUSDT', 317, 129, 2.46], ['STORJUSDT', 262, 107, 2.45], ['FUNUSDT', 205, 84, 2.44], ['IRISUSDT', 329, 135, 2.44], ['TRUUSDT', 253, 104, 2.43], ['APEUSDT', 87, 36, 2.42], ['DEXEUSDT', 138, 57, 2.42], ['WANUSDT', 241, 100, 2.41], ['GLMUSDT', 12, 5, 2.4], ['LOKAUSDT', 173, 72, 2.4], ['NMRUSDT', 214, 89, 2.4], ['UNFIUSDT', 369, 154, 2.4], ['WAVESUSDT', 230, 96, 2.4], ['EPXUSDT', 91, 38, 2.39], ['ORNUSDT', 210, 88, 2.39], ['WOOUSDT', 79, 33, 2.39], ['CKBUSDT', 194, 82, 2.37], ['OOKIUSDT', 140, 59, 2.37], ['UNIUSDT', 161, 68, 2.37], ['FIROUSDT', 183, 78, 2.35], ['ARUSDT', 200, 86, 2.33], ['POLYXUSDT', 63, 27, 2.33], ['NKNUSDT', 351, 151, 2.32], ['STXUSDT', 292, 126, 2.32], ['TROYUSDT', 387, 167, 2.32], ['PEOPLEUSDT', 166, 72, 2.31], ['RIFUSDT', 187, 81, 2.31], ['SPELLUSDT', 110, 48, 2.29], ['ALPACAUSDT', 89, 39, 2.28], ['AUDIOUSDT', 290, 128, 2.27], ['NEARUSDT', 193, 85, 2.27], ['SKLUSDT', 266, 117, 2.27], ['STRAXUSDT', 259, 114, 2.27], ['BETAUSDT', 154, 68, 2.26], ['CLVUSDT', 113, 50, 2.26], ['GALAUSDT', 156, 69, 2.26], ['HARDUSDT', 253, 112, 2.26], ['LINAUSDT', 215, 95, 2.26], ['MKRUSDT', 115, 51, 2.25], ['RAYUSDT', 108, 48, 2.25], ['ARPAUSDT', 323, 144, 2.24], ['DARUSDT', 152, 68, 2.24], ['KP3RUSDT', 118, 53, 2.23], ['RNDRUSDT', 185, 83, 2.23], ['BIFIUSDT', 73, 33, 2.21], ['ILVUSDT', 53, 24, 2.21], ['MASKUSDT', 212, 96, 2.21], ['OMUSDT', 192, 87, 2.21], ['BLZUSDT', 310, 141, 2.2], ['GASUSDT', 33, 15, 2.2], ['MAVUSDT', 22, 10, 2.2], ['QTUMUSDT', 191, 87, 2.2], ['ZRXUSDT', 227, 103, 2.2], ['MBLUSDT', 344, 157, 2.19], ['CVCUSDT', 261, 120, 2.17], ['ANTUSDT', 229, 106, 2.16], ['DASHUSDT', 125, 58, 2.16], ['SFPUSDT', 207, 96, 2.16], ['DFUSDT', 99, 46, 2.15], ['AMPUSDT', 60, 28, 2.14], ['MBOXUSDT', 120, 56, 2.14], ['OSMOUSDT', 15, 7, 2.14], ['SSVUSDT', 15, 7, 2.14], ['IMXUSDT', 96, 45, 2.13], ['STMXUSDT', 279, 131, 2.13], ['C98USDT', 121, 57, 2.12], ['JUVUSDT', 242, 114, 2.12], ['MTLUSDT', 289, 136, 2.12], ['TUSDT', 70, 33, 2.12], ['LEVERUSDT', 99, 47, 2.11], ['PHAUSDT', 116, 55, 2.11], ['FIOUSDT', 215, 104, 2.07], ['JSTUSDT', 151, 73, 2.07], ['FISUSDT', 235, 114, 2.06], ['XECUSDT', 78, 38, 2.05], ['UMAUSDT', 198, 97, 2.04], ['ZENUSDT', 206, 101, 2.04], ['CHESSUSDT', 121, 60, 2.02], ['CVPUSDT', 99, 49, 2.02], ['LQTYUSDT', 44, 22, 2.0], ['PROMUSDT', 10, 5, 2.0], ['WLDUSDT', 20, 10, 2.0], ['BICOUSDT', 93, 47, 1.98], ['PUNDIXUSDT', 160, 81, 1.98], ['QIUSDT', 129, 65, 1.98], ['GALUSDT', 106, 54, 1.96], ['BNXUSDT', 93, 48, 1.94], ['WNXMUSDT', 203, 105, 1.93], ['ACHUSDT', 117, 61, 1.92], ['MOVRUSDT', 69, 36, 1.92], ['NULSUSDT', 257, 134, 1.92], ['KMDUSDT', 241, 126, 1.91], ['ONGUSDT', 292, 154, 1.9], ['BALUSDT', 130, 69, 1.88], ['HIVEUSDT', 277, 147, 1.88], ['PHBUSDT', 58, 31, 1.87], ['STEEMUSDT', 65, 35, 1.86], ['RADUSDT', 126, 68, 1.85], ['API3USDT', 105, 57, 1.84], ['DCRUSDT', 105, 57, 1.84], ['AGLDUSDT', 139, 76, 1.83], ['APTUSDT', 44, 24, 1.83], ['STPTUSDT', 282, 156, 1.81], ['DYDXUSDT', 137, 76, 1.8], ['LOOMUSDT', 45, 25, 1.8], ['HIFIUSDT', 53, 30, 1.77], ['JOEUSDT', 99, 56, 1.77], ['PERPUSDT', 177, 100, 1.77], ['FIDAUSDT', 104, 59, 1.76], ['GMTUSDT', 127, 72, 1.76], ['ALCXUSDT', 73, 42, 1.74], ['MLNUSDT', 82, 47, 1.74], ['VOXELUSDT', 134, 78, 1.72], ['HIGHUSDT', 118, 69, 1.71], ['WAXPUSDT', 94, 55, 1.71], ['GNSUSDT', 17, 10, 1.7], ['ARDRUSDT', 227, 135, 1.68], ['AMBUSDT', 30, 18, 1.67], ['LDOUSDT', 116, 70, 1.66], ['EDUUSDT', 18, 11, 1.64], ['YGGUSDT', 129, 79, 1.63], ['FRONTUSDT', 100, 62, 1.61], ['POLSUSDT', 95, 59, 1.61], ['KLAYUSDT', 46, 29, 1.59], ['ELFUSDT', 78, 50, 1.56], ['QUICKUSDT', 86, 55, 1.56], ['CITYUSDT', 64, 42, 1.52], ['AERGOUSDT', 9, 6, 1.5], ['USTCUSDT', 12, 8, 1.5], ['IOTXUSDT', 244, 164, 1.49], ['POWRUSDT', 90, 62, 1.45], ['MOBUSDT', 62, 43, 1.44], ['STGUSDT', 36, 25, 1.44], ['BADGERUSDT', 109, 77, 1.42], ['FORUSDT', 95, 67, 1.42], ['SYNUSDT', 21, 15, 1.4], ['AUCTIONUSDT', 116, 86, 1.35], ['FXSUSDT', 44, 33, 1.33], ['CVXUSDT', 62, 47, 1.32], ['RPLUSDT', 17, 13, 1.31], ['UFTUSDT', 13, 11, 1.18], ['WBETHUSDT', 1, 0, 1], ['SCRTUSDT', 37, 39, 0.95], ['QKCUSDT', 10, 15, 0.67]]


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
            time_frames = [0, 4, 8, 10, 12, 16, 20, 22]

            time_frames_4h = [0, 4, 8, 12, 16, 20]

            time_frames_6h = [4, 10, 16, 22]

            if time.localtime(time.time()).tm_min == 59 and time.localtime(time.time()).tm_hour in time_frames:
                data_token: Dataset = last_data(name_cript_check, "4h", "17280")
                volume_per_5h: float = sum([int(i * data_token.high_price[-1]) for i in data_token.volume[-4:]]) / len(
                    data_token.volume[-4:]) / 80
                res: float = round(data_token.close_price[-1] / data_token.open_price[-1] * 100 - 100, 2)
                res_before: float = round(data_token.close_price[-1] / data_token.low_price[-1] * 100 - 100, 2)
                price_change_percent_24h: float = round(
                    ((data_token.close_price[-1] / data_token.open_price[-6]) * 100) - 100, 2)
                price_change_percent_7d: float = round(
                    ((max(data_token.high_price) / data_token.close_price[-1]) * 100) - 100, 2)
                high_close = list(map(lambda x: round(x[0] / x[1] * 100 - 100, 2),
                                      zip(data_token.high_price[:-1], data_token.close_price[:-1])))
                high_close_change = round(sum(high_close) / len(high_close), 2)
                """Отношение свечи падения к нижнему хвосту"""
                res_k_low = round(abs(res) / res_before * 100, 2)
                '''процент падения за последние 2ч. Отрицательные значение == был рост'''
                loss_price_for_two_hours: float = round(
                    100 - data_token.close_price[-2] / max([i for i in data_token.open_price[-9:]]) * 100, 2)

                if -4.1 > res > -20:

                    ''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
                    '''''''''''''''''''''''''''''Выбор цены продажи'''''''''''''''''''''''''''''''''''''''''''''''
                    ''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

                    if -4.1 > res > -8.5:
                        sell_pr = 100.95

                    if -8.5 > res > -20:
                        sell_pr = 101.25

                    """Волатильность по фреймам"""
                    high_frames = list(map(lambda x: round(x[1] / x[0] * 100 - 100, 2),
                                           zip(data_token.open_price, data_token.high_price)))
                    awerage_high_frame = len([i for i in high_frames if i > sell_pr - 100])

                    buy_qty = round(11 / data_token.close_price[-1], 1)

                    telebot.TeleBot(telega_token).send_message(chat_id, f"ПРЕАЛГТЕСТ- {name_cript_check}\n"
                                                                        f"{time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))}\n"
                                                                        f"Рост по фреймам - {len([i for i in high_frames if i > sell_pr - 100])}\n"
                                                                        f"Объемы {int(volume_per_5h)}\n"
                                                                        f"Цена упала на {res}%\n"
                                                                        f"Свечной хвостик {res_k_low}%\n"
                                                                        f"Изменение цены за сутки {price_change_percent_24h}%\n")

                if time.localtime(time.time()).tm_hour in time_frames_4h:

                    data_token: Dataset = last_data(name_cript_check, "4h", "17280")
                    volume_per_5h: float = sum([int(i * data_token.high_price[-1]) for i in data_token.volume[-4:]]) / len(data_token.volume[-4:]) / 80
                    res: float = round(data_token.close_price[-1] / data_token.open_price[-1] * 100 - 100, 2)
                    res_before: float = round(data_token.close_price[-1] / data_token.low_price[-1] * 100 - 100, 2)
                    price_change_percent_24h: float = round(((data_token.close_price[-1] / data_token.open_price[-6]) * 100) - 100, 2)
                    price_change_percent_7d: float = round(((max(data_token.high_price) / data_token.close_price[-1]) * 100) - 100, 2)
                    high_close = list(map(lambda x: round(x[0] / x[1] * 100 - 100, 2), zip(data_token.high_price[:-1], data_token.close_price[:-1])))
                    high_close_change = round(sum(high_close) / len(high_close), 2)
                    """Отношение свечи падения к нижнему хвосту"""
                    res_k_low = round(abs(res) / res_before * 100, 2)
                    '''процент падения за последние 2ч. Отрицательные значение == был рост'''
                    loss_price_for_two_hours: float = round(100 - data_token.close_price[-2] / max([i for i in data_token.open_price[-9:]]) * 100, 2)

                    if -4.1 > res > -20:

                        ''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
                        '''''''''''''''''''''''''''''Выбор цены продажи'''''''''''''''''''''''''''''''''''''''''''''''
                        ''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

                        if -4.1 > res > -8.5:
                            sell_pr = 100.95

                        if -8.5 > res > -20:
                            sell_pr = 101.25

                        """Волатильность по фреймам"""
                        high_frames = list(map(lambda x: round(x[1] / x[0] * 100 - 100, 2),
                                               zip(data_token.open_price, data_token.high_price)))
                        awerage_high_frame = len([i for i in high_frames if i > sell_pr-100])

                        buy_qty = round(11 / data_token.close_price[-1], 1)

                        telebot.TeleBot(telega_token).send_message(chat_id, f"RABOTAEM 4 ЧАСОВИК- {name_cript_check}\n"
                                                                                f"{time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))}\n"
                                                                                f"Рост по фреймам - {len([i for i in high_frames if i > sell_pr-100])}\n"
                                                                                f"Объемы {int(volume_per_5h)}\n"
                                                                                f"Цена упала на {res}%\n"
                                                                                f"Свечной хвостик {res_k_low}%\n"
                                                                                f"Изменение цены за сутки {price_change_percent_24h}%\n")

                        """Изменяем % суточного падения, чтобы исключить выбор этой крипты для закупа"""
                        # if price_change_percent_24h < -30:
                        #     res = 0
                        #     price_change_percent_24h = 100


                        '''Если такой крипты в базе еще нет, то добавляем в базу '''
                        if name_cript_check + "_4h" not in [i['name_cript'] for i in get_crypto()] and volume_per_5h > 6500 and res_k_low > 200:
                                equal(name_cript_check + "_4h", res, res_before, price_change_percent_24h, awerage_high_frame, price_change_percent_7d, res_k_low)

                if time.localtime(time.time()).tm_hour in time_frames_6h:
                    data_token: Dataset = last_data(name_cript_check, "6h", "17280")
                    volume_per_5h: float = sum(
                        [int(i * data_token.high_price[-1]) for i in data_token.volume[-4:]]) / len(
                        data_token.volume[-4:]) / 120
                    res: float = round(data_token.close_price[-1] / data_token.open_price[-1] * 100 - 100, 2)
                    res_before: float = round(data_token.close_price[-1] / data_token.low_price[-1] * 100 - 100, 2)
                    price_change_percent_24h: float = round(
                        ((data_token.close_price[-1] / data_token.open_price[-6]) * 100) - 100, 2)
                    price_change_percent_7d: float = round(
                        ((max(data_token.high_price) / data_token.close_price[-1]) * 100) - 100, 2)
                    high_close = list(map(lambda x: round(x[0] / x[1] * 100 - 100, 2),
                                          zip(data_token.high_price[:-1], data_token.close_price[:-1])))
                    high_close_change = round(sum(high_close) / len(high_close), 2)
                    """Отношение свечи падения к нижнему хвосту"""
                    res_k_low = round(abs(res) / res_before * 100, 2)
                    '''процент падения за последние 2ч. Отрицательные значение == был рост'''
                    loss_price_for_two_hours: float = round(
                        100 - data_token.close_price[-2] / max([i for i in data_token.open_price[-9:]]) * 100, 2)

                    if -4.1 > res > -20:

                        ''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
                        '''''''''''''''''''''''''''''Выбор цены продажи'''''''''''''''''''''''''''''''''''''''''''''''
                        ''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

                        if -4.1 > res > -8.5:
                            sell_pr = 101.15

                        if -8.5 > res > -20:
                            sell_pr = 101.5

                        """Волатильность по фреймам"""
                        high_frames = list(map(lambda x: round(x[1] / x[0] * 100 - 100, 2),
                                               zip(data_token.open_price, data_token.high_price)))
                        awerage_high_frame = len([i for i in high_frames if i > sell_pr - 100])

                        buy_qty = round(11 / data_token.close_price[-1], 1)

                        telebot.TeleBot(telega_token).send_message(chat_id, f"RABOTAEM 6 ЧАСОВИК- {name_cript_check}\n"
                                                                            f"{time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))}\n"
                                                                            f"Рост по фреймам - {len([i for i in high_frames if i > sell_pr - 100])}\n"
                                                                            f"Объемы {int(volume_per_5h)}\n"
                                                                            f"Цена упала на {res}%\n"
                                                                            f"Свечной хвостик {res_k_low}%\n"
                                                                            f"Изменение цены за сутки {price_change_percent_24h}%\n")

                        """Изменяем % суточного падения, чтобы исключить выбор этой крипты для закупа"""
                        # if price_change_percent_24h < -30:
                        #     res = 0
                        #     price_change_percent_24h = 100

                        '''Если такой крипты в базе еще нет, то добавляем в базу '''
                        if name_cript_check + "_6h" not in [i['name_cript'] for i in
                                                    get_crypto()] and volume_per_5h > 6500 and res_k_low > 200:
                            equal(name_cript_check + "_6h", res, res_before, price_change_percent_24h, awerage_high_frame,
                                  price_change_percent_7d, res_k_low)


                start_time_check = time.time()
                '''Заглушка для ожидания конца таймфрейма 15 мин (58 сек не менять!)'''
                while time.localtime(start_time_check).tm_min != 59 or time.localtime(start_time_check).tm_sec < 58:
                    start_time_check = time.time()
                    time.sleep(1)

                bd_cript = get_crypto()
                '''Проверка на наилучший объект и работа с ним дальше'''
                reit_bd_cript = []

                bd_cript_6h = []
                bd_cript_4h = []

                for i in bd_cript:
                    if i['name_cript'][-3:] == "_6h":
                        bd_cript_6h.append(i)
                    if i['name_cript'][-3:] == "_4h":
                        bd_cript_4h.append(i)

                if len(bd_cript_6h) > 0 and len(bd_cript_4h) == 0:
                    bd_cript = bd_cript_6h
                elif len(bd_cript_6h) > 0 and len(bd_cript_4h) > 0:
                    for i in bd_cript_6h:
                        for j in bd_cript_4h:
                            if i['name_cript'][:-3] == j['name_cript'][:-3]:
                                bd_cript_4h.remove(j)
                    bd_cript = bd_cript_6h + bd_cript_4h
                else:
                    bd_cript = bd_cript_4h

                for j in bd_cript:
                    reit_bd_cript.append([j['name_cript'], j["res"], j["price_change_percent_24h"], j["awerage_high_frame"], j["high_close_change"], j["res_k_low"]])

                """Алгоритм сортировки по рейтингу (падение за таймфрейм(4 часа) и изменение цены за сутки)"""
                reit_timeframe_change = [i[0] for i in sorted(reit_bd_cript, key=lambda x: x[1])]
                reit_day_change = [i[0] for i in sorted(reit_bd_cript, key=lambda x: x[2])]
                reit_awerage_high_frame = [i[0] for i in sorted(reit_bd_cript, key=lambda x: -x[3])]

                """Формируем список крипт со значениями"""
                itog = []
                for i in reit_timeframe_change:
                    for j in reit_bd_cript:
                        if i == j[0]:
                            itog.append([i, reit_timeframe_change.index(i), reit_day_change.index(i), reit_awerage_high_frame.index(i), j[4], j[5], j[1]])

                """Определяем топ крипту и оставшийся массив для доп закупа"""
                # top = sorted(reit_bd_cript, key=lambda x: -x[4])[0][0]
                # all_work_crypt = sorted(reit_bd_cript, key=lambda x: -x[4])
                top = sorted([[i[0][:-3], i[1] + i[2], i[5], i[6]] for i in itog], key=lambda x: x[1])[0][0]
                all_work_crypt = sorted([[i[0][:-3], i[1] + i[2], i[5], i[6]] for i in itog], key=lambda x: x[1])

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
                                                                        f"РЕЙТИНГ - {sorted([[i[0], i[1] + i[2], i[5]] for i in itog], key=lambda x: x[1])}\n"
                                                                        f"------------------------\n"
                                                                        f"Количество триггеров - {len(bd_cript)}\n")


                    try:
                        order_buy = client.create_order(symbol=name_cript_check, side='BUY', type='MARKET',
                                                            quantity=buy_qty)
                    except BinanceAPIException as e:
                        if e.message == "Filter failure: LOT_SIZE":
                            buy_qty = int(round(11 / data_token.close_price[-1], 1))
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

                    """Алгоритм продажи"""
                    while open_position:
                        data_token: Dataset = last_data(name_cript_check, "4h", "1440")
                        last_time = time.time()
                        all_orders = pd.DataFrame(client.get_all_orders(symbol=name_cript_check), columns=["orderId", "type", "side", "price", "status"])
                        balance = client.get_asset_balance(asset=name_cript_check[:-4])
                        sell_qty = float(balance["free"])
                            # sell_qty = Decimal(sell_qty).quantize(Decimal(okr), ROUND_FLOOR)
                        try:
                            x = Decimal(str(round((buyprice / 100) * sell_pr,
                                                  max([len(f'{i:.15f}'.rstrip("0").split(".")[1]) for i in
                                                       data_token[0][-5:]]))))

                        except BinanceAPIException as e:
                            telebot.TeleBot(telega_token).send_message(chat_id, f"SELL ERROR 1: {e}\n"
                                                                                f"buyprice - {buyprice}, sell_pr - {sell_pr}\n"
                                                                                f"Количество продаваемого - {sell_qty}, Цена - {x}\n"
                                                                                f"Монеты в кошельке - {float(sell_qty)}, Количество открытых ордеров - {len(all_orders[all_orders.isin(['NEW']).any(axis=1)])}")
                            time.sleep(2)

                            try:
                                x = round((buyprice / 100) * sell_pr,
                                          max([len(str(i).split(".")[1]) for i in data_token[0][-5:]]))
                            except BinanceAPIException as e:
                                telebot.TeleBot(telega_token).send_message(chat_id, f"SELL ERROR: {e}\n"
                                                                                    f"Количество продаваемого - {sell_qty}, Цена - {x}\n"
                                                                                    f"Монеты в кошельке - {float(sell_qty)}, Количество открытых ордеров - {len(all_orders[all_orders.isin(['NEW']).any(axis=1)])}")
                                time.sleep(2)

                                try:
                                    x = Decimal(str(round((buyprice / 100) * sell_pr,
                                                          max([len(f'{i:.15f}'.rstrip("0").split(".")[1]) for i in
                                                               data_token[0][-5:]]))))
                                except BinanceAPIException as e:
                                    telebot.TeleBot(telega_token).send_message(chat_id, f"SELL ERROR: {e}\n"
                                                                                        f"Количество продаваемого - {int(sell_qty)}, Цена - {x}\n"
                                                                                        f"Монеты в кошельке - {float(sell_qty)}, Количество открытых ордеров - {len(all_orders[all_orders.isin(['NEW']).any(axis=1)])}")
                                    time.sleep(2)

                                    try:
                                        x = round((buyprice / 100) * sell_pr,
                                                  max([len(str(i).split(".")[1]) for i in data_token[0][-5:]]))
                                    except BinanceAPIException as e:
                                        telebot.TeleBot(telega_token).send_message(chat_id, f"ВСЕ РАВНО ФЕЙЛ: {e}\n"
                                                                                            f"Количество продаваемого - {int(sell_qty)}, Цена - {x}\n"
                                                                                            f"Монеты в кошельке - {float(sell_qty)}, Количество открытых ордеров - {len(all_orders[all_orders.isin(['NEW']).any(axis=1)])}")

                        high_k_now_price = round(data_token.high_price[-1] / data_token.close_price[-1] * 100 - 100, 2)

                        if sell_qty > 0.05 and len(all_orders[all_orders.isin(["NEW"]).any(axis=1)]) == 0 and data_token.close_price[-1] >= x and high_k_now_price > 0.2:
                            balance = client.get_asset_balance(asset=name_cript_check[:-4])
                            sell_qty = float(balance["free"])
                            order_sell = client.order_market_sell(symbol=name_cript_check, quantity=sell_qty)


                        sell_qty = float(balance["free"])

                        if float(sell_qty) < 0.05 and len(all_orders[all_orders.isin(["NEW"]).any(axis=1)]) == 0:
                            open_position = False
                            orders = client.get_all_orders(symbol=name_cript_check, limit=1)
                            price = round(float(orders[0]['cummulativeQuoteQty']) / float(orders[0]["origQty"]), 7)
                            bot = telebot.TeleBot(telega_token)
                            message = f"СДЕЛКА ЗАВЕРШЕНА - {name_cript_check}\n" \
                                      f"\n" \
                                      f"ПРИБЫЛЬ СО СДЕЛКИ: +{round(100 - 100 * (buyprice / price), 2)}%\n" \
                                      f"\n" \
                                      f"https://www.binance.com/ru/trade/{name_cript_check[:-4]}_USDT?_from=markets&theme=dark&type=grid"
                            bot.send_message(chat_id, message)

                        if last_time - start_time > 45300:
                            # if buyprice * 0.90 > data_token.close_price[-1]:
                            #     telebot.TeleBot(telega_token).send_message(chat_id,
                            #                                                f"ОБВАЛ!!!!!!!!!!!! ------>>>>> {name_cript_check}")
                            #     break
                            # else:

                            orders = client.get_open_orders(symbol=name_cript_check)
                            for order in orders:
                                ordId = order["orderId"]
                                client.cancel_order(symbol=name_cript_check, orderId=ordId)

                            try:
                                balance = client.get_asset_balance(asset=name_cript_check[:-4])
                                sell_qty = float(balance["free"])
                                order_sell = client.order_market_sell(symbol=name_cript_check, quantity=sell_qty)
                                orders = client.get_all_orders(symbol=name_cript_check, limit=1)
                                price = round(float(orders[0]['cummulativeQuoteQty']) / float(orders[0]["origQty"]),7)
                                telebot.TeleBot(telega_token).send_photo(chat_id, 'https://github.com/bibar228/hhru-analize/blob/main/patrik_35715679_orig_.jpg?raw=true', caption=
                                                                                    f"ВРЕМЯ ИСТЕКЛО - {name_cript_check}"
                                                                                    f"Продажа по времени {price}\n"
                                                                                    f"Покупал за {buyprice}\n"
                                                                                    f"Разница {round(100 - 100 * (buyprice / price), 2)}%")
                                open_position = False

                            except Exception as e:
                                telebot.TeleBot(telega_token).send_message(chat_id,
                                                                                   f"Ошибка продажи в минус, Нужен хелп!\n"
                                                                                   f"{e}")
                                time.sleep(1)
                                break


                        time.sleep(1)

                    max_price = max(data_token[0])

                    time.sleep(1)

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
                            sell_pr = 100.95

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
                                    buy_qty = round(11 / data_token.close_price[-1], 1)
                                    telebot.TeleBot(telega_token).send_message(chat_id, f"!!!!!!!!!!!!!ДОП АЛГОРИТМ!!!!!!!!!!!!!\n"
                                                                                        f"РАБОТАЕМ С {i[0]}\n"
                                                                                        f"Изменение цены сейчас относительно начала фрейма: {res_now}%\n"
                                                                                        f"Максимальный рост цены в этот фрейм: {res_past}%\n")
                                    new_alg_crypto_work_end.append(i[0])

                                    try:
                                        order_buy = client.create_order(symbol=i[0], side='BUY', type='MARKET', quantity=buy_qty)
                                    except BinanceAPIException as e:
                                        if e.message == "Filter failure: LOT_SIZE":
                                            buy_qty = int(round(11 / data_token.close_price[-1], 1))
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

                                    """Алгоритм продажи"""
                                    while open_position:
                                        data_token: Dataset = last_data(i[0], "4h", "1440")
                                        last_time_dop_alg = time.time()
                                        all_orders = pd.DataFrame(client.get_all_orders(symbol=i[0]), columns=["orderId", "type", "side", "price", "status"])
                                        balance = client.get_asset_balance(asset=i[0][:-4])
                                        sell_qty = float(balance["free"])
                                        # sell_qty = Decimal(sell_qty).quantize(Decimal(okr), ROUND_FLOOR)
                                        try:
                                            x = Decimal(str(round((buyprice / 100) * sell_pr,
                                                                  max([len(f'{i:.15f}'.rstrip("0").split(".")[1]) for i
                                                                       in
                                                                       data_token[0][-5:]]))))

                                        except BinanceAPIException as e:
                                            telebot.TeleBot(telega_token).send_message(chat_id, f"SELL ERROR 1: {e}\n"
                                                                                                f"buyprice - {buyprice}, sell_pr - {sell_pr}\n"
                                                                                                f"Количество продаваемого - {sell_qty}, Цена - {x}\n"
                                                                                                f"Монеты в кошельке - {float(sell_qty)}, Количество открытых ордеров - {len(all_orders[all_orders.isin(['NEW']).any(axis=1)])}")
                                            time.sleep(2)

                                            try:
                                                x = round((buyprice / 100) * sell_pr,
                                                          max([len(str(i).split(".")[1]) for i in data_token[0][-5:]]))
                                            except BinanceAPIException as e:
                                                telebot.TeleBot(telega_token).send_message(chat_id, f"SELL ERROR: {e}\n"
                                                                                                    f"Количество продаваемого - {sell_qty}, Цена - {x}\n"
                                                                                                    f"Монеты в кошельке - {float(sell_qty)}, Количество открытых ордеров - {len(all_orders[all_orders.isin(['NEW']).any(axis=1)])}")
                                                time.sleep(2)

                                                try:
                                                    x = Decimal(str(round((buyprice / 100) * sell_pr,
                                                                          max([len(
                                                                              f'{i:.15f}'.rstrip("0").split(".")[1]) for
                                                                               i in
                                                                               data_token[0][-5:]]))))
                                                except BinanceAPIException as e:
                                                    telebot.TeleBot(telega_token).send_message(chat_id,
                                                                                               f"SELL ERROR: {e}\n"
                                                                                               f"Количество продаваемого - {int(sell_qty)}, Цена - {x}\n"
                                                                                               f"Монеты в кошельке - {float(sell_qty)}, Количество открытых ордеров - {len(all_orders[all_orders.isin(['NEW']).any(axis=1)])}")
                                                    time.sleep(2)

                                                    try:
                                                        x = round((buyprice / 100) * sell_pr,
                                                                  max([len(str(i).split(".")[1]) for i in
                                                                       data_token[0][-5:]]))
                                                    except BinanceAPIException as e:
                                                        telebot.TeleBot(telega_token).send_message(chat_id,
                                                                                                   f"ВСЕ РАВНО ФЕЙЛ: {e}\n"
                                                                                                   f"Количество продаваемого - {int(sell_qty)}, Цена - {x}\n"
                                                                                                   f"Монеты в кошельке - {float(sell_qty)}, Количество открытых ордеров - {len(all_orders[all_orders.isin(['NEW']).any(axis=1)])}")

                                        high_k_now_price = round(
                                            data_token.high_price[-1] / data_token.close_price[-1] * 100 - 100, 2)

                                        if sell_qty > 0.05 and len(all_orders[all_orders.isin(["NEW"]).any(axis=1)]) == 0 and \
                                                data_token.close_price[-1] >= x and high_k_now_price > 0.2:
                                            balance = client.get_asset_balance(asset=name_cript_check[:-4])
                                            sell_qty = float(balance["free"])
                                            order_sell = client.order_market_sell(symbol=name_cript_check,
                                                                                  quantity=sell_qty)

                                        sell_qty = float(balance["free"])

                                        if float(sell_qty) < 0.05 and len(all_orders[all_orders.isin(["NEW"]).any(axis=1)]) == 0:
                                            open_position = False
                                            orders = client.get_all_orders(symbol=name_cript_check, limit=1)
                                            price = round(float(orders[0]['cummulativeQuoteQty']) / float(orders[0]["origQty"]), 7)
                                            bot = telebot.TeleBot(telega_token)
                                            message = f"СДЕЛКА ЗАВЕРШЕНА - {name_cript_check}\n" \
                                                      f"\n" \
                                                      f"ПРИБЫЛЬ СО СДЕЛКИ: +{round(100 - 100 * (buyprice / price), 2)}%\n" \
                                                      f"\n" \
                                                      f"https://www.binance.com/ru/trade/{name_cript_check[:-4]}_USDT?_from=markets&theme=dark&type=grid"
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
                                                time.sleep(1)
                                                break


                                        time.sleep(1)

                                    max_price = max(data_token[0])

                                    time.sleep(1)

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
    while time.localtime(start_time_check).tm_min % 15 != 14 or time.localtime(start_time_check).tm_sec < 30:
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

