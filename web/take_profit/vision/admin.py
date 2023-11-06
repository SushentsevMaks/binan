from django.contrib import admin

from vision import Orders


# Register your models here.
class OrdersAdmin(admin.ModelAdmin):
    list_display = ["name_cript", "id"]

admin.site.register(Orders, OrdersAdmin)