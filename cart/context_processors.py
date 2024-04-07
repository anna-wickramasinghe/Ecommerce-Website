from .cart import Cart

# create conteext available for all the pages.
def cart(request):
	# return the defult data from the Cart
	return {'cart': Cart(request)}

	