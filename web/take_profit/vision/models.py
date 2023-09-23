from django.db import models

# Create your models here.
class Orders(models.Model):
    time = models.CharField(max_length=30)
    update_time = models.CharField(max_length=30)
    name_cript = models.CharField(verbose_name="Название крипты", max_length=15)
    side = models.CharField(verbose_name="Сторона", max_length=15)
    price = models.CharField(verbose_name="Цена за шт.", max_length=20)
    count = models.CharField(verbose_name="Количество монет", max_length=20)
    all_cost = models.CharField(verbose_name="Общая стоимость", max_length=20)
    link_cript = models.CharField(verbose_name="Ссылка на валюту", max_length=100)



    class Meta:
        ordering = ('id',)
        verbose_name_plural = 'Данные ордеров'


    def __str__(self):
        return self.name_cript