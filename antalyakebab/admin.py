from django.contrib import admin
from django.utils import timezone
from .models import Category, Delivery, Dressing, Drink, Products, SideDish, Customer, Order, CartItem, DeliveryAddress, Price

class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'status', 'get_expired_order') 

    def get_expired_order(self, order):
        if order.status == 'CREATING' and (timezone.now() - order.date_ordered).days > 15:
            return 'Neprovedená objednávka'
        else:
            return ''
    get_expired_order.short_description = 'Stav'

# Register your models here.
admin.site.register(Category)
admin.site.register(Delivery)
admin.site.register(Dressing)
admin.site.register(Drink)
admin.site.register(Products)
admin.site.register(SideDish)
admin.site.register(Customer)
admin.site.register(Order, OrderAdmin)
admin.site.register(DeliveryAddress)
admin.site.register(CartItem)
admin.site.register(Price)