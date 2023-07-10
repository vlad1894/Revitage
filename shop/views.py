from django.shortcuts import render, get_object_or_404
from .models import Product, Cart, CartItem, Subscription
from .forms import ProductForm

def home(request):
    return render(request, 'shop/index.html')


def shop(request):
    products = Product.objects.all()
    return render(request, 'shop/shop.html', {'products': products})

def about(request):
    return render(request, 'shop/about.html')



def add_to_cart(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_item = cart.items.filter(product=product).first()
    if cart_item:
        cart_item.quantity += 1
        cart_item.save()
    else:
        new_cart_item = CartItem(cart=cart, product=product, quantity=1)
        new_cart_item.save()
    return render(request, 'shop/base.html', {'cart': cart})




def subscribe_newsletter(request):
    if request.method == "POST":
        first_name = request.POST.get('first_name')
        email = request.POST.get('email')

        if not first_name or not email:
            error_message = "Please provide both First Name and Email."
            return render(request, 'shop/index.html', {'error_message': error_message})
        
        subscription = Subscription(first_name=first_name, email=email)
        subscription.save()
        
        return render(request, 'shop/index.html')
    return render(render, 'shop/index.html')


def cart_view(request):
    session_id = request.session.session_key
    
    cart = Cart.objects.filter(session_id=session_id).first()
    if not cart:
        cart = Cart.objects.create(session_id=session_id)
    
    total_price = 0
    cart_items = cart.items.all()
    for item in cart_items:
        total_price += item.quantity * item.product.price

    context = {
        'cart': cart,
        'cart_items': cart_items,
        'total_price': total_price,
    }

    return render(request, 'shop/cart.html', context)




def blog(request):
    return render(request, 'shop/blog.html')


# Create your views here.
