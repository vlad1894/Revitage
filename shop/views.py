from .forms import ProductForm
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.conf import settings
from .models import Product, Cart, CartItem, Subscription
from .mongo import create_user, authenticate_user, create_blog_post, list_blog_posts

def home(request):
    return render(request, 'shop/index.html')


def shop(request):
    products = Product.objects.all()
    return render(request, 'shop/shop.html', {'products': products})

def about(request):
    return render(request, 'shop/about.html')



def add_to_cart(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    if not request.session.session_key:
        request.session.save()
    cart, created = Cart.objects.get_or_create(session_id=request.session.session_key)
    cart_item = cart.items.filter(product=product).first()
    if cart_item:
        cart_item.quantity += 1
        cart_item.save()
    else:
        new_cart_item = CartItem(cart=cart, product=product, quantity=1)
        new_cart_item.save()
    return redirect(request.META.get("HTTP_REFERER", "shop:shop"))




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
    return render(request, 'shop/index.html')


def cart_view(request):
    if not request.session.session_key:
        request.session.save()
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


def update_cart_item(request, item_id):
    if request.method != "POST":
        return redirect("shop:cart")

    if not request.session.session_key:
        request.session.save()
    session_id = request.session.session_key

    cart_item = get_object_or_404(CartItem, pk=item_id, cart__session_id=session_id)
    try:
        quantity = int(request.POST.get("quantity", cart_item.quantity))
    except (TypeError, ValueError):
        quantity = cart_item.quantity

    if quantity <= 0:
        cart_item.delete()
    else:
        cart_item.quantity = quantity
        cart_item.save()

    return redirect("shop:cart")


def remove_cart_item(request, item_id):
    if request.method != "POST":
        return redirect("shop:cart")

    if not request.session.session_key:
        request.session.save()
    session_id = request.session.session_key

    cart_item = get_object_or_404(CartItem, pk=item_id, cart__session_id=session_id)
    cart_item.delete()
    return redirect("shop:cart")




def blog(request):
    posts = list_blog_posts()
    if not posts:
        posts = [
            {
                "title": "Product 1 Rituals: Morning Energy in 3 Steps",
                "category": "Energy Reset",
                "excerpt": "Start with hydration, follow with a light protein breakfast, and add your daily Revitage blend.",
                "body": "Small, consistent habits beat big resets every time. Pair your morning ritual with a short walk to lock it in.",
            },
            {
                "title": "Product 2 Focus Windows: Protect Your Best Hours",
                "category": "Focus Formula",
                "excerpt": "Build a 90-minute focus window: silence alerts and stack your most important task first.",
                "body": "A calm routine makes focus stick. Keep water nearby and set a single intent for the session.",
            },
            {
                "title": "Product 3 Evening Wind-Down: A Softer Landing",
                "category": "Calm Balance",
                "excerpt": "Ease into the evening with dim lights and a device-free 15 minutes before bed.",
                "body": "Add a short stretch and warm tea to reduce stimulation and improve sleep quality.",
            },
        ]
    return render(request, 'shop/blog.html', {"posts": posts})


def register(request):
    if request.method == "POST":
        full_name = request.POST.get("full_name") or ""
        username = request.POST.get("username") or ""
        email = request.POST.get("email") or ""
        password = request.POST.get("password") or ""
        password2 = request.POST.get("password2") or ""

        if not username or not email or not password:
            messages.error(request, "Username, email, and password are required.")
            return render(request, "shop/register.html")

        if password != password2:
            messages.error(request, "Passwords do not match.")
            return render(request, "shop/register.html")

        try:
            user = create_user(username=username, email=email, password=password, full_name=full_name)
        except ValueError as e:
            messages.error(request, str(e))
            return render(request, "shop/register.html")

        messages.success(request, "Account created. You can log in now.")
        return redirect("shop:login")

    return render(request, "shop/register.html")


def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username") or ""
        password = request.POST.get("password") or ""

        user = authenticate_user(username_or_email=username, password=password)
        if not user:
            messages.error(request, "Invalid username or password.")
            return render(request, "shop/login.html")

        # store minimal info in session
        request.session["user_id"] = str(user["_id"])
        request.session["user_email"] = user.get("email", "")
        request.session["user_name"] = user.get("username", "")
        request.session["is_blog_admin"] = user.get("username") == settings.BLOG_ADMIN_USERNAME

        messages.success(request, "Logged in successfully.")
        return redirect("shop:shop")  # go to product listing

    return render(request, "shop/login.html")


def logout_view(request):
    request.session.flush()
    messages.info(request, "You have been logged out.")
    return redirect("shop:home")


def account_view(request):
    if not request.session.get("user_id"):
        messages.info(request, "Please log in to view your account.")
        return redirect("shop:login")

    context = {
        "user_id": request.session.get("user_id", ""),
        "user_email": request.session.get("user_email", ""),
        "user_name": request.session.get("user_name", ""),
    }
    return render(request, "shop/account.html", context)


def blog_admin(request):
    if not request.session.get("user_name"):
        messages.info(request, "Please log in to continue.")
        return redirect("shop:login")
    if request.session.get("user_name") != settings.BLOG_ADMIN_USERNAME:
        messages.error(request, "You do not have access to blog admin.")
        return redirect("shop:blog")

    if request.method == "POST":
        title = request.POST.get("title") or ""
        category = request.POST.get("category") or ""
        excerpt = request.POST.get("excerpt") or ""
        body = request.POST.get("body") or ""

        if not title or not body:
            messages.error(request, "Title and body are required.")
        else:
            try:
                create_blog_post(title=title, category=category, excerpt=excerpt, body=body)
                messages.success(request, "Blog post published.")
                return redirect("shop:blog_admin")
            except ValueError as exc:
                messages.error(request, str(exc))

    posts = list_blog_posts()
    return render(request, "shop/blog_admin.html", {"posts": posts})
# Create your views here.
