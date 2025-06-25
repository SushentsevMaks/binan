import time
from decimal import Decimal
from datetime import datetime
from binance.client import Client
from binance.exceptions import BinanceAPIException
import keys
import pandas as pd
import telebot
from sql_request import sql_req_str2, get_crypto
from threading import Thread
from typing import NamedTuple
from tradingview_ta import TA_Handler, Interval, Exchange
client = Client(keys.api_key, keys.api_secret)
chat_id = -695765690

telega_token = "5926919919:AAFCHFocMt_pdnlAgDo-13wLe4h_tHO0-GE"

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


def osnova():
    try:
        time_frames = [0, 4, 8, 12, 16, 20]

        if time.localtime(time.time()).tm_min == 59 and time.localtime(time.time()).tm_hour in time_frames:

            bd_cript = get_crypto("`vision_equals`")
            '''Проверка на наилучший объект и работа с ним дальше'''
            reit_bd_cript = []

            for j in bd_cript:
                reit_bd_cript.append \
                    ([j['name_cript'], j["res"], j["price_change_percent_24h"], j["awerage_high_frame"], j["high_close_change"], j["res_k_low"]])

            """Алгоритм сортировки по рейтингу (падение за таймфрейм(4 часа) и изменение цены за сутки)"""

            reit_awerage_high_frame = [i[0] for i in sorted(reit_bd_cript, key=lambda x: -x[5])]

            """Определяем топ крипту и оставшийся массив для доп закупа"""

            top = reit_awerage_high_frame[0]
            all_work_crypt = sorted(reit_bd_cript, key=lambda x: -x[5])


            ''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
            '''''''''''''''''''''''''''Основная логика'''''''''''''''''''''''''''''''''''''''''''''''''''
            ''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
            start_time = time.time()

            """Алгоритм закупа"""

            data_token: Dataset = last_data(top, "4h", "17280")
            volume_per_5h: float = sum([int(i * data_token.high_price[-1]) for i in data_token.volume[-6:]]) / len(data_token.volume[-6:]) / 80
            res: float = round(data_token.close_price[-1] / data_token.open_price[-1] * 100 - 100, 2)
            price_change_percent_24h: float = round(((data_token.close_price[-1] / data_token.open_price[-6]) * 100) - 100, 2)
            sell_pr = sorted(reit_bd_cript, key=lambda x: -x[5])[0][4]

            telebot.TeleBot(telega_token).send_message(chat_id, f"ВЫБОР ПАЛ НА {top} 4ч\n"
                                                                f"sell_pr = {sell_pr}\n"
                                                                f"Список крипт из базы по рейтингу - {sorted(reit_bd_cript, key=lambda x: -x[5])}\n"
                                                                f"------------------------\n"
                                                                f"РЕЙТИНГ - {reit_awerage_high_frame}\n"
                                                                f"------------------------\n"
                                                                f"Количество триггеров - {len(bd_cript)}\n")

            buy_qty = round(20 / data_token.close_price[-1], 1)

            try:
                order_buy = client.create_order(symbol=top, side='BUY', type='MARKET',
                                                quantity=buy_qty)
            except BinanceAPIException as e:
                if e.message == "Filter failure: LOT_SIZE":
                    buy_qty = int(round(20 / data_token.close_price[-1], 1))
                    try:
                        order_buy = client.create_order(symbol=top, side='BUY', type='MARKET',
                                                        quantity=buy_qty)
                    except:
                        telebot.TeleBot(telega_token).send_message(chat_id, f"BUY ERROR: {e.message}\n"
                                                                            f"{top}\n"
                                                                            f"Количество покупаемого - {buy_qty}, Цена - {data_token.high_price[-1]}")
                        time.sleep(1)

                else:
                    telebot.TeleBot(telega_token).send_message(chat_id, f"BUY ERROR: {e.message}\n"
                                                                        f"{top}\n"
                                                                        f"Количество покупаемого - {buy_qty}, Цена - {data_token.high_price[-1]}")
                    time.sleep(1)



            try:
                buyprice = float(order_buy["fills"][0]["price"])
                open_position = True

            except Exception as e:
                telebot.TeleBot(telega_token).send_message(chat_id, f"ERROR: {e}\n")
                time.sleep(1)

            time.sleep(5)

            """Алгоритм продажи"""
            while open_position:
                try:
                    last_time = time.time()
                    all_orders = pd.DataFrame(client.get_all_orders(symbol=top), columns=["orderId", "type", "side", "price", "status"])
                    balance = client.get_asset_balance(asset=top[:-4])
                    sell_qty = float(balance["free"])

                    if sell_qty > 0.05 and len(all_orders[all_orders.isin(["NEW"]).any(axis=1)]) == 0:
                        try:
                            x = Decimal(str(round((buyprice / 100) * sell_pr, max([len(f'{i:.15f}'.rstrip("0").split(".")[1]) for i in data_token[0][-5:]]))))
                            order_sell = client.order_limit_sell(symbol=top, quantity=buy_qty, price=x)

                        except BinanceAPIException as e:
                            time.sleep(2)

                            try:
                                x = round((buyprice / 100) * sell_pr, max([len(str(i).split(".")[1]) for i in data_token[0][-5:]]))
                                order_sell = client.order_limit_sell(symbol=top, quantity=buy_qty, price=x)
                            except BinanceAPIException as e:
                                time.sleep(2)

                                try:
                                    x = Decimal(str(round((buyprice / 100) * sell_pr, max([len(f'{i:.15f}'.rstrip("0").split(".")[1]) for i in data_token[0][-5:]]))))
                                    order_sell = client.order_limit_sell(symbol=top, quantity=int(buy_qty), price=x)
                                except BinanceAPIException as e:
                                    time.sleep(2)

                                    try:
                                        x = round((buyprice / 100) * sell_pr, max([len(str(i).split(".")[1]) for i in data_token[0][-5:]]))
                                        order_sell = client.order_limit_sell(symbol=top, quantity=int(buy_qty), price=x)
                                    except BinanceAPIException as e:
                                        telebot.TeleBot(telega_token).send_message(chat_id, f"ФЕЙЛ ПРОДАЖИ: {e}\n"
                                                                                            f"Количество продаваемого - {int(buy_qty)}, Цена - {x}\n"
                                                                                            f"buyprice - {buyprice}, sell_pr - {sell_pr}\n"
                                                                                            f"f{[str(i).split('.')[1] for i in data_token[0][-5:]]}\n"
                                                                                            f"Монеты в кошельке - {float(sell_qty)}, Количество открытых ордеров - {len(all_orders[all_orders.isin(['NEW']).any(axis=1)])}")
                                        time.sleep(600)

                    elif float(sell_qty) < 0.05 and len(all_orders[all_orders.isin(["NEW"]).any(axis=1)]) == 0:
                        open_position = False
                        bot = telebot.TeleBot(telega_token)
                        message = f"СДЕЛКА ЗАВЕРШЕНА - {top}\n" \
                                  f"\n" \
                                  f"ПРИБЫЛЬ СО СДЕЛКИ: +{round(sell_pr-100, 2)}%\n" \
                                  f"\n" \
                                  f"https://www.binance.com/ru/trade/{top[:-4]}_USDT?_from=markets&theme=dark&type=grid"
                        bot.send_message(chat_id, message)

                    if last_time - start_time > 53400:

                        orders = client.get_open_orders(symbol=top)
                        for order in orders:
                            ordId = order["orderId"]
                            client.cancel_order(symbol=top, orderId=ordId)

                        time.sleep(1)
                        try:
                            balance = client.get_asset_balance(asset=top[:-4])
                            sell_qty = float(balance["free"])
                            order_sell = client.order_market_sell(symbol=top, quantity=sell_qty)
                            orders = client.get_all_orders(symbol=top, limit=1)
                            try:
                                price = round(float(orders[0]['cummulativeQuoteQty']) / float(orders[0]["origQty"]), 7)
                                telebot.TeleBot(telega_token).send_photo(chat_id, 'https://github.com/SushentsevMaks/hhru-analize/blob/main/patrik_35715679_orig_.jpg?raw=true', caption=
                                f"ВРЕМЯ ИСТЕКЛО - {top}\n"
                                f"Продажа по времени {price}\n"
                                f"Покупал за {buyprice}\n"
                                f"Разница {round(100 - 100 * (buyprice / price), 2)}%")
                                open_position = False
                            except:
                                try:
                                    time.sleep(5)
                                    price = round(float(orders[0]['cummulativeQuoteQty']) / float(orders[0]["origQty"]), 7)
                                    telebot.TeleBot(telega_token).send_photo(chat_id,
                                                                             'https://github.com/bibar228/hhru-analize/blob/main/patrik_35715679_orig_.jpg?raw=true',
                                                                             caption=
                                                                             f"ВРЕМЯ ИСТЕКЛО - {top}\n"
                                                                             f"Продажа по времени {price}\n"
                                                                             f"Покупал за {buyprice}\n"
                                                                             f"Разница {round(100 - 100 * (buyprice / price), 2)}%")
                                    open_position = False

                                except Exception as e:
                                    telebot.TeleBot(telega_token).send_message(chat_id ,f"Ошибка продажи в минус, Нужен хелп!\n"
                                                                                       f"{e}\n"
                                                                                       f"sell_qty {sell_qty}\n"
                                                                                       f"balance {balance}\n"
                                                                                       f'price {float(orders[0]["cummulativeQuoteQty"])} {float(orders[0]["origQty"])}')
                                    time.sleep(5)
                        except Exception as e:
                            telebot.TeleBot(telega_token).send_message(chat_id,
                                                                       f"Ошибыч продажи в минус\n"
                                                                       f"{e}")
                            time.sleep(5)

                    if buyprice * 0.95 > data_token.close_price[-1]:
                        orders = client.get_open_orders(symbol=top)
                        for order in orders:
                            ordId = order["orderId"]
                            client.cancel_order(symbol=top, orderId=ordId)

                        try:
                            balance = client.get_asset_balance(asset=top[:-4])
                            sell_qty = float(balance["free"])
                            order_sell = client.order_market_sell(symbol=top,
                                                                  quantity=sell_qty)
                            orders = client.get_all_orders(symbol=top, limit=1)
                            price = round(
                                float(orders[0]['cummulativeQuoteQty']) / float(orders[0]["origQty"]), 7)
                            telebot.TeleBot(telega_token).send_photo(chat_id,
                                                                     'https://github.com/SushentsevMaks/hhru-analize/blob/main/patrik_35715679_orig_.jpg?raw=true',
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

                    data_token: Dataset = last_data(top, "15m", "1440")
                    time.sleep(4)

                except Exception as e:
                    telebot.TeleBot(telega_token).send_message(chat_id, f"ERROR: {e}\n")
                    time.sleep(5)

            max_price = max(data_token[0])

            time.sleep(1)
            try:
                sql_req_str2("`vision_orders_str2`", top, price_change_percent_24h, volume_per_5h, max_price, 1, res)
            except:
                time.sleep(5)
                sql_req_str2("`vision_orders_str2`", top, price_change_percent_24h, volume_per_5h, max_price, 1, res)

            new_alg_crypto_work_end = []
            """Заглушка до 25 минут, если первая продажа была быстрее"""
            while last_time - start_time < 1200:
                last_time = time.time()
                time.sleep(1)


            """АЛГОРИТМ ДОП ЗАКУПА ПОСЛЕ ОСНОВНОГО"""
            if len(all_work_crypt) > 1:

                telebot.TeleBot(telega_token).send_message(chat_id,f"Заглушку прошел, включаю доп алг")

                while last_time - start_time < 12000:


                    for i in all_work_crypt[1:round(len(all_work_crypt))]:

                        sell_pr = i[4]
                        last_time = time.time()
                        data_token: Dataset = last_data(i[0], "4h", "1440")
                        volume_per_5h: float = sum([int(i * data_token.high_price[-1]) for i in data_token.volume[:-1]]) / len \
                            (data_token.volume[:-1]) / 80
                        res_now: float = round(data_token.close_price[-1] / data_token.open_price[-1] * 100 - 100, 2)
                        res_past: float = round(data_token.high_price[-1] / data_token.close_price[-2] * 100 - 100, 2)
                        price_change_percent_24h: float = round \
                            (((data_token.close_price[-1] / data_token.open_price[0]) * 100) - 100, 2)
                        '''процент падения за последние 2ч. Отрицательные значение == был рост'''
                        loss_price_for_two_hours: float = round \
                            (100 - data_token.close_price[-2] / max([i for i in data_token.open_price[-9:]]) * 100, 2)

                        """Какая сейчас цена относительно максимального падения (Чем больше тем лучше)"""
                        low = round(data_token.close_price[-1] / data_token.low_price[-1] * 100 - 100, 2)
                        now = round(data_token.close_price[-1] / data_token.open_price[-1] * 100 - 100, 2)
                        now_k_low = abs(round(now / low, 2))

                        """ЗАКУПАЕМ С УСЛОВИЯМИ"""
                        if res_now < 0 and res_past < 0.6 and now_k_low > 1.5 and last_time - start_time < 12000 and i not in new_alg_crypto_work_end:
                            start_time_dop_alg = time.time()

                            buy_qty = round(20 / data_token.close_price[-1], 1)
                            telebot.TeleBot(telega_token).send_message(chat_id, f"!!!!!!!!!!!!!ДОП АЛГОРИТМ!!!!!!!!!!!!!\n"
                                                                                f"now_k_low = {now_k_low}\n"
                                                                                f"РАБОТАЕМ С {i[0]}\n"
                                                                                f"Изменение цены сейчас относительно начала фрейма: {res_now}%\n"
                                                                                f"Максимальный рост цены в этот фрейм: {res_past}%\n")
                            new_alg_crypto_work_end.append(i[0])

                            try:
                                order_buy = client.create_order(symbol=i[0], side='BUY', type='MARKET', quantity=buy_qty)
                            except BinanceAPIException as e:
                                if e.message == "Filter failure: LOT_SIZE":
                                    buy_qty = int(round(20 / data_token.close_price[-1], 1))
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

                            time.sleep(5)

                            """Алгоритм продажи"""
                            while open_position:
                                try:
                                    last_time_dop_alg = time.time()
                                    all_orders = pd.DataFrame(client.get_all_orders(symbol=i[0]), columns=["orderId", "type", "side", "price", "status"])
                                    balance = client.get_asset_balance(asset=i[0][:-4])
                                    sell_qty = float(balance["free"])

                                    if sell_qty > 0.05 and len(all_orders[all_orders.isin(["NEW"]).any(axis=1)]) == 0:
                                        try:
                                            y = Decimal(str(round((buyprice / 100) * sell_pr, max([len(f'{i:.15f}'.rstrip("0").split(".")[1]) for i in data_token[0][-5:]]))))
                                            order_sell = client.order_limit_sell(symbol=i[0],
                                                                                 quantity=buy_qty,
                                                                                 price=y)

                                        except BinanceAPIException as e:
                                            time.sleep(2)

                                            try:
                                                y = round((buyprice / 100) * sell_pr, max([len(str(i).split(".")[1]) for i in data_token[0][-5:]]))
                                                order_sell = client.order_limit_sell(symbol=i[0],
                                                                                     quantity=buy_qty,
                                                                                     price=y)
                                            except BinanceAPIException as e:
                                                time.sleep(2)

                                                try:
                                                    y = Decimal(str(round((buyprice / 100) * sell_pr, max([len(f'{i:.15f}'.rstrip("0").split(".")[1]) for i in data_token[0][-5:]]))))
                                                    order_sell = client.order_limit_sell(symbol=i[0],
                                                                                         quantity=int(buy_qty),
                                                                                         price=y)
                                                except BinanceAPIException as e:
                                                    time.sleep(2)

                                                    try:
                                                        y = round((buyprice / 100) * sell_pr, max([len(str(i).split(".")[1]) for i in data_token[0][-5:]]))
                                                        order_sell = client.order_limit_sell(symbol=i[0], quantity=int(buy_qty), price=y)

                                                    except BinanceAPIException as e:
                                                        telebot.TeleBot(telega_token).send_message(chat_id,
                                                                                                   f"ФЕЙЛ ПРОДАЖИ: {e}\n"
                                                                                                   f"buyprice - {buyprice}, sell_pr - {sell_pr}\n"
                                                                                                   f"Количество продаваемого - {int(buy_qty)}, Цена - {y}\n"
                                                                                                   f"Монеты в кошельке - {float(sell_qty)}, Количество открытых ордеров - {len(all_orders[all_orders.isin(['NEW']).any(axis=1)])}")
                                                        time.sleep(600)

                                    elif float(sell_qty) < 0.05 and len(all_orders[all_orders.isin(["NEW"]).any(axis=1)]) == 0:
                                        open_position = False
                                        bot = telebot.TeleBot(telega_token)
                                        message = f"СДЕЛКА ЗАВЕРШЕНА - {i[0]}\n" \
                                                  f"\n" \
                                                  f"ПРИБЫЛЬ СО СДЕЛКИ: +{round(sell_pr - 100, 2)}%\n" \
                                                  f"\n" \
                                                  f"https://www.binance.com/ru/trade/{i[0][:-4]}_USDT?_from=markets&theme=dark&type=grid"
                                        bot.send_message(chat_id, message)

                                    if last_time_dop_alg - start_time_dop_alg > 42300:
                                        telebot.TeleBot(telega_token).send_message(chat_id,
                                                                                   f"ВРЕМЯ ИСТЕКЛО {i[0]} {buyprice} {data_token.close_price[-1]}")

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
                                                                                     'https://github.com/SushentsevMaks/hhru-analize/blob/main/patrik_35715679_orig_.jpg?raw=true',
                                                                                     caption=f"Продажа по времени {price}\n"
                                                                                             f"Покупал за {buyprice}\n"
                                                                                             f"Разница {round(100 - 100 * (buyprice / price), 2)}%")
                                            open_position = False

                                        except Exception as e:
                                            telebot.TeleBot(telega_token).send_message(chat_id,
                                                                                       f"Ошибка продажи в минус, Нужен хелп!\n"
                                                                                       f"{e}")
                                            time.sleep(500)

                                    if buyprice * 0.95 > data_token.close_price[-1]:
                                        orders = client.get_open_orders(symbol=top)
                                        for order in orders:
                                            ordId = order["orderId"]
                                            client.cancel_order(symbol=top, orderId=ordId)

                                        try:
                                            balance = client.get_asset_balance(asset=top[:-4])
                                            sell_qty = float(balance["free"])
                                            order_sell = client.order_market_sell(symbol=top,
                                                                                  quantity=sell_qty)
                                            orders = client.get_all_orders(symbol=top, limit=1)
                                            price = round(
                                                float(orders[0]['cummulativeQuoteQty']) / float(orders[0]["origQty"]), 7)
                                            telebot.TeleBot(telega_token).send_photo(chat_id,
                                                                                     'https://github.com/SushentsevMaks/hhru-analize/blob/main/patrik_35715679_orig_.jpg?raw=true',
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

                                    data_token: Dataset = last_data(i[0], "15m", "1440")
                                    time.sleep(4)

                                except Exception as e:
                                    telebot.TeleBot(telega_token).send_message(chat_id, f"ERROR: {e}\n")
                                    time.sleep(5)

                            max_price = max(data_token[0])

                            time.sleep(1)
                            try:
                                sql_req_str2("`vision_orders_str2`", i[0], price_change_percent_24h, volume_per_5h, max_price, loss_price_for_two_hours, res_now)
                            except:
                                time.sleep(5)
                                sql_req_str2("`vision_orders_str2`", i[0], price_change_percent_24h, volume_per_5h, max_price, loss_price_for_two_hours, res_now)

                            time.sleep(1)

                    time.sleep(1200)


            telebot.TeleBot(telega_token).send_message(chat_id ,f"Доп. алг закончился, готов к новому циклу")

            time.sleep(60)

    except Exception as e:
        telebot.TeleBot(telega_token).send_message(chat_id,
                                                   f"НЕТ КРИПТ\n"
                                                        f"Часы {time.localtime(time.time()).tm_hour}\n"
                                                        f"минуты{time.localtime(time.time()).tm_min}\n"
                                                        f"{e}")



while True:
    try:
        start_time_check = time.time()

        while time.localtime(start_time_check).tm_min != 59 or time.localtime(start_time_check).tm_sec < 57:
            start_time_check = time.time()
            time.sleep(1)


        osnova()

        time.sleep(60)
    except Exception as e:
        telebot.TeleBot(telega_token).send_message(chat_id,
                                                   f"Ошибка общего скрипта 4ч основа\n"
                                                   f"{e}")
