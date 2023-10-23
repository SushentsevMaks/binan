from django.db import models

# Create your models here.
class Orders(models.Model):
    time = models.CharField(max_length=30)
    update_time = models.CharField(max_length=30)
    name_cript = models.CharField(verbose_name="Название крипты", max_length=15)
    price_buy = models.FloatField(verbose_name="Цена за шт.")
    price_sell = models.FloatField(verbose_name="Цена за штnn.")
    count = models.CharField(verbose_name="Количество монет", max_length=20)
    all_volume = models.DecimalField(verbose_name="Общая стоимость", max_digits=7, decimal_places=2)
    percent_profit = models.DecimalField(max_digits=5, decimal_places=2)
    volume_profit = models.DecimalField(max_digits=5, decimal_places=2)
    link_cript = models.CharField(verbose_name="Ссылка на валюту", max_length=100)
    price_in_5min = models.FloatField(verbose_name="Цена за 5 мин")
    price_in_4min = models.FloatField(verbose_name="Цена за 4 мин")
    price_in_3min = models.FloatField(verbose_name="Цена за 3 мин")
    price_in_2min = models.FloatField(verbose_name="Цена за 2 мин")
    price_change_percent_24h = models.FloatField(verbose_name="Изменение цены за последние 24 ч.")
    volume_per_5h = models.DecimalField(max_digits=10, decimal_places=0, verbose_name="Объемы за последние 5 часов")


    class Meta:
        ordering = ('id',)
        verbose_name_plural = 'Данные ордеров'

    def __str__(self):
        return self.name_cript