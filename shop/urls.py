from django.urls import path
from . import views

app_name = 'shop'

urlpatterns = [
    path('', views.home, name='home'),
    path('shop/', views.shop, name='shop'),
    path('about/', views.about, name='about'),
    path('add_to_cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('subscribe/', views.subscribe_newsletter, name='subscribe'),
    path('cart/', views.cart_view, name='cart'),
    path('cart/item/<int:item_id>/update/', views.update_cart_item, name='update_cart_item'),
    path('cart/item/<int:item_id>/remove/', views.remove_cart_item, name='remove_cart_item'),
    path('blog/', views.blog, name='blog'),
    path('blog/admin/', views.blog_admin, name='blog_admin'),
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('account/', views.account_view, name='account'),
    path('logout/', views.logout_view, name='logout'),
]
