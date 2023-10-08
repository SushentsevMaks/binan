import time
from decimal import Decimal

#from decimal import Decimal, ROUND_FLOOR
from binance.client import Client
from binance.exceptions import BinanceAPIException
import keys
import pandas as pd
import telebot
from sql_request import sql_req

telega_token = "5926919919:AAFCHFocMt_pdnlAgDo-13wLe4h_tHO0-GE"


client = Client(keys.api_key, keys.api_secret)
# futures_exchange_info = client.futures_exchange_info()
# trading_pairs = [info['symbol'] for info in futures_exchange_info['symbols'] if info['symbol'][-4:] == "USDT"]
trading_pairs = ['PERLUSDT', 'PERPUSDT', 'PHAUSDT', 'PHBUSDT', 'PLAUSDT', 'PNTUSDT', 'POLSUSDT', 'POLYXUSDT', 'PONDUSDT', 'PORTOUSDT', 'POWRUSDT', 'PROMUSDT', 'PROSUSDT', 'PSGUSDT', 'PUNDIXUSDT', 'PYRUSDT', 'QIUSDT', 'QKCUSDT', 'QNTUSDT', 'QTUMUSDT', 'QUICKUSDT', 'RADUSDT', 'RAREUSDT']

ex = []

chat_id = -695765690

trading_pairs_fut = ['LEVERUSDT', 'USDCUSDT', 'AVAXUSDT', 'ATAUSDT', 'ACHUSDT', 'ARPAUSDT', 'CYBERUSDT', 'CHZUSDT', 'RNDRUSDT',
                     'MASKUSDT', 'MTLUSDT', 'XTZUSDT', 'BTCUSDT', 'XRPUSDT', 'CFXUSDT', 'ASTRUSDT', 'NEARUSDT', 'AGIXUSDT',
                     'API3USDT', 'EOSUSDT', 'IDEXUSDT', 'WLDUSDT', 'RAYUSDT', 'THETAUSDT', 'FTMUSDT', 'XMRUSDT', 'BATUSDT',
                     'ENSUSDT', 'FILUSDT', 'ALGOUSDT', 'SEIUSDT', 'STGUSDT', 'ROSEUSDT', 'INJUSDT', 'TUSDT', 'SOLUSDT', 'HIGHUSDT',
                     'YGGUSDT', 'TRBUSDT', 'UNIUSDT', 'FLMUSDT', 'LQTYUSDT', 'ARKMUSDT', 'YFIUSDT', 'PEOPLEUSDT', 'IOSTUSDT',
                     'COMBOUSDT', 'MATICUSDT', 'DUSKUSDT', 'JASMYUSDT', 'CTKUSDT', 'TLMUSDT', 'WOOUSDT', 'NEOUSDT', 'KAVAUSDT',
                     'MAVUSDT', 'PHBUSDT', 'CKBUSDT', 'CVCUSDT', 'IOTAUSDT', 'SFPUSDT', 'COTIUSDT', 'CELOUSDT', 'MINAUSDT',
                     'LTCUSDT', 'NKNUSDT', 'FLOWUSDT', 'ETCUSDT', 'GMTUSDT', 'GTCUSDT', 'SNXUSDT', 'TRXUSDT', 'EGLDUSDT',
                     'CELRUSDT', 'IDUSDT', 'GALAUSDT', 'LITUSDT', 'ADAUSDT', 'CRVUSDT', 'DYDXUSDT', 'DOGEUSDT', 'GALUSDT',
                     'FETUSDT', 'MKRUSDT', 'CTSIUSDT', 'ATOMUSDT', 'ICPUSDT', 'AUDIOUSDT', 'RLCUSDT', 'LDOUSDT', 'AMBUSDT',
                     'OCEANUSDT', 'RDNTUSDT', 'STMXUSDT', 'OMGUSDT', 'APTUSDT', 'HOOKUSDT', 'STORJUSDT', 'CVXUSDT', 'ONTUSDT',
                     'BLZUSDT', 'PERPUSDT', 'SKLUSDT', 'LRCUSDT', 'BNBUSDT', 'BCHUSDT', 'EDUUSDT', 'SPELLUSDT', '1INCHUSDT',
                     'DENTUSDT', 'ZECUSDT', 'CHRUSDT', 'TOMOUSDT', 'KLAYUSDT', 'XEMUSDT', 'RSRUSDT', 'RENUSDT', 'ICXUSDT',
                     'BANDUSDT', 'GMXUSDT', 'ARBUSDT', 'KNCUSDT', 'DASHUSDT', 'TRUUSDT', 'HBARUSDT', 'RUNEUSDT', 'SCUSDT',
                     'DGBUSDT', 'BAKEUSDT', 'SUSHIUSDT', 'HOTUSDT', 'RADUSDT', 'BELUSDT', 'XLMUSDT', 'BTSUSDT', 'QNTUSDT',
                     'MAGICUSDT', 'VETUSDT', 'APEUSDT', 'DARUSDT', 'LINAUSDT', 'NMRUSDT', 'MDTUSDT', 'OPUSDT', 'ANKRUSDT',
                     'SANDUSDT', 'ONEUSDT', 'ARUSDT', 'SXPUSDT', 'ZILUSDT', 'OXTUSDT', 'BALUSDT', 'IMXUSDT', 'DOTUSDT', 'XVGUSDT',
                     'LPTUSDT', 'WAVESUSDT', 'ZENUSDT', 'BNXUSDT', 'ALPHAUSDT', 'COMPUSDT', 'ZRXUSDT', 'SSVUSDT', 'UMAUSDT',
                     'PENDLEUSDT', 'AGLDUSDT', 'UNFIUSDT', 'LINKUSDT', 'ALICEUSDT', 'OGNUSDT', 'REEFUSDT', 'BNTUSDT', 'GRTUSDT',
                     'HFTUSDT', 'STXUSDT', 'IOTXUSDT', 'ANTUSDT', 'C98USDT', 'AXSUSDT', 'AAVEUSDT', 'ENJUSDT', 'RVNUSDT',
                     'MANAUSDT', 'XVSUSDT', 'FXSUSDT', 'SUIUSDT', 'KSMUSDT', 'JOEUSDT', 'KEYUSDT', 'ETHUSDT', 'QTUMUSDT']


