from django.db import models

# Create your models here.
class Orders(models.Model):
    time = models.CharField(max_length=30)
    update_time = models.CharField(max_length=30)
    name_cript = models.CharField(verbose_name="Название крипты", max_length=15)
    price_buy = models.FloatField(verbose_name="Цена за шт.")
    price_sell = models.FloatField(verbose_name="Цена за штnn.")
    count = models.CharField(verbose_name="Количество монет", max_length=20)
    all_volume = models.FloatField(verbose_name="Общая стоимость")
    percent_profit = models.FloatField(verbose_name="Прибыль")
    volume_profit = models.FloatField(verbose_name="Прибыль")
    link_cript = models.CharField(verbose_name="Ссылка на валюту", max_length=100)



    class Meta:
        ordering = ('id',)
        verbose_name_plural = 'Данные ордеров'


    def __str__(self):
        return self.name_cript