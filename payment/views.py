from django.shortcuts import render, redirect
from cart.cart import Cart
from payment.forms import ShippingForm, PaymentForm
from payment.models import ShippingAddress, Order, OrderItem
from django.contrib import messages
from django.contrib.auth.models import User


def process_order(request):
	if request.POST:

		#grab data from the cart
		cart = Cart(request)
		cart_products = cart.get_cart_products()
		quantities = cart.get_quantities()
		totals = cart.cart_total()

		#get billing info
		payment_form = PaymentForm(request.POST or None)

		#get shipping session data
		my_shipping = request.session.get('my_shipping')

		# gathering order info
		full_name = my_shipping['shipping_full_name']
		email = my_shipping['shipping_email']
		
		#create shipping address from shipping info
		shipping_address = f"{my_shipping['shipping_address1']}\n{my_shipping['shipping_address2']}\n{my_shipping['shipping_city']}\n{my_shipping['shipping_state']}\n{my_shipping['shipping_zipcode']}\n{my_shipping['shipping_country']}"
		amount_paid = totals

		# if the user is logged in
		if request.user.is_authenticated:
			user = request.user

			#The order
			create_order = Order(user=user, full_name=full_name, email=email,shipping_address=shipping_address, amount_paid=amount_paid)
			create_order.save()

			#get order id
			order_id = create_order.pk

			#get information on each product
			for product in cart_products:

				# product id
				product_id = product.id

				#product price
				if product.is_sale:
					price = product.sale_price
				else:
					price = product.price

				for key,value in quantities.items():
					if int(key) == product.id:
						# creating the order item
						create_order_item = OrderItem(user=user, order_id=order_id, product_id=product_id, quantity=value, price=price)
						create_order_item.save()

			#clearing the cart after checkout
			for key in list(request.session.keys()):
				if key == "session_key":
					del request.session[key]


			messages.success(request, 'Order Placed!')
			return redirect('home')

		else:
			create_order = Order(full_name=full_name, email=email,shipping_address=shipping_address, amount_paid=amount_paid)
			create_order.save()

			#get order id
			order_id = create_order.pk

			#get information on each product
			for product in cart_products:

				# product id
				product_id = product.id

				#product price
				if product.is_sale:
					price = product.sale_price
				else:
					price = product.price

				for key,value in quantities.items():
					if int(key) == product.id:
						# creating the order item
						create_order_item = OrderItem(order_id=order_id, product_id=product_id, quantity=value, price=price)
						create_order_item.save()

			#clearing the cart after checkout
			for key in list(request.session.keys()):
				if key == "session_key":
					del request.session[key]

			messages.success(request, 'Order Placed!')
			return redirect('home')


	else:
		messages.success(request, 'Access Denied!')
		return redirect('home')


def blling_info(request):
	if request.POST:
# get the cart
		cart = Cart(request)
		cart_products = cart.get_cart_products
		quantities = cart.get_quantities
		totals = cart.cart_total()

		my_shipping = request.POST
		request.session['my_shipping'] = my_shipping

		if request.user.is_authenticated:
			billing_form = PaymentForm()
			return render(request,
					 'payment/billing_info.html',
					  {'cart_products': cart_products,
					  	'quantities': quantities,
					  	'totals':totals,
					  	'shipping_data': request.POST,
					  	'billing_form' : billing_form
					  }
					)
# for guest user
		else:
			billing_form = PaymentForm()
			return render(request,
					 'payment/billing_info.html',
					  {'cart_products': cart_products,
					  	'quantities': quantities,
					  	'totals':totals,
					  	'shipping_data': request.POST,
					  	'billing_form' : billing_form
					  }
					)


		shipping_form = request.POST
		return render(request,
					 'payment/billing_info.html',
					  {'cart_products': cart_products,
					  	'quantities': quantities,
					  	'totals':totals,
					  	'shipping_form': shipping_form
					  }
					)
	else:
		messages.success(request, 'Access Denied!')
		return redirect('home')



def payment_success(request):
	return render(request, 'payment/payment_success.html', {})

def checkout(request):
	cart = Cart(request)
	cart_products = cart.get_cart_products
	quantities = cart.get_quantities
	totals = cart.cart_total()

	if request.user.is_authenticated:
		# Checkout as logged in user
		# Shipping User
		shipping_user = ShippingAddress.objects.get(user__id=request.user.id)
		
		shipping_form = ShippingForm(request.POST or None, instance=shipping_user)

		return render(request,
					 'payment/checkout.html',
					  {'cart_products': cart_products,
					  	'quantities': quantities,
					  	'totals':totals,
					  	'shipping_form': shipping_form
					  }
					 )
	else:
		# Checkout as guest
		shipping_form = ShippingForm(request.POST or None)
		return render(request,
					 'payment/checkout.html',
					  {'cart_products': cart_products,
					  	'quantities': quantities,
					  	'totals':totals,
					  	'shipping_form': shipping_form
					  }
					 )