keks = []

def top_coin():
    for i in trading_pairs:
        if i not in ex:
            try:
                # print(i)
                # print(last_data(i, "3m", "300"))
                data_token_price = last_data(i, "1m", "1440")
                d = data_token_price[1][900:]
                prices_token = data_token_price[0][300:]
                #volumes_token = [round(d[i] + d[i + 1] + d[i + 2], 2) for i in range(0, len(d), 3)]
                price_change_in_5min = (prices_token[-1] / prices_token[-5]) * 100 - 100
                price_change_in_2min = (prices_token[-1] / prices_token[-2]) * 100 - 100
                price_change_in_3min = (prices_token[-1] / prices_token[-3]) * 100 - 100
                price_change_in_4min = (prices_token[-1] / prices_token[-4]) * 100 - 100
                price_change_percent_24h = 100 - ((data_token_price[0][0] / data_token_price[0][-40]) * 100)
                volume_per_10h = sum([int(i * data_token_price[0][-1]) for i in data_token_price[1][1140:-5]]) / len(data_token_price[1][1140:-5])
                # if price_change_percent_24h > 100:
                #     price_change_percent_24h = round(price_change_percent_24h - 100, 2)
                # elif price_change_percent_24h < 100:
                #     price_change_percent_24h = round(100 - price_change_percent_24h, 2)
                # else:
                #     price_change_percent_24h = 0
                #print(i)
                #and sum(volumes_token[:-5]) / len(volumes_token[:-5]) * 9.5 < volumes_token[-2] \

                if (price_change_in_3min > 3 or price_change_in_2min > 3)\
                        and prices_token[-3:] == sorted(prices_token[-3:]) and i not in keks:

                    if i in trading_pairs_fut:
                        fut_yes = "Фьючерсная"
                    else:
                        fut_yes = "НЕ Фьючерсная"
                    telebot.TeleBot(telega_token).send_message(chat_id, f"ОБЪЕМЫ МЕНЬШЕ 3200 - {i}\n"
                                                                        f"Цены {prices_token[-8:]}\n"
                                                                        f"Объемы {int(volume_per_10h)}\n"
                                                                        f"Изменение цены за 5 мин {round(price_change_in_5min, 2)}%  {round(price_change_in_5min-price_change_in_4min, 2)}%\n"
                                                                        f"Изменение цены за 4 мин {round(price_change_in_4min, 2)}%  {round(price_change_in_4min-price_change_in_3min, 2)}%\n"
                                                                        f"Изменение цены за 3 мин {round(price_change_in_3min, 2)}%  {round(price_change_in_3min-price_change_in_2min, 2)}%\n"
                                                                        f"Изменение цены за 2 мин {round(price_change_in_2min, 2)}%\n"
                                                                        f"Изменение цены за 10ч  {round(price_change_percent_24h, 2)}%\n"
                                                                        f"{fut_yes}")
                    keks.append(i)

                if (price_change_in_2min > 2.4 and price_change_in_3min-price_change_in_2min > 0.49 and price_change_in_4min-price_change_in_3min > 0.2)\
                        or (price_change_in_2min > 0.90 and price_change_in_3min-price_change_in_2min > 2.6 and price_change_in_4min-price_change_in_3min > 0.2)\
                        and prices_token[-3:] == sorted(prices_token[-3:]) \
                        and 8 > price_change_percent_24h > -8\
                        and volume_per_10h > 500:

                    buy_qty = round(11 / prices_token[-1], 1)
                    if i in trading_pairs_fut:
                        fut_yes = "Фьючерсная"
                    else:
                        fut_yes = "НЕ Фьючерсная"
                    telebot.TeleBot(telega_token).send_message(chat_id, f"RABOTAEM - {i}\n"
                                                                        f"Количество покупаемого - {buy_qty}, Цена - {prices_token[-1]}\n"
                                                                        f"Цены {prices_token[-8:]}\n"
                                                                        f"Объемы {int(volume_per_10h)}\n"
                                                                        f"Изменение цены за 5 мин {round(price_change_in_5min, 2)}%  {round(price_change_in_5min-price_change_in_4min, 2)}%\n"
                                                                        f"Изменение цены за 4 мин {round(price_change_in_4min, 2)}%  {round(price_change_in_4min-price_change_in_3min, 2)}%\n"
                                                                        f"Изменение цены за 3 мин {round(price_change_in_3min, 2)}%  {round(price_change_in_3min-price_change_in_2min, 2)}%\n"
                                                                        f"Изменение цены за 2 мин {round(price_change_in_2min, 2)}%\n"
                                                                        f"Изменение цены за 10ч  {round(price_change_percent_24h, 2)}%\n"
                                                                        f"{fut_yes}")

                    ex.append(i)

                    try:
                        order_buy = client.create_order(symbol=i, side='BUY', type='MARKET', quantity=buy_qty)
                    except BinanceAPIException as e:
                        if e.message == "Filter failure: LOT_SIZE":
                            buy_qty = int(round(11 / prices_token[-1], 1))
                            order_buy = client.create_order(symbol=i, side='BUY', type='MARKET', quantity=buy_qty)
                        else:
                            telebot.TeleBot(telega_token).send_message(chat_id, f"BUY ERROR: {e.message}\n"
                                                                               f"Количество покупаемого - {buy_qty}, Цена - {prices_token[-1]}")
                            time.sleep(30)
                            break

                    try:
                        buyprice = float(order_buy["fills"][0]["price"])
                        open_position = True

                    except Exception as e:
                        telebot.TeleBot(telega_token).send_message(chat_id, f"ERROR: {e}\n")
                        time.sleep(30)
                        break

                    #start_time = time.time()


                    while open_position:
                        #last_time = time.time()
                        all_orders = pd.DataFrame(client.get_all_orders(symbol=i),
                                                  columns=["orderId", "type", "side", "price", "status"])
                        balance = client.get_asset_balance(asset=i[:-4])
                        sell_qty = float(balance["free"])
                        #sell_qty = Decimal(sell_qty).quantize(Decimal(okr), ROUND_FLOOR)

                        if sell_qty > 0.05 and len(all_orders[all_orders.isin(["NEW"]).any(axis=1)]) == 0:
                            try:
                                order_sell = client.order_limit_sell(symbol=i, quantity=sell_qty, price=Decimal(str(round((buyprice / 100) * 101, max([len(str(i).split(".")[1]) for i in data_token_price[0][-5:]])))))
                                time.sleep(10)
                            except Exception as e:
                                telebot.TeleBot(telega_token).send_message(chat_id, f"SELL ERROR: {e}\n"
                                                                                       f"Количество продаваемого - {sell_qty}, Цена - {round((buyprice / 100) * 101, len(str(prices_token[-1]).split('.')[1]))}\n"
                                                                                       f"Монеты в кошельке - {float(sell_qty)}, Количество открытых ордеров - {len(all_orders[all_orders.isin(['NEW']).any(axis=1)])}")
                                time.sleep(30)
                        sell_qty = float(balance["free"])

                        if float(sell_qty) < 0.05 and len(all_orders[all_orders.isin(["NEW"]).any(axis=1)]) == 0:
                            open_position = False

                            bot = telebot.TeleBot(telega_token)
                            message = f"СДЕЛКА ЗАВЕРШЕНА - {i}\n" \
                                      f"{prices_token[-3:]}\n" \
                                      f"ЗАСЕК НА РОСТЕ ЦЕНЫ В {round(price_change_in_5min, 2)}%\n"\
                                      f"\n" \
                                      f"https://www.binance.com/ru/trade/{i[:-4]}_USDT?_from=markets&theme=dark&type=grid"
                            bot.send_message(chat_id, message)

                        # if int(last_time-start_time) > 3300:
                        #     data_token_price = last_data(i, "1m", "1440")
                        #     prices_token = data_token_price[0][300:]
                        #     orders = client.get_all_orders(symbol=i, limit=2)[0]
                        #     price = round(float(orders['cummulativeQuoteQty']) / float(orders["origQty"]), 7)
                        #     if 100*((price / prices_token[-1])-1) > 4:
                        #         time.sleep(20000)
                        #     else:
                        #         orders = client.get_open_orders(symbol=i)
                        #         for order in orders:
                        #             ordId = order["orderId"]
                        #             client.cancel_order(symbol=i, orderId=ordId)
                        #
                        #         try:
                        #             balance = client.get_asset_balance(asset=i[:-4])
                        #             sell_qty = float(balance["free"])
                        #             order_sell = client.order_market_sell(symbol=i, quantity=sell_qty)
                        #             orders = client.get_all_orders(symbol=i, limit=1)
                        #             price = round(float(orders[0]['cummulativeQuoteQty']) / float(orders[0]["origQty"]), 7)
                        #             telebot.TeleBot(telega_token).send_message(chat_id,
                        #                                                        f"Продажа в минус за {price}\n"
                        #                                                        f"Покупал за {buyprice}\n"
                        #                                                        f"Разница {round(100 - 100*(buyprice/price)), 2}%")
                        #             open_position = False
                        #         except Exception as e:
                        #             telebot.TeleBot(telega_token).send_message(chat_id,
                        #                                                        f"Ошибка продажи в минус, Нужен хелп!\n"
                        #                                                        f"{e}")
                        #             time.sleep(30)
                        #             break

                        time.sleep(10)
                    sql_req(i)
            except:
                pass


