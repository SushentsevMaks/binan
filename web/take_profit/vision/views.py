from django.shortcuts import render

from rest_framework import viewsets

from vision.models import Orders, Orders_str2


# Create your views here.
class OrdersViewSet(viewsets.ModelViewSet):
    pass
    # queryset = Orders.objects.filter(side="Купить")[::-1]
    # d = 0
    # for i in queryset:
    #     d += float(i.price)
    # permission_classes = [
    #     permissions.AllowAny
    # ]
    # serializer_class = OrdersSerializer



def index_str1(request):
    sort_orders = Orders.objects.order_by("time")[::-1]
    orders = Orders.objects.all()

    percent_change_for_day = {}

    for daytime in sorted(set([i.time[:10] for i in orders])):
        for order in orders:
            if daytime == order.time[:10]:
                day_percent_profit = sum([orders[i].percent_profit for i in range(0, len(orders)) if orders[i].time[:10] == daytime])
                day_volume_profit = sum([orders[i].volume_profit for i in range(0, len(orders)) if orders[i].time[:10] == daytime])
                orders_qnt_per_day = len([i for i in range(len(orders)) if orders[i].time[:10] == daytime])
                percent_change_for_day[daytime] = [day_percent_profit,
                                                   day_volume_profit,
                                                   orders_qnt_per_day]

    all_profit = [sum([i[0] for i in percent_change_for_day.values()]), sum([i[1] for i in percent_change_for_day.values()])]

    return render(request, "vision/index_str1.html", {"orders": sort_orders, "percent_change_for_day": percent_change_for_day, "all_profit": all_profit})

def day_str1(request, time):

    queryset = set([i.time[:10] for i in Orders.objects.all()])
    day_percent_result = sum([i.percent_profit for i in Orders.objects.all() if i.time[:10] == time])
    day_volume_result = sum([i.volume_profit for i in Orders.objects.all() if i.time[:10] == time])
    day_qnt = len([i for i in Orders.objects.all() if i.time[:10] == time])
    days = [i for i in Orders.objects.all() if i.time[:10] == time]
    months = {"1": "Января", "2": "Февраля", "3": "Марта", "4": "Апреля", "5": "Мая", "6": "Июня",
              "7": "Июля", "8": "Августа", "9": "Сентября", "10": "Октября", "11": "Ноября", "12": "Декабря"}
    date = f"{time[-2:]} {months[time[5:7]]} {time[:4]}"

    return render(request, "vision/day_str1.html", {"day": queryset, "days": days, "date": date, "day_percent_result": day_percent_result,
                                               "day_volume_result": day_volume_result, "day_qnt": day_qnt})


def index_str2(request):
    sort_orders = Orders_str2.objects.order_by("time")[::-1]
    orders = Orders_str2.objects.all()

    percent_change_for_day = {}

    for daytime in sorted(set([i.time[:10] for i in orders])):
        for order in orders:
            if daytime == order.time[:10]:
                day_percent_profit = sum([orders[i].percent_profit for i in range(0, len(orders)) if orders[i].time[:10] == daytime])
                day_volume_profit = sum([orders[i].volume_profit for i in range(0, len(orders)) if orders[i].time[:10] == daytime])
                orders_qnt_per_day = len([i for i in range(len(orders)) if orders[i].time[:10] == daytime])
                percent_change_for_day[daytime] = [day_percent_profit,
                                                   day_volume_profit,
                                                   orders_qnt_per_day]

    all_profit = [sum([i[0] for i in percent_change_for_day.values()]), sum([i[1] for i in percent_change_for_day.values()])]

    return render(request, "vision/index_str2.html", {"orders": sort_orders, "percent_change_for_day": percent_change_for_day, "all_profit": all_profit})

def day_str2(request, time):

    queryset = set([i.time[:10] for i in Orders_str2.objects.all()])
    day_percent_result = sum([i.percent_profit for i in Orders_str2.objects.all() if i.time[:10] == time])
    day_volume_result = sum([i.volume_profit for i in Orders_str2.objects.all() if i.time[:10] == time])
    day_qnt = len([i for i in Orders_str2.objects.all() if i.time[:10] == time])
    days = [i for i in Orders_str2.objects.all() if i.time[:10] == time]
    months = {"1": "Января", "2": "Февраля", "3": "Марта", "4": "Апреля", "5": "Мая", "6": "Июня",
              "7": "Июля", "8": "Августа", "9": "Сентября", "10": "Октября", "11": "Ноября", "12": "Декабря"}
    date = f"{time[-2:]} {months[time[5:7]]} {time[:4]}"

    return render(request, "vision/day_str2.html", {"day": queryset, "days": days, "date": date, "day_percent_result": day_percent_result,
                                               "day_volume_result": day_volume_result, "day_qnt": day_qnt})

