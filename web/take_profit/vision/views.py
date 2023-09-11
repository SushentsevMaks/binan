from django.shortcuts import render
from rest_framework import viewsets


from rest_framework import viewsets, permissions

from vision.models import Orders
from vision.serializers import OrdersSerializer


# Create your views here.
class OrdersViewSet(viewsets.ModelViewSet):
    queryset = Orders.objects.filter(side="Купить")[::-1]
    d = 0
    for i in queryset:
        d += float(i.price)
    permission_classes = [
        permissions.AllowAny
    ]
    serializer_class = OrdersSerializer



def index(request):
    orders = Orders.objects.all()[::-1]
    buys = Orders.objects.filter(side="Купить")[::-1]
    sells = Orders.objects.filter(side="Продать")[::-1]
    d = 0
    for i in range(len(sells)):
        d += float(sells[i].all_cost) - float(buys[i].all_cost)
    return render(request, "vision/index.html", {"orders": orders, "buys": round(d, 2)})