def last_data(symbol, interval, lookback):
    frame = pd.DataFrame(client.get_historical_klines(symbol, interval, lookback + 'min ago UTC'))
    frame = frame.iloc[:, :6]
    frame.columns = ['Time', 'Open', 'High', 'Low', 'Close', 'Volume']
    frame = frame.set_index('Time')
    frame.index = pd.to_datetime(frame.index, unit='ms')
    frame = frame.astype(float)
    # frame.to_csv('file1.csv')
    # print(frame["Volume"].sum())
    return [i.High for i in frame.itertuples()], [i.Volume for i in frame.itertuples()], [i.Close for i in frame.itertuples()]



def btc_anal(data):
    if round(data[0][-1] / (sum(data[0][:-1]) / len(data[0][:-1])) - 1, 3) > 0.5:
        bot = telebot.TeleBot(telega_token)
        message = f"БИТОК РАСТЕТ НА {round((sum(data[0][:-1]) / len(data[0][:-1])) / data[0][-1] - 1, 3)}%"
        bot.send_message(chat_id, message)
        return True
    elif round(data[0][-1] / (sum(data[0][:-1]) / len(data[0][:-1])) - 1, 3) < -0.5:
        bot = telebot.TeleBot(telega_token)
        message = f"БИТОК ПАДАЕТ НА {abs(round((sum(data[0][:-1]) / len(data[0][:-1])) / data[0][-1] - 1, 3))}%"
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
    #btc_differ = btc_anal(last_data('BTCUSDT', "15m", "300"))

    top_coin()