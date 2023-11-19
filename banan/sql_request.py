import time
import pymysql
from binance.client import Client
import telebot
import keys

telega_token = "5926919919:AAFCHFocMt_pdnlAgDo-13wLe4h_tHO0-GE"

client = Client(keys.api_key, keys.api_secret)

# def sql_req(i: str, price_change_percent_24h: float, price_in_2min: float, price_in_3min: float, price_in_4min: float,
#             price_in_5min: float, volume_per_5h: float, price_change_percent_min_24h: float, price_change_percent_max_24h: float,
#             max_price: float, volatility: float, res: float):
#     try:
#         orders = client.get_all_orders(symbol=i, limit=5)
#         orders = [i for i in orders if i["status"] == "FILLED"][-2:]
#
#         times = time.localtime(int((str(orders[0]["time"]))[:-3]))
#         formatted_time = time.strftime("%Y-%m-%d %H:%M:%S", times)
#
#         times_update = time.localtime(int((str(orders[1]["updateTime"]))[:-3]))
#         formatted_time_update = time.strftime("%Y-%m-%d %H:%M:%S", times_update)
#
#         if times_update.tm_mday > times.tm_mday:
#             duration_order = (times_update.tm_hour + 24 - times.tm_hour)*60*60 + (times_update.tm_min - times.tm_min)*60 + (times_update.tm_sec - times.tm_sec)
#         else:
#             duration_order = (times_update.tm_hour - times.tm_hour) * 60 * 60 + (times_update.tm_min - times.tm_min) * 60 + (times_update.tm_sec - times.tm_sec)
#
#         name_cript = orders[0]["symbol"][:-4]
#         price_buy = round(float(orders[0]['cummulativeQuoteQty']) / float(orders[0]["origQty"]), 7)
#         price_sell = round(float(orders[1]['cummulativeQuoteQty']) / float(orders[1]["origQty"]), 7)
#         count = float(orders[0]["origQty"])
#         all_volume = float(orders[0]['cummulativeQuoteQty']) + float(orders[1]['cummulativeQuoteQty'])
#         percent_profit = round(100 - (float(orders[0]['cummulativeQuoteQty']) / (float(orders[1]['cummulativeQuoteQty'])-(float(all_volume)*0.075)/100)) * 100, 3)
#         volume_profit = round(float(orders[1]['cummulativeQuoteQty']) - float(orders[0]['cummulativeQuoteQty']) - (float(all_volume)*0.075)/100, 3)
#         link_cript = f"https://www.binance.com/ru/trade/{i[:-4]}_USDT?_from=markets&theme=dark&type=grid"
#         if volume_profit > 0:
#             max_profit = round(((max_price / price_sell) * 100) - 100, 2) # % от цены продажи (упущенная выгода)
#         else:
#             max_profit = -round(((max_price / price_buy) * 100) - 100, 2)
#
#         values = (formatted_time, formatted_time_update, duration_order, name_cript, price_buy, price_sell, count, all_volume, percent_profit,
#                   volume_profit, link_cript, price_change_percent_24h, price_in_2min, price_in_3min, price_in_4min, price_in_5min,
#                   volume_per_5h, price_change_percent_min_24h, price_change_percent_max_24h, max_profit, volatility)
#
#         try:
#             connection = pymysql.connect(host='127.0.0.1', port=3306, user='banan_user', password='warlight123',
#                                              database='banans',
#                                              cursorclass=pymysql.cursors.DictCursor)
#             try:
#                 with connection.cursor() as cursor:
#                     insert_query = "INSERT INTO `vision_orders` (time, update_time, duration_order, name_cript, price_buy, price_sell, count, all_volume, percent_profit, " \
#                                    "volume_profit, link_cript, price_change_percent_24h, price_in_2min, price_in_3min, price_in_4min, price_in_5min, volume_per_5h, " \
#                                    "price_change_percent_min_24h, price_change_percent_max_24h, max_profit, volatility) " \
#                                    "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
#                     cursor.execute(insert_query, (values))
#                     connection.commit()
#             finally:
#                 connection.close()
#
#         except Exception as e:
#             telebot.TeleBot(telega_token).send_message(-695765690, f"SQL ERROR: {e}\n")
#
#     except Exception as e:
#         telebot.TeleBot(telega_token).send_message(-695765690, f"SQL ERROR: {e}\n")


#sql_req("LUNCUSDT", 7.21, 1.87, 2.65, 0.92, -0.05, 16078)

