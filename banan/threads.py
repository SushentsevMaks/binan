import time
from decimal import Decimal
from datetime import datetime
# from decimal import Decimal, ROUND_FLOOR
from binance.client import Client
from binance.exceptions import BinanceAPIException
import keys
import pandas as pd
import telebot
from sql_request import sql_req
from threading import Thread
from typing import NamedTuple

telega_token = "5926919919:AAFCHFocMt_pdnlAgDo-13wLe4h_tHO0-GE"

client = Client(keys.api_key, keys.api_secret)
# futures_exchange_info = client.futures_exchange_info()
# trading_pairs = [info['symbol'] for info in futures_exchange_info['symbols'] if info['symbol'][-4:] == "USDT"]

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

fifteenth = ['VTHOUSDT', 'WANUSDT', 'WAVESUSDT', 'WAXPUSDT', 'WBETHUSDT', 'WINGUSDT', 'WINUSDT', 'WLDUSDT', 'WNXMUSDT',
             'WOOUSDT', 'WRXUSDT', 'WTCUSDT', 'XECUSDT', 'XEMUSDT', 'XLMUSDT', 'XMRUSDT', 'XNOUSDT', 'XRPUSDT',
             'XVGUSDT', 'XVSUSDT', 'YFIUSDT']

ex = {}

chat_id = -695765690

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

keks = {}


