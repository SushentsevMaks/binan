import time
import pymysql
from binance.client import Client
import telebot
import keys

telega_token = "5926919919:AAFCHFocMt_pdnlAgDo-13wLe4h_tHO0-GE"

client = Client(keys.api_key, keys.api_secret)
i = "FRONTUSDT"

def sql_req(i):
    try:
        orders = client.get_all_orders(symbol=i, limit=5)
        orders = [i for i in orders if i["status"] == "FILLED"][-2:]
        times = time.localtime(int((str(orders[0]["time"]))[:-3]))
        formatted_time = time.strftime("%Y-%m-%d %H:%M:%S", times)
        times_update = time.localtime(int((str(orders[1]["updateTime"]))[:-3]))
        formatted_time_update = time.strftime("%Y-%m-%d %H:%M:%S", times_update)
        name_cript = orders[0]["symbol"][:-4]
        price_buy = round(float(orders[0]['cummulativeQuoteQty']) / float(orders[0]["origQty"]), 7)
        price_sell = round(float(orders[1]['cummulativeQuoteQty']) / float(orders[1]["origQty"]), 7)
        count = float(orders[0]["origQty"])
        all_volume = float(orders[0]['cummulativeQuoteQty']) + float(orders[1]['cummulativeQuoteQty'])
        percent_profit = round(100 - (float(orders[0]['cummulativeQuoteQty']) / (float(orders[1]['cummulativeQuoteQty'])-(float(all_volume)*0.075)/100)) * 100,
                       2)
        volume_profit = round(float(orders[1]['cummulativeQuoteQty']) - float(orders[0]['cummulativeQuoteQty']) - (float(all_volume)*0.075)/100, 2)
        link_cript = f"https://www.binance.com/ru/trade/{i[:-4]}_USDT?_from=markets&theme=dark&type=grid"

        values = (formatted_time, formatted_time_update, name_cript, price_buy, price_sell, count, all_volume, percent_profit, volume_profit, link_cript)

        try:
            connection = pymysql.connect(host='127.0.0.1', port=3306, user='banan_user', password='warlight123',
                                             database='banan',
                                             cursorclass=pymysql.cursors.DictCursor)
            try:
                with connection.cursor() as cursor:
                    insert_query = "INSERT INTO `vision_orders` (time, update_time, name_cript, price_buy, price_sell, count, all_volume, percent_profit, volume_profit, link_cript) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
                    cursor.execute(insert_query, (values))
                    connection.commit()
            finally:
                connection.close()

        except Exception as e:
            telebot.TeleBot(telega_token).send_message(-695765690, f"SQL OSHIBKA: {e}\n")

    except Exception as e:
        telebot.TeleBot(telega_token).send_message(-695765690, f"SQL OSHIBKA: {e}\n")

sql_req(i)