def sql_req_str2(i: str, price_change_percent_24h: float, volume_per_5h: float,
            max_price: float, loss_price_for_two_hours: float, res: float):
    try:
        orders = client.get_all_orders(symbol=i, limit=5)
        orders = [i for i in orders if i["status"] == "FILLED"][-2:]

        times = time.localtime(int((str(orders[0]["time"]))[:-3]))
        formatted_time = time.strftime("%Y-%m-%d %H:%M:%S", times)

        times_update = time.localtime(int((str(orders[1]["updateTime"]))[:-3]))
        formatted_time_update = time.strftime("%Y-%m-%d %H:%M:%S", times_update)

        if times_update.tm_mday > times.tm_mday:
            duration_order = (times_update.tm_hour + 24 - times.tm_hour) * 60 * 60 + (times_update.tm_min - times.tm_min) * 60 + (times_update.tm_sec - times.tm_sec)
        else:
            duration_order = (times_update.tm_hour - times.tm_hour) * 60 * 60 + (times_update.tm_min - times.tm_min) * 60 + (times_update.tm_sec - times.tm_sec)

        name_cript = orders[0]["symbol"][:-4]
        price_buy = round(float(orders[0]['cummulativeQuoteQty']) / float(orders[0]["origQty"]), 7)
        price_sell = round(float(orders[1]['cummulativeQuoteQty']) / float(orders[1]["origQty"]), 7)
        count = float(orders[0]["origQty"])
        all_volume = float(orders[0]['cummulativeQuoteQty']) + float(orders[1]['cummulativeQuoteQty'])
        percent_profit = round(100 - (float(orders[0]['cummulativeQuoteQty']) / (float(orders[1]['cummulativeQuoteQty'])-(float(all_volume)*0.075)/100)) * 100, 3)
        volume_profit = round(float(orders[1]['cummulativeQuoteQty']) - float(orders[0]['cummulativeQuoteQty']) - (float(all_volume)*0.075)/100, 3)
        link_cript = f"https://www.binance.com/ru/trade/{i[:-4]}_USDT?_from=markets&theme=dark&type=grid"
        if volume_profit > 0:
            max_profit = round(((max_price / price_sell) * 100) - 100, 2) # % от цены продажи (упущенная выгода)
        else:
            max_profit = 0

        values = (formatted_time, formatted_time_update, duration_order, name_cript, price_buy, price_sell, count, all_volume, percent_profit,
                  volume_profit, link_cript, price_change_percent_24h,
                  volume_per_5h, max_profit, loss_price_for_two_hours, res)

        try:
            connection = pymysql.connect(host='127.0.0.1', port=3306, user='banan_user', password='warlight123',
                                             database='banans',
                                             cursorclass=pymysql.cursors.DictCursor)
            try:
                with connection.cursor() as cursor:
                    insert_query = "INSERT INTO `vision_orders_str2` (time, update_time, duration_order, name_cript, price_buy, price_sell, count, all_volume, percent_profit, " \
                                   "volume_profit, link_cript, price_change_percent_24h, volume_per_5h, " \
                                   "max_profit, loss_price_for_two_hours, res) " \
                                   "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
                    cursor.execute(insert_query, (values))
                    connection.commit()
            finally:
                connection.close()

        except Exception as e:
            telebot.TeleBot(telega_token).send_message(-695765690, f"SQL ERROR data fix: {e}\n"
                                                                   f"relation_high: {loss_price_for_two_hours}\n")

    except Exception as e:
        telebot.TeleBot(telega_token).send_message(-695765690, f"SQL ERROR input attempt: {e}\n"
                                                               f"relation_high: {loss_price_for_two_hours}\n")

#sql_req_str2("SUPERUSDT", 22.18, 7640, 1.54, 2.52, -3.2, 0.0)

def equal(name_cript_check: str, res: float):
    try:
        values = (name_cript_check, res)

        try:
            connection = pymysql.connect(host='127.0.0.1', port=3306, user='banan_user', password='warlight123',
                                             database='banans',
                                             cursorclass=pymysql.cursors.DictCursor)
            try:
                with connection.cursor() as cursor:
                    insert_query = "INSERT INTO `vision_equals` (name_cript, res) " \
                                   "VALUES (%s, %s)"
                    cursor.execute(insert_query, (values))
                    connection.commit()
            finally:
                connection.close()

        except Exception as e:
            telebot.TeleBot(telega_token).send_message(-695765690, f"SQL ERROR equal connect k bd: {e}\n")

    except Exception as e:
        telebot.TeleBot(telega_token).send_message(-695765690, f"SQL ERROR equal: {e}\n")

def get_top_crypto():
    try:
        connection = pymysql.connect(host='127.0.0.1', port=3306, user='banan_user', password='warlight123',
                                             database='banans',
                                             cursorclass=pymysql.cursors.DictCursor)
        try:
            with connection.cursor() as cursor:
                cursor.execute("select name_cript from `vision_equals`"
                               "ORDER BY res ASC LIMIT 1")
                result = cursor.fetchall()

        finally:
            connection.close()

        return result[0]["name_cript"]

    except Exception as e:
        telebot.TeleBot(telega_token).send_message(-695765690, f"SQL ERROR get top cripto connect: {e}\n")

def sql_del():
    try:
        connection = pymysql.connect(host='127.0.0.1', port=3306, user='banan_user', password='warlight123',
                                     database='banans',
                                     cursorclass=pymysql.cursors.DictCursor)
        try:
            with connection.cursor() as cursor:
                insert_query = "DELETE FROM `vision_equals`"
                cursor.execute(insert_query)
                connection.commit()
        finally:
            connection.close()

    except Exception as e:
        telebot.TeleBot(telega_token).send_message(-695765690, f"SQL ERROR DEL: {e}\n")

