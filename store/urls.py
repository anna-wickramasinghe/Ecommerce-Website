from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('register/', views.register_user, name='register'),
    path('update_user/', views.update_user, name='update_user'),
    path('update_info/', views.update_info, name='update_info'),
    path('update_password/', views.update_password, name='update_password'),
    path('product/<int:pid>', views.product, name='product'),
    path('category/<str:cat>', views.category, name='category'),
    path('all_categories/', views.all_categories, name='all_categories'),
    path('search/', views.search, name='search'),
    
]
