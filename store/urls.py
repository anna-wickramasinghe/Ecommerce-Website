from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('register/', views.register_user, name='register'),
    path('product/<int:pid>', views.product, name='product'),
    path('category/<str:cat>', views.category, name='category'),
    path('all_categories/', views.all_categories, name='all_categories'),
]
