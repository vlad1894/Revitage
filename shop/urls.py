from django.urls import path
from . import views
from .views import add_to_cart, subscribe_newsletter

app_name = 'shop'

urlpatterns = [
    path('', views.home, name = 'home'),
    path('shop/', views.shop, name='shop'),
    path('about/', views.about, name='about'),
    path('add_to_cart/<int:product_id>/', add_to_cart, name='add_to_cart'),
    path('subscribe/', subscribe_newsletter, name='subscribe')
]