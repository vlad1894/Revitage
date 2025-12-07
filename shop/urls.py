from django.urls import path
from . import views

app_name = 'shop'

urlpatterns = [
    path('', views.home, name='home'),
    path('shop/', views.shop, name='shop'),
    path('about/', views.about, name='about'),
    path('add_to_cart/', views.add_to_cart, name='add_to_cart'),
    path('subscribe/', views.subscribe_newsletter, name='subscribe'),
    path('cart/', views.cart_view, name='cart'),
    path('blog/', views.blog, name='blog'),
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
]