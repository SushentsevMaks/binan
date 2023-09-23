from django.shortcuts import render
from rest_framework import viewsets


from rest_framework import viewsets, permissions

from vision.models import Orders
from vision.serializers import OrdersSerializer


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



def index(request):
    sort_orders = Orders.objects.order_by("time")[::-1]
    orders = Orders.objects.all()

    percent_change_for_day = {}

    for daytime in sorted(set([i.time[:10] for i in orders])):
        for order in orders:
            if daytime == order.time[:10]:
                day_percent_profit = round(sum([orders[i].percent_profit for i in range(0, len(orders)) if orders[i].time[:10] == daytime]), 2)
                day_volume_profit = round(sum([orders[i].volume_profit for i in range(0, len(orders)) if orders[i].time[:10] == daytime]), 2)
                ers_qnt_per_day = len([i for i in range(len(orders)) if orders[i].time[:10] == daytime])
                percent_change_for_day[daytime] = [day_percent_profit,
                                                   day_volume_profit,
                                                   ers_qnt_per_day]

    all_profit = [sum([i[0] for i in percent_change_for_day.values()]), sum([i[1] for i in percent_change_for_day.values()])]

    return render(request, "vision/index.html", {"orders": sort_orders, "percent_change_for_day": percent_change_for_day, "all_profit": all_profit})

