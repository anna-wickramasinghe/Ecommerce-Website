from django.contrib import admin
from .models import ShippingAddress, Order, OrderItem


# Register your models here.
admin.site.register(ShippingAddress)
admin.site.register(Order)
admin.site.register(OrderItem)

class OrderItemInline(admin.StackedInline):
	model= OrderItem
	extra = 0

class OrderAdmin(admin.ModelAdmin):
	model = Order
	inlines = [OrderItemInline]

# unregister the Order model and reregister the OrderAdmin and Order
admin.site.unregister(Order)
admin.site.register(Order, OrderAdmin)