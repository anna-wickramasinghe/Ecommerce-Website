from django.db import models
from django.contrib.auth.models import User
from store.models import Product
from django.db.models.signals import post_save
import datetime

class ShippingAddress(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
	shipping_full_name = models.CharField(max_length=255)
	shipping_email = models.CharField(max_length=255)
	shipping_address1 = models.CharField(max_length=255)
	shipping_address2 = models.CharField(max_length=255, null=True, blank=True)
	shipping_city = models.CharField(max_length=255)
	shipping_state = models.CharField(max_length=255, null=True, blank=True)
	shipping_zipcode = models.CharField(max_length=255, null=True, blank=True)
	shipping_country = models.CharField(max_length=255)

	class Meta:
		verbose_name_plural = "Shipping Address"

	def __str__(self):
		return f'Shipping Adress: {str(self.id)}'



#dcreate a shipping address bydefalt when a user is created.
def create_shipping(sender, instance, created, **kwargs):
	if created:
		user_shipping = ShippingAddress(user=instance)
		user_shipping.save()

post_save.connect(create_shipping, sender=User)




class Order(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
	full_name = models.CharField(max_length=250, null=True)
	email = models.EmailField(max_length=250, null=True)
	shipping_address = models.TextField(max_length=15000, null=True)
	amount_paid = models.DecimalField(max_digits=20, decimal_places=2, null=True)
	date_ordered = models.DateField(default=datetime.datetime.today)

	def __str__(self):
		return f'Order: {str(self.id)}'


class OrderItem(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
	order = models.ForeignKey(Order, on_delete=models.CASCADE, null=True)
	product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True)
	quantity = models.PositiveBigIntegerField(default=1)
	price = models.DecimalField(max_digits=20, decimal_places=2)

	def __str__(self):
		return f'Order Item: {str(self.id)}'