def top_coin(trading_pairs: list):
    for name_cript_check in trading_pairs:
        start = time.time()
        if name_cript_check not in ex or start - ex[name_cript_check] > 12000:
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
                # print(name_cript_check)
                now = datetime.now()
                frame = now.strftime("%H:%M:%S")

                if ((price_change_in_3min > 3 or price_change_in_2min > 3)
                        and data_token.high_price[-3:] == sorted(data_token.high_price[-3:])
                        and (name_cript_check not in keks or start-keks[name_cript_check] > 12000)):

                    if name_cript_check in trading_pairs_fut:
                        fut_yes = "Фьючерсная"
                    else:
                        fut_yes = "НЕ Фьючерсная"

                    telebot.TeleBot(telega_token).send_message(chat_id, f"ОБЪЕМЫ МЕНЬШЕ 250 - {name_cript_check}\n"
                                                                        f"Цены {data_token.high_price[-8:]}\n"
                                                                        f"Объемы {int(volume_per_5h)}\n"
                                                                        f"Изменение цены за 6 мин {round(price_change_in_6min, 2)}%  {round(price_change_in_6min - price_change_in_5min, 2)}%\n"
                                                                        f"Изменение цены за 5 мин {round(price_change_in_5min, 2)}%  {round(price_change_in_5min - price_change_in_4min, 2)}%\n"
                                                                        f"Изменение цены за 4 мин {round(price_change_in_4min, 2)}%  {round(price_change_in_4min - price_change_in_3min, 2)}%\n"
                                                                        f"Изменение цены за 3 мин {round(price_change_in_3min, 2)}%  {round(price_change_in_3min - price_change_in_2min, 2)}%\n"
                                                                        f"Изменение цены за 2 мин {round(price_change_in_2min, 2)}%\n"
                                                                        f"Изменение цены за 24ч  {round(price_change_percent_24h, 2)}%\n"
                                                                        f"Изменение цены от минимальной за 24ч  {round(price_change_percent_min_24h, 2)}%\n"
                                                                        f"Изменение цены от максимальной за 24ч  {round(price_change_percent_max_24h, 2)}%\n"
                                                                        f"Время засечки  {frame}%\n"
                                                                        f"{fut_yes}")
                    keks[name_cript_check] = time.time()

                # and price_change_percent_min_24h < 20 \
                # and price_change_percent_max_24h < 20
                if ((4.7 > price_change_in_2min > 2.4 and 4.7 > price_change_in_3min - price_change_in_2min > 0.85
                     and (price_change_in_4min - price_change_in_3min > -0.3 or (price_change_in_4min - price_change_in_3min + price_change_in_5min - price_change_in_4min) > 1)
                     and price_change_in_4min - price_change_in_3min != 0
                     and price_change_in_5min - price_change_in_4min > -0.3
                     and price_change_in_6min - price_change_in_5min > -0.9)
                    or (4.7 > price_change_in_2min > 0.85 and 4.7 > price_change_in_3min - price_change_in_2min > 2.3
                        and (price_change_in_4min - price_change_in_3min > -0.3 or (price_change_in_4min - price_change_in_3min + price_change_in_5min - price_change_in_4min) > 1)
                        and price_change_in_4min - price_change_in_3min != 0
                        and price_change_in_5min - price_change_in_4min > -0.3
                        and price_change_in_6min - price_change_in_5min > -0.9)
                    or (4.7 > price_change_in_2min > 1.25 and 4.7 > price_change_in_3min - price_change_in_2min > 1.25
                        and (price_change_in_4min - price_change_in_3min > -0.3 or (price_change_in_4min - price_change_in_3min + price_change_in_5min - price_change_in_4min) > 1)
                        and price_change_in_4min - price_change_in_3min != 0
                        and price_change_in_5min - price_change_in_4min > -0.3
                        and price_change_in_6min - price_change_in_5min > -0.9)
                    or (4.7 > price_change_in_2min > 1.5 and 4.7 > price_change_in_4min - price_change_in_3min > 1.5
                        and price_change_in_3min - price_change_in_2min > 0
                        and price_change_in_5min - price_change_in_4min > -0.3
                        and price_change_in_6min - price_change_in_5min > -0.9)) \
                    and price_change_in_5min < 10 \
                    and 10 > price_change_percent_24h > -8 \
                    and volume_per_5h > 250:

                    buy_qty = round(11 / data_token.high_price[-1], 1)
                    if name_cript_check in trading_pairs_fut:
                        fut_yes = "Фьючерсная"
                    else:
                        fut_yes = "НЕ Фьючерсная"
                    telebot.TeleBot(telega_token).send_message(chat_id, f"RABOTAEM - {name_cript_check}\n"
                                                                        f"Количество покупаемого - {buy_qty}, Цена - {data_token.high_price[-1]}\n"
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
                                                                        f"Изменение цены от минимальной за 24ч  {round(price_change_percent_min_24h, 2)}%\n"
                                                                        f"Изменение цены от максимальной за 24ч  {round(price_change_percent_max_24h, 2)}%\n"
                                                                        f"Время покупки {frame}\n"
                                                                        f"{fut_yes}")


                    start_time = time.time()
                    try:
                        order_buy = client.create_order(symbol=name_cript_check, side='BUY', type='MARKET', quantity=buy_qty)
                    except BinanceAPIException as e:
                        if e.message == "Filter failure: LOT_SIZE":
                            buy_qty = int(round(11 / data_token.high_price[-1], 1))
                            try:
                                order_buy = client.create_order(symbol=name_cript_check, side='BUY', type='MARKET', quantity=buy_qty)
                            except:
                                telebot.TeleBot(telega_token).send_message(chat_id, f"BUY ERROR: {e.message}\n"
                                                                                    f"Количество покупаемого - {buy_qty}, Цена - {data_token.high_price[-1]}")
                                time.sleep(1)
                                break
                        else:
                            telebot.TeleBot(telega_token).send_message(chat_id, f"BUY ERROR: {e.message}\n"
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


                    while open_position:
                        last_time = time.time()
                        all_orders = pd.DataFrame(client.get_all_orders(symbol=name_cript_check),
                                                  columns=["orderId", "type", "side", "price", "status"])
                        balance = client.get_asset_balance(asset=name_cript_check[:-4])
                        sell_qty = float(balance["free"])
                        # sell_qty = Decimal(sell_qty).quantize(Decimal(okr), ROUND_FLOOR)

                        if sell_qty > 0.05 and len(all_orders[all_orders.isin(["NEW"]).any(axis=1)]) == 0:
                            try:
                                order_sell = client.order_limit_sell(symbol=name_cript_check, quantity=sell_qty, price=Decimal(
                                    str(round((buyprice / 100) * 101,
                                              max([len(str(i).split(".")[1]) for i in data_token[0][-5:]])))))
                                time.sleep(10)
                            except Exception as e:
                                telebot.TeleBot(telega_token).send_message(chat_id, f"SELL ERROR: {e}\n"
                                                                                    f"Количество продаваемого - {sell_qty}, Цена - {round((buyprice / 100) * 101, len(str(data_token.high_price[-1]).split('.')[1]))}\n"
                                                                                    f"Монеты в кошельке - {float(sell_qty)}, Количество открытых ордеров - {len(all_orders[all_orders.isin(['NEW']).any(axis=1)])}")
                                time.sleep(1)
                        sell_qty = float(balance["free"])

                        if float(sell_qty) < 0.05 and len(all_orders[all_orders.isin(["NEW"]).any(axis=1)]) == 0:
                            open_position = False
                            frame = now.strftime("%H:%M:%S")
                            bot = telebot.TeleBot(telega_token)
                            message = f"СДЕЛКА ЗАВЕРШЕНА - {name_cript_check}\n" \
                                      f"{data_token.high_price[-3:]}\n" \
                                      f"ЗАСЕК НА РОСТЕ ЦЕНЫ В {round(price_change_in_5min, 2)}%\n" \
                                      f"Время продажи {frame}\n" \
                                      f"\n" \
                                      f"https://www.binance.com/ru/trade/{name_cript_check[:-4]}_USDT?_from=markets&theme=dark&type=grid"
                            bot.send_message(chat_id, message)

                        if int(last_time-start_time) > 9050:
                            data_token = last_data(name_cript_check, "1m", "1440")
                            prices_token = data_token[0][300:]
                            orders = client.get_all_orders(symbol=name_cript_check, limit=2)[0]
                            price = round(float(orders['cummulativeQuoteQty']) / float(orders["origQty"]), 7)

                            orders = client.get_open_orders(symbol=name_cript_check)
                            for order in orders:
                                ordId = order["orderId"]
                                client.cancel_order(symbol=name_cript_check, orderId=ordId)

                            try:
                                balance = client.get_asset_balance(asset=name_cript_check[:-4])
                                sell_qty = float(balance["free"])
                                order_sell = client.order_market_sell(symbol=name_cript_check, quantity=sell_qty)
                                orders = client.get_all_orders(symbol=name_cript_check, limit=1)
                                price = round(float(orders[0]['cummulativeQuoteQty']) / float(orders[0]["origQty"]), 7)
                                telebot.TeleBot(telega_token).send_message(chat_id,
                                                                               f"Продажа в минус за {price}\n"
                                                                               f"Покупал за {buyprice}\n"
                                                                               f"Разница {round(100 - 100*(buyprice/price)), 2}%")
                                open_position = False
                            except Exception as e:
                                telebot.TeleBot(telega_token).send_message(chat_id,
                                                                               f"Ошибка продажи в минус, Нужен хелп!\n"
                                                                               f"{e}")
                                time.sleep(1)
                                break

                        time.sleep(1)

                    start = time.time()
                    finish = 0
                    while finish - start < 600:
                        finish = time.time()

                    data_tok: Dataset = last_data(name_cript_check, "1m", "11")
                    max_price = max(data_tok[0])

                    sql_req(name_cript_check, price_change_percent_24h, price_change_in_2min, price_change_in_3min,
                            price_change_in_4min, price_change_in_5min, volume_per_5h, price_change_percent_min_24h,
                            price_change_percent_max_24h, max_price)

                    ex[name_cript_check] = time.time()
            except:
                pass


class Dataset(NamedTuple):
    high_price: list
    volume: list
    close_price: list


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
                   close_price=[i.Close for i in frame.itertuples()])


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
    if btc_anal(last_data("BTCUSDT", "1m", "5")):
        threads = [Thread(target=top_coin, args=([one])), Thread(target=top_coin, args=([two])),
                   Thread(target=top_coin, args=([three])),
                   Thread(target=top_coin, args=([four])), Thread(target=top_coin, args=([five])),
                   Thread(target=top_coin, args=([six])),
                   Thread(target=top_coin, args=([seven])), Thread(target=top_coin, args=([eight])),
                   Thread(target=top_coin, args=([nine])),
                   Thread(target=top_coin, args=([ten])), Thread(target=top_coin, args=([eleven])),
                   Thread(target=top_coin, args=([twelve])),
                   Thread(target=top_coin, args=([thirteenth])), Thread(target=top_coin, args=([fourteenth])),
                   Thread(target=top_coin, args=([fifteenth]))]

        start_threads = [i.start() for i in threads]

        stop_threads = [i.join() for i in threads]
    else:
        time.sleep(1000)
