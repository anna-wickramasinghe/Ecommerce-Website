from django.shortcuts import render, redirect
from .models import Product, Category, Profile
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .forms import SignUpForm, UpdateUserForm, ChangePasswordForm, UserInfoForm
from django import forms
from django.db.models import Q
import json
from cart.cart import Cart


def search(request):
	if request.method =='POST':
		#catch the user enterd word
		searched = request.POST['searched']

		#filter out products that word is contained case insensitively
		searched = Product.objects.filter(Q(name__icontains=searched) | Q(description__icontains=searched) | Q(sub_title__icontains=searched))

		# if no such search item
		if not searched:
			messages.success(request, "That product does not exist. Please try with different key words...")
			return render(request, "search.html", {})
		return render(request, "search.html", {'searched':searched})
	else:
		return render(request, 'search.html', {})


def update_info(request):
	if request.user.is_authenticated:
		current_user = Profile.objects.get(id=request.user.id)
		form = UserInfoForm(request.POST or None, instance=current_user)

		if form.is_valid():
			form.save()
			messages.success(request, "Shipping information has been updated successfully!!")
			return redirect('home')
		return render(request, 'update_info.html', {'form':form})

	else:
		messages.success(request, "You must be logged in to update your shipping information.")
		return redirect('home')


def update_password(request):
	if request.user.is_authenticated:
		current_user = request.user

		#if filled the form
		if request.method == 'POST':
			form = ChangePasswordForm(current_user, request.POST)

			if form.is_valid():
				form.save()
				messages.success(request, "Your Password Has Been Updated. Please Log In Agan..!")
				return redirect('login')

			else:
				for error in list(form.errors.values()):
					messages.error(request, error)
					return redirect('update_password')
		else:
			form = ChangePasswordForm(current_user)	
			return render(request, 'update_password.html', {'form': form})
	else:
		messages.success(request, "You must be logged in to update th password")
		return redirect('home')

def all_categories(request):
	all_categories = Category.objects.all()
	return render(request, 'all_categories.html', {'all_categories':all_categories})

def home(request):
	products = Product.objects.all()
	return render(request, 'home.html', {'products':products})

def category(request,cat):
	cat = cat.replace('-',' ')
	try:
		category = Category.objects.get(name=cat)
		products = Product.objects.filter(category=category)
		return render(request,
					 'category.html',
					 	{'products':products,
						'category': category
						})
	except:
		messages.success(request, ("This category does not exist."))
		return redirect('home')

def product(request,pid):
	product = Product.objects.get(id=pid)
	return render(request, 'product.html', {'product':product})

def about(request):
	return render(request, 'about.html', {})

def login_user(request):
	if request.method == "POST":
		username = request.POST['username']
		password = request.POST['password']
		user = authenticate(request, username=username, password=password)
		if user is not None:
			login(request, user)

			#related to keeping the persistance of cart over login
			current_user = Profile.objects.get(user__id=request.user.id)
			saved_cart = current_user.old_cart

			#convert saved_cart string into a dictionary with using json
			if saved_cart:
				converted_cart = json.loads(saved_cart)

				#save this loaded cart into the session
				#get cart
				cart = Cart(request)

				#loop through the cart items from loaded cart dctionary
				for key,value in converted_cart.items():
					cart.db_add(product=key, quantity=value)




			messages.success(request, ("You have been logged in successfully...!"))
			return redirect('home')
		else:
			messages.success(request, ("There was an error, please try again...!"))
			return redirect('login')
	else:
		return render(request, 'login.html', {})

def logout_user(request):
	logout(request)
	messages.success(request, ("You have been logged out... Thanks for stoping to shop."))
	return redirect('home')

def register_user(request):
	form = SignUpForm()
	if request.method == "POST":
		form = SignUpForm(request.POST)
		if form.is_valid():
			form.save()
			username = form.cleaned_data['username']
			password = form.cleaned_data['password1']

			user = authenticate(username=username, password=password)
			login(request, user)
			messages.success(request, ("You have been registered successfully. Please fill out your shipping info below.!"))
			return redirect('update_info')
		else:
			messages.success(request, ("There seems to have a prblem in registering. Please try again."))
			return redirect('register')
	else:
		return render(request, 'register.html', {'form':form})


def update_user(request):
	if request.user.is_authenticated:
		current_user = User.objects.get(id=request.user.id)
		user_form = UpdateUserForm(request.POST or None, instance=current_user)

		if user_form.is_valid():
			user_form.save()

			login(request, current_user)
			messages.success(request, "User has been updated successfully!!")
			return redirect('home')
		return render(request, 'update_user.html', {'user_form':user_form})

	else:
		messages.success(request, "You must be logged in to update your profile.")
		return redirect('home')



	