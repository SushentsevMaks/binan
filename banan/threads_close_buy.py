import time
from decimal import Decimal
from datetime import datetime
from binance.client import Client
from binance.exceptions import BinanceAPIException
import keys
import pandas as pd
import telebot
from sql_request import sql_req_str2, equal, sql_del, get_top_crypto
from threading import Thread
from typing import NamedTuple
from tradingview_ta import TA_Handler, Interval, Exchange

telega_token = "5926919919:AAFCHFocMt_pdnlAgDo-13wLe4h_tHO0-GE"

client = Client(keys.api_key, keys.api_secret)
# futures_exchange_info = client.futures_exchange_info()
# trading_pairs = [info['symbol'] for info in futures_exchange_info['symbols'] if info['symbol'][-4:] == "USDT"]

one = ['1INCHUSDT', 'AAVEUSDT', 'ACHUSDT', 'ACMUSDT', 'ADAUSDT']

onegop = ['AERGOUSDT', 'AGIXUSDT', 'AGLDUSDT', 'ALCXUSDT', 'ALGOUSDT']

onedop = ['ALICEUSDT', 'ALPACAUSDT', 'ALPHAUSDT', 'ALPINEUSDT', 'AMBUSDT']

onemop = ['AMPUSDT', 'ANKRUSDT', 'ANTUSDT', 'APEUSDT', 'API3USDT']

two = ['APTUSDT', 'ARBUSDT', 'ARDRUSDT', 'ARKMUSDT', 'ARPAUSDT']

twogop = ['ARUSDT', 'ASRUSDT', 'ATMUSDT', 'ATOMUSDT', 'AUCTIONUSDT']

twodop = ['AUDIOUSDT', 'AVAXUSDT', 'AXSUSDT', 'BADGERUSDT', 'BAKEUSDT']

twomop = ['BALUSDT', 'BANDUSDT', 'BARUSDT', 'BATUSDT', 'ARKUSDT']

three = ["BEAMXUSDT", 'BCHUSDT', 'BELUSDT', 'BETAUSDT', 'BICOUSDT']

threegop = ['BIFIUSDT', 'BLZUSDT', 'BNXUSDT', 'BONDUSDT', 'YGGUSDT']

threedop = ['ZECUSDT', 'ZENUSDT', 'ZILUSDT', 'ZRXUSDT', 'BURGERUSDT', 'C98USDT', 'CAKEUSDT']

threemop = ['CELRUSDT', 'CFXUSDT', 'CHESSUSDT', 'CHRUSDT', 'CHZUSDT']

four = ['CITYUSDT', 'CKBUSDT', 'CLVUSDT', 'COMPUSDT', 'COTIUSDT']

fourgop = ['CRVUSDT', 'CTSIUSDT', 'CTXCUSDT', 'CVCUSDT']

fourdop = ['CVPUSDT', 'CVXUSDT', 'CYBERUSDT', 'DARUSDT', 'DASHUSDT', 'DATAUSDT']

fourmop = ['DCRUSDT', 'DEGOUSDT', 'DENTUSDT', 'DEXEUSDT', 'DFUSDT']

five = ['DIAUSDT', 'DODOUSDT', 'DOGEUSDT', 'DOTUSDT', 'DREPUSDT']

fivegop = ['DUSKUSDT', 'DYDXUSDT', 'EDUUSDT', 'EGLDUSDT', 'ELFUSDT']

fivedop = ['ENJUSDT', 'ENSUSDT', 'EPXUSDT', 'ETCUSDT']

fivemop = ['FARMUSDT', 'FETUSDT', 'FIDAUSDT', 'GFTUSDT']

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

fourteenthdop = ['UNIUSDT', 'USTCUSDT', 'VETUSDT', 'VGXUSDT', 'XVGUSDT']

fourteenthmop = ['VIBUSDT', 'VIDTUSDT', 'VITEUSDT', 'VOXELUSDT', 'YFIUSDT']

fifteenth = ['WANUSDT', 'WAVESUSDT', 'WAXPUSDT', 'WBETHUSDT']

fifteenthgop = ['WLDUSDT', 'WNXMUSDT', 'WOOUSDT', 'WRXUSDT', 'WTCUSDT']

fifteenthdop = ['XECUSDT', 'XEMUSDT', 'XLMUSDT', 'XMRUSDT', 'XRPUSDT']

