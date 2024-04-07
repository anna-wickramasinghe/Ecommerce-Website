from store.models import Product

class Cart:
	def __init__(self, request):
		self.session = request.session

		cart = self.session.get('session_key')
		if 'session_key' not in request.session:
			cart = self.session['session_key'] = {}


		# making sure the cart is available on all pages of the site
		self.cart = cart

	def add(self, product, quantity):
		product_id = str(product.id)
		product_qty = str(quantity)

		if product_id in self.cart:
			pass
		else:
			self.cart[product_id] = int(product_qty)
		self.session.modified = True

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

		updated_cart_obj = self.cart
		return updated_cart_obj



