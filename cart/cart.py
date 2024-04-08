from store.models import Product, Profile

class Cart:
	def __init__(self, request):
		self.session = request.session

		#get request
		self.request = request

		cart = self.session.get('session_key')
		if 'session_key' not in request.session:
			cart = self.session['session_key'] = {}


		# making sure the cart is available on all pages of the site
		self.cart = cart


	def db_add(self, product, quantity):
		product_id = str(product)
		product_qty = str(quantity)

		if product_id in self.cart:
			pass
		else:
			self.cart[product_id] = int(product_qty)
		self.session.modified = True

		#saving logged in user stuff
		if self.request.user.is_authenticated:
			#get the curnt user
			current_user = Profile.objects.filter(user__id=self.request.user.id)

			#in the cart obj, converting string crts. "'" into " " "
			#{'3':2, '5':1} into {"3":2, "5":1}
			cart_str = str(self.cart)
			cart_str = cart_str.replace("\'", "\"")

			#save cart_str in the profiles' field
			current_user.update(old_cart=cart_str)



	def add(self, product, quantity):
		product_id = str(product.id)
		product_qty = str(quantity)

		if product_id in self.cart:
			pass
		else:
			self.cart[product_id] = int(product_qty)
		self.session.modified = True

		#saving logged in user stuff
		if self.request.user.is_authenticated:
			#get the curnt user
			current_user = Profile.objects.filter(user__id=self.request.user.id)

			#in the cart obj, converting string crts. "'" into " " "
			#{'3':2, '5':1} into {"3":2, "5":1}
			cart_str = str(self.cart)
			cart_str = cart_str.replace("\'", "\"")

			#save cart_str in the profiles' field
			current_user.update(old_cart=cart_str)

	def __len__(self):
		return len(self.cart)

	def get_cart_products(self):
		#get ids of thr cart
		product_ids = self.cart.keys()

		#lookup ids to find the product model in DB
		products = Product.objects.filter(id__in=product_ids)

		return products

	def get_quantities(self):
		quantities = self.cart
		return quantities

	def update(self, product, quantity):

		product_id = str(product)
		product_qty = int(quantity)

		# update the cart
		updated_cart = self.cart
		updated_cart[product_id] = product_qty 

		self.session.modified = True

		#saving logged in user stuff
		if self.request.user.is_authenticated:
			#get the curnt user
			current_user = Profile.objects.filter(user__id=self.request.user.id)

			#in the cart obj, converting string crts. "'" into " " "
			#{'3':2, '5':1} into {"3":2, "5":1}
			cart_str = str(self.cart)
			cart_str = cart_str.replace("\'", "\"")

			#save cart_str in the profiles' field
			current_user.update(old_cart=cart_str)

		updated_cart_obj = self.cart
		return updated_cart_obj

	def delete(self, product):
		product_id = str(product)
		if product_id in self.cart:
			del self.cart[product_id]

		self.session.modified = True

		#saving logged in user stuff
		if self.request.user.is_authenticated:
			#get the curnt user
			current_user = Profile.objects.filter(user__id=self.request.user.id)

			#in the cart obj, converting string crts. "'" into " " "
			#{'3':2, '5':1} into {"3":2, "5":1}
			cart_str = str(self.cart)
			cart_str = cart_str.replace("\'", "\"")

			#save cart_str in the profiles' field
			current_user.update(old_cart=cart_str)


	def cart_total(self):
		# get product ids from dict
		product_ids = self.cart.keys()

		#use those ids to search the relevent products in Db
		products = Product.objects.filter(id__in=product_ids)

		#get quantities
		quantities = self.cart

		total = 0
		for key, value in quantities.items():
			key = int(key)
			for product in products:
				if product.id == key:
					if product.is_sale:
						total = total + (product.sale_price*value)
					else:
						total = total + (product.price*value)
		return total