izg = ["HIFIUSDT", "CREAMUSDT", 'QIUSDT']

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
        if name_cript_check not in ex or start - ex[name_cript_check] > 60:
            try:
                # print(name_cript_check)
                # print(last_data(name_cript_check, "3m", "300"))

                data_token: Dataset = last_data(name_cript_check, "1h", "1440")
                volume_per_5h: float = sum([int(i * data_token.high_price[-1]) for i in data_token.volume[-2:]]) / len(data_token.volume[-2:]) / 60
                res: float = round(data_token.close_price[-1] / data_token.open_price[-1] * 100 - 100, 2)
                res_before: float = round(data_token.close_price[-2] / data_token.open_price[-2] * 100 - 100, 2)
                price_change_percent_24h: float = round(((data_token.close_price[-2] / data_token.close_price[0]) * 100) - 100, 2)


                '''процент падения за последние 2ч. Отрицательные значение == был рост'''
                loss_price_for_two_hours: float = round(100 - data_token.close_price[-2] / max([i for i in data_token.open_price[-9:]]) * 100, 2)

                if -4.8 > res and volume_per_5h > 6500 and max(data_token.high_price) != data_token.high_price[-1]:

                    # try:
                    #     data_token_check: Dataset = last_data(name_cript_check, "1m", "15")
                    #     low_price = data_token_check.low_price
                    #     low_price_index = data_token_check.low_price.index(min(data_token.low_price))
                    # except BinanceAPIException as e:
                    #     telebot.TeleBot(telega_token).send_message(chat_id, f"ERROR in start: {e}\n")
                    #     low_price = 0
                    #     low_price_index = 0

                    buy_qty = round(40 / data_token.close_price[-1], 1)

                    telebot.TeleBot(telega_token).send_message(chat_id, f"RABOTAEM - {name_cript_check}\n"
                                                                            f"Количество покупаемого - {buy_qty}\n"
                                                                            f"На сколько упала цена за последние 2ч {loss_price_for_two_hours}% (Отриц. знач. == был рост)\n"
                                                                            f"Объемы {int(volume_per_5h)}\n"
                                                                            f"Цена упала на {res}%\n"
                                                                            f"Изменение цены за сутки {price_change_percent_24h}%\n"
                                                                            f"Изменение цены за прошлый таймфрейм {res_before}%\n")
                    '''Добавляем в базу найденный объект'''
                    equal(name_cript_check, res)

                    start_time_check = time.time()
                    '''Заглушка для ожидания конца таймфрейма 15 мин'''
                    while time.localtime(start_time_check).tm_min != 59 or time.localtime(start_time_check).tm_sec < 58:
                        start_time_check = time.time()
                        time.sleep(1)

                    '''Проверка на наилучший объект и работа с ним дальше'''
                    if name_cript_check == get_top_crypto():

                        start_time = time.time()
                        try:
                            order_buy = client.create_order(symbol=name_cript_check, side='BUY', type='MARKET',
                                                            quantity=buy_qty)
                        except BinanceAPIException as e:
                            if e.message == "Filter failure: LOT_SIZE":
                                buy_qty = int(round(40 / data_token.close_price[-1], 1))
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

                        while open_position:
                            last_time = time.time()
                            all_orders = pd.DataFrame(client.get_all_orders(symbol=name_cript_check),
                                                      columns=["orderId", "type", "side", "price", "status"])
                            balance = client.get_asset_balance(asset=name_cript_check[:-4])
                            sell_qty = float(balance["free"])
                            # sell_qty = Decimal(sell_qty).quantize(Decimal(okr), ROUND_FLOOR)

                            if sell_qty > 0.05 and len(all_orders[all_orders.isin(["NEW"]).any(axis=1)]) == 0:
                                try:
                                    order_sell = client.order_limit_sell(symbol=name_cript_check, quantity=sell_qty,
                                                                         price=Decimal(
                                                                             str(round((buyprice / 100) * 101.15,
                                                                                       max([len(str(i).split(".")[1]) for i
                                                                                            in data_token[0][-5:]])))))
                                    time.sleep(10)
                                except Exception as e:
                                    telebot.TeleBot(telega_token).send_message(chat_id, f"SELL ERROR: {e}\n"
                                                                                        f"Количество продаваемого - {sell_qty}, Цена - {round((buyprice / 100) * 100.99, len(str(data_token.high_price[-1]).split('.')[1]))}\n"
                                                                                        f"Монеты в кошельке - {float(sell_qty)}, Количество открытых ордеров - {len(all_orders[all_orders.isin(['NEW']).any(axis=1)])}")
                                    order_sell = client.order_limit_sell(symbol=name_cript_check, quantity=sell_qty,
                                                                         price=str(Decimal(
                                                                             str(round((buyprice / 100) * 101.15,
                                                                                       max([len(str(i).split(".")[1]) for i
                                                                                            in data_token[0][-5:]])))))[:-1])
                                    time.sleep(1)

                            sell_qty = float(balance["free"])

                            if float(sell_qty) < 0.05 and len(all_orders[all_orders.isin(["NEW"]).any(axis=1)]) == 0:
                                open_position = False
                                bot = telebot.TeleBot(telega_token)
                                message = f"СДЕЛКА ЗАВЕРШЕНА - {name_cript_check}\n" \
                                          f"\n" \
                                          f"https://www.binance.com/ru/trade/{name_cript_check[:-4]}_USDT?_from=markets&theme=dark&type=grid"
                                bot.send_message(chat_id, message)

                            if last_time - start_time > 1795:

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
                                                                                    f"Продажа в минус за {price}\n"
                                                                                   f"Покупал за {buyprice}\n"
                                                                                   f"Разница {round(100 - 100 * (buyprice / price), 2)}%")
                                    open_position = False

                                except Exception as e:
                                    telebot.TeleBot(telega_token).send_message(chat_id,
                                                                                   f"Ошибка продажи в минус, Нужен хелп!\n"
                                                                                   f"{e}")
                                    time.sleep(1)
                                    break

                            if buyprice * 0.965 > data_token.close_price[-1]:
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
                                    telebot.TeleBot(telega_token).send_photo(chat_id,
                                                                             'https://github.com/bibar228/hhru-analize/blob/main/patrik_35715679_orig_.jpg?raw=true',
                                                                             caption=
                                                                             f"Продажа в минус за {price}\n"
                                                                             f"Покупал за {buyprice}\n"
                                                                             f"Разница {round(100 - 100 * (buyprice / price), 2)}%")
                                    open_position = False

                                except Exception as e:
                                    telebot.TeleBot(telega_token).send_message(chat_id,
                                                                               f"Ошибка СТОП ЛОССА, Нужен хелп!\n"
                                                                               f"{e}")
                                    time.sleep(1)
                                    break

                            data_token: Dataset = last_data(name_cript_check, "15m", "1440")

                            time.sleep(10)

                        max_price = max(data_token[0])

                        time.sleep(1)

                        sql_req_str2(name_cript_check, price_change_percent_24h, volume_per_5h, max_price, loss_price_for_two_hours, res)

                        ex[name_cript_check] = time.time()

                        sql_del()
                    else:
                        break

                if -4.8 > res and volume_per_5h > 6500 and max(data_token.high_price) == data_token.high_price[-1]:
                    telebot.TeleBot(telega_token).send_message(chat_id,
                                                               f"МАКСИМАЛЬНАЯ ЦЕНА В ЭТОМ ТАЙМ ФРЕЙМЕ, КУКУ")
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
    while time.localtime(start_time_check).tm_min != 59 or time.localtime(start_time_check).tm_sec < 48:
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
               Thread(target=top_coin, args=([fifteenthdop])),
               Thread(target=top_coin, args=([onegop])), Thread(target=top_coin, args=([twogop])),
               Thread(target=top_coin, args=([threegop])),
               Thread(target=top_coin, args=([fourgop])), Thread(target=top_coin, args=([fivegop])),
               Thread(target=top_coin, args=([sixgop])),
               Thread(target=top_coin, args=([sevengop])), Thread(target=top_coin, args=([eightgop])),
               Thread(target=top_coin, args=([ninegop])),
               Thread(target=top_coin, args=([tengop])), Thread(target=top_coin, args=([elevengop])),
               Thread(target=top_coin, args=([twelvegop])),
               Thread(target=top_coin, args=([thirteenthgop])), Thread(target=top_coin, args=([fourteenthgop])),
               Thread(target=top_coin, args=([fifteenthgop])),
               Thread(target=top_coin, args=([onemop])), Thread(target=top_coin, args=([twomop])),
               Thread(target=top_coin, args=([threemop])),
               Thread(target=top_coin, args=([fourmop])), Thread(target=top_coin, args=([fivemop])),
               Thread(target=top_coin, args=([sixmop])),
               Thread(target=top_coin, args=([sevenmop])), Thread(target=top_coin, args=([eightmop])),
               Thread(target=top_coin, args=([ninemop])),
               Thread(target=top_coin, args=([tenmop])), Thread(target=top_coin, args=([elevenmop])),
               Thread(target=top_coin, args=([twelvemop])),
               Thread(target=top_coin, args=([thirteenthmop])), Thread(target=top_coin, args=([fourteenthmop]))]

    start_threads = [i.start() for i in threads]

    stop_threads = [i.join() for i in threads]







