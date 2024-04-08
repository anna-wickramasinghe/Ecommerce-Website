from django.contrib import admin
from .models import Category, Order, Customer, Product, Profile
from django.contrib.auth.models import User

# Register your models here.
admin.site.register(Category)
admin.site.register(Product)
admin.site.register(Customer)
admin.site.register(Order)
admin.site.register(Profile)


# combine profile info and user info
class ProfileInline(admin.StackedInline):
	model = Profile


# exted User Profile
class UserAdmin(admin.ModelAdmin):
	model = User
	field = ["username", "first_name", "last_name", "email"]
	inlines = [ProfileInline]

# Unregister the old User
admin.site.unregister(User)

#Reregister the new UserProfile
admin.site.register(User, UserAdmin)
