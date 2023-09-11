import time
import pymysql
from binance.client import Client
import telebot
import keys

telega_token = "5926919919:AAFCHFocMt_pdnlAgDo-13wLe4h_tHO0-GE"

client = Client(keys.api_key, keys.api_secret)
#i = "SNXUSDT"

def sql_req(i):
    try:
        orders = client.get_all_orders(symbol=i, limit=2)
        for b in orders:
            times = time.localtime(int((str(b["time"]))[:-3]))
            formatted_time = time.strftime("%Y-%m-%d %H:%M:%S", times)
            name_cript = b["symbol"][:-4]
            if b["side"] == "SELL":
                side = "Продать"
            elif b["side"] == "BUY":
                side = "Купить"
            price = float(b['cummulativeQuoteQty']) / float(b["origQty"])
            count = float(b["origQty"])
            all_cost = float(b['cummulativeQuoteQty'])
            link_cript = f"https://www.binance.com/ru/trade/{i[:-4]}_USDT?_from=markets&theme=dark&type=grid"

            values = (formatted_time, name_cript, side, price, count, all_cost, link_cript)

            try:
                connection = pymysql.connect(host='127.0.0.1', port=3306, user='banan_user', password='warlight123',
                                             database='banan',
                                             cursorclass=pymysql.cursors.DictCursor)
                try:
                    with connection.cursor() as cursor:
                        insert_query = "INSERT INTO `vision_orders` (time, name_cript, side, price, count, all_cost, link_cript) VALUES (%s, %s, %s, %s, %s, %s, %s)"
                        cursor.execute(insert_query, (values))
                        connection.commit()
                finally:
                    connection.close()

            except Exception as e:
                telebot.TeleBot(telega_token).send_message(-695765690, f"SQL OSHIBKA: {e}\n")

    except Exception as e:
        telebot.TeleBot(telega_token).send_message(-695765690, f"SQL OSHIBKA: {e}\n")

