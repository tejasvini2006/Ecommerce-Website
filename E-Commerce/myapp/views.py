from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from .forms import CustomerSignupForm, ShopkeeperSignupForm
from .models import Product, Category, Cart, CartItem, Order, OrderItem, Feedback, UserProfile, User, Shopkeeper, Customer
from django.db.models.deletion import transaction

# Create your views here.

def signup(request):
    if request.user.is_authenticated:
        return redirect('product_list')
        
    if request.method == 'POST':
        form = CustomerSignupForm(request.POST)
        if form.is_valid():
            try:
                with transaction.atomic():
                    # Create User
                    user = form.save(commit=False)
                    user.set_password(form.cleaned_data['password1'])
                    user.save()
                    
                    # Create UserProfile
                    UserProfile.objects.create(
                        user=user,
                        user_type='customer'
                    )
                    
                    # Create Customer
                    Customer.objects.create(
                        user=user,
                        mobile=form.cleaned_data['phone'],
                        address=form.cleaned_data['address']
                    )
                    
                    # Log the user in
                    login(request, user)
                    messages.success(request, 'Account created successfully!')
                    return redirect('product_list')
            except Exception as e:
                messages.error(request, f'Error creating account: {str(e)}')
                return render(request, 'myapp/signup.html', {'form': form})
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = CustomerSignupForm()
        
    return render(request, 'myapp/signup.html', {'form': form})

def login_view(request):
    if request.user.is_authenticated:
        return redirect('product_list')
        
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user_type = request.POST.get('user_type', 'customer')
        
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            try:
                user_profile = UserProfile.objects.get(user=user)
                if user_profile.user_type == user_type:
                    login(request, user)
                    messages.success(request, 'Logged in successfully!')
                    if user_type == 'shopkeeper':
                        return redirect('shopkeeper_dashboard')
                    return redirect('product_list')
                else:
                    messages.error(request, 'Invalid role selected for this account.')
            except UserProfile.DoesNotExist:
                messages.error(request, 'User profile not found.')
        else:
            messages.error(request, 'Invalid username or password.')
    
    return render(request, 'myapp/login.html')

def logout_view(request):
    # Clear any existing messages
    storage = messages.get_messages(request)
    for message in storage:
        pass
    
    # Logout the user
    logout(request)
    
    # Add a success message that will be shown on the login page
    messages.success(request, 'You have been successfully logged out.')
    
    # Redirect to login page
    return redirect('login')

@login_required(login_url='login')
def home(request):
    try:
        user_profile = UserProfile.objects.get(user=request.user)
        if user_profile.user_type == 'shopkeeper':
            return redirect('shopkeeper_dashboard')
        return redirect('product_list')
    except UserProfile.DoesNotExist:
        messages.error(request, 'User profile not found.')
        return redirect('login')

@login_required
def shopkeeper_dashboard(request):
    if not hasattr(request.user, 'userprofile') or request.user.userprofile.user_type != 'shopkeeper':
        messages.error(request, 'Access denied. Shopkeeper privileges required.')
        return redirect('home')
    
    try:
        # Get all products
        products = Product.objects.all().order_by('-created_at')
        
        # Get recent orders
        recent_orders = Order.objects.all().order_by('-order_date')[:5]
        
        # Calculate subtotal and total
        subtotal = sum(order.total_amount for order in recent_orders)
        shipping = 0  # Shipping is free
        total = subtotal + shipping
        
        context = {
            'products': products,
            'recent_orders': recent_orders,
            'subtotal': subtotal,
            'total': total
        }
        
        return render(request, 'myapp/shopkeeper_dashboard.html', context)
    except Exception as e:
        print(f"Error in shopkeeper_dashboard: {str(e)}")
        messages.error(request, f'Error loading dashboard: {str(e)}')
        return redirect('home')

@login_required
def add_product(request):
    if not hasattr(request.user, 'userprofile') or request.user.userprofile.user_type != 'shopkeeper':
        return redirect('home')
    
    if request.method == 'POST':
        name = request.POST.get('name')
        category_id = request.POST.get('category')
        description = request.POST.get('description')
        price = request.POST.get('price')
        sale_price = request.POST.get('sale_price')
        stock = request.POST.get('stock')
        is_active = request.POST.get('is_active') == 'on'
        
        try:
            category = Category.objects.get(id=category_id)
            product = Product.objects.create(
                name=name,
                category=category,
                description=description,
                price=price,
                sale_price=sale_price if sale_price else None,
                stock=stock,
                is_active=is_active
            )
            
            if 'product_image' in request.FILES:
                product.product_image = request.FILES['product_image']
                product.save()
            
            messages.success(request, 'Product added successfully!')
            return redirect('shopkeeper_dashboard')
        except Exception as e:
            messages.error(request, f'Error adding product: {str(e)}')
    
    categories = Category.objects.all()
    return render(request, 'myapp/add_product.html', {'categories': categories})

@login_required
def edit_product(request, product_id):
    if not hasattr(request.user, 'userprofile') or request.user.userprofile.user_type != 'shopkeeper':
        return redirect('home')
    
    product = get_object_or_404(Product, id=product_id)
    
    if request.method == 'POST':
        product.name = request.POST.get('name')
        product.category_id = request.POST.get('category')
        product.description = request.POST.get('description')
        product.price = request.POST.get('price')
        product.sale_price = request.POST.get('sale_price') or None
        product.stock = request.POST.get('stock')
        product.is_active = request.POST.get('is_active') == 'on'
        
        if 'product_image' in request.FILES:
            product.product_image = request.FILES['product_image']
        
        try:
            product.save()
            messages.success(request, 'Product updated successfully!')
            return redirect('shopkeeper_dashboard')
        except Exception as e:
            messages.error(request, f'Error updating product: {str(e)}')
    
    categories = Category.objects.all()
    return render(request, 'myapp/edit_product.html', {
        'product': product,
        'categories': categories
    })

@login_required
def delete_product(request, product_id):
    if not hasattr(request.user, 'userprofile') or request.user.userprofile.user_type != 'shopkeeper':
        return redirect('home')
    
    if request.method == 'POST':
        product = get_object_or_404(Product, id=product_id)
        try:
            product.delete()
            messages.success(request, 'Product deleted successfully!')
        except Exception as e:
            messages.error(request, f'Error deleting product: {str(e)}')
    
    return redirect('shopkeeper_dashboard')

@login_required
def order_detail(request, order_id):
    if not hasattr(request.user, 'userprofile') or request.user.userprofile.user_type != 'shopkeeper':
        return redirect('home')
    
    order = get_object_or_404(Order, id=order_id)
    return render(request, 'myapp/order_detail.html', {'order': order})

@login_required
def update_order_status(request, order_id):
    if not hasattr(request.user, 'userprofile') or request.user.userprofile.user_type != 'shopkeeper':
        return redirect('home')
    
    if request.method == 'POST':
        order = get_object_or_404(Order, id=order_id)
        new_status = request.POST.get('status')
        
        if new_status in ['pending', 'shipped', 'out_for_delivery', 'delivered']:
            order.status = new_status
            order.save()
            messages.success(request, 'Order status updated successfully!')
        else:
            messages.error(request, 'Invalid order status!')
    
    return redirect('order_detail', order_id=order_id)

@login_required
def all_orders(request):
    if not hasattr(request.user, 'userprofile') or request.user.userprofile.user_type != 'shopkeeper':
        return redirect('home')
    
    orders = Order.objects.all().order_by('-order_date')
    return render(request, 'myapp/all_orders.html', {'orders': orders})

@login_required
def customer_dashboard(request):
    if not hasattr(request.user, 'userprofile') or request.user.userprofile.user_type != 'customer':
        return redirect('home')
    return render(request, 'myapp/customer_dashboard.html')

@login_required(login_url='login')
def product_list(request):
    category_id = request.GET.get('category')
    search_query = request.GET.get('search', '')
    sort_by = request.GET.get('sort', 'name')
    
    products = Product.objects.filter(is_active=True)
    
    if category_id:
        products = products.filter(category_id=category_id)
    
    if search_query:
        products = products.filter(
            Q(name__icontains=search_query) |
            Q(description__icontains=search_query) |
            Q(category__name__icontains=search_query)
        )
    
    if sort_by == 'price_low':
        products = products.order_by('price')
    elif sort_by == 'price_high':
        products = products.order_by('-price')
    elif sort_by == 'newest':
        products = products.order_by('-created_at')
    else:
        products = products.order_by('name')
    
    categories = Category.objects.all()
    return render(request, 'myapp/product_list.html', {
        'products': products,
        'categories': categories,
        'selected_category': category_id,
        'search_query': search_query,
        'sort_by': sort_by
    })

@login_required(login_url='login')
def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id, is_active=True)
    related_products = Product.objects.filter(
        category=product.category,
        is_active=True
    ).exclude(id=product_id)[:4]
    
    feedbacks = Feedback.objects.filter(product=product)
    return render(request, 'myapp/product_detail.html', {
        'product': product,
        'related_products': related_products,
        'feedbacks': feedbacks
    })

@login_required(login_url='login')
def add_to_cart(request, product_id):
    if request.method == 'POST':
        product = get_object_or_404(Product, id=product_id)
        quantity = int(request.POST.get('quantity', 1))
        order_now = request.POST.get('order_now') == 'true'
        
        if quantity > product.stock:
            messages.error(request, 'Not enough stock available!')
            return redirect('product_detail', product_id=product_id)
        
        cart, created = Cart.objects.get_or_create(customer=request.user.customer)
        
        # If order_now is True, clear existing cart items
        if order_now:
            cart.cartitem_set.all().delete()
        
        # Create or update cart item
        cart_item, created = CartItem.objects.get_or_create(
            cart=cart,
            product=product,
            defaults={'quantity': quantity}
        )
        
        if not created:
            cart_item.quantity += quantity
            cart_item.save()
        
        messages.success(request, 'Product added to cart successfully!')
        
        if order_now:
            return redirect('checkout')
        return redirect('cart')
    
    return redirect('product_detail', product_id=product_id)

@login_required(login_url='login')
def cart(request):
    try:
        cart = Cart.objects.get(customer=request.user.customer)
        cart_items = cart.cartitem_set.all()
        
        # Calculate totals
        subtotal = cart.get_cart_total
        shipping_cost = 0  # Shipping is free
        total = subtotal + shipping_cost
        
        context = {
            'cart_items': cart_items,
            'subtotal': subtotal,
            'shipping_cost': shipping_cost,
            'total': total
        }
    except Cart.DoesNotExist:
        context = {
            'cart_items': [],
            'subtotal': 0,
            'shipping_cost': 0,
            'total': 0
        }
    
    return render(request, 'myapp/cart.html', context)

@login_required(login_url='login')
def update_cart(request, cart_item_id):
    if request.method == 'POST':
        cart_item = get_object_or_404(CartItem, id=cart_item_id, cart__customer=request.user.customer)
        quantity = int(request.POST.get('quantity', 1))
        
        if quantity > cart_item.product.stock:
            messages.error(request, 'Not enough stock available!')
            return redirect('cart')
        
        cart_item.quantity = quantity
        cart_item.save()
        messages.success(request, 'Cart updated successfully!')
    
    return redirect('cart')

@login_required(login_url='login')
def remove_from_cart(request, cart_item_id):
    cart_item = get_object_or_404(CartItem, id=cart_item_id, cart__customer=request.user.customer)
    cart_item.delete()
    messages.success(request, 'Product removed from cart!')
    return redirect('cart')

@login_required(login_url='login')
def checkout(request):
    try:
        cart = Cart.objects.get(customer=request.user.customer)
        cart_items = cart.cartitem_set.all()
        
        if not cart_items:
            messages.error(request, 'Your cart is empty!')
            return redirect('cart')
        
        if request.method == 'POST':
            # Create order
            order = Order.objects.create(
                customer=request.user.customer,
                cart=cart,
                total_amount=cart.get_cart_total,
                shipping_address=request.user.customer.address  # Use customer's address
            )
            
            # Create order items
            for cart_item in cart_items:
                OrderItem.objects.create(
                    order=order,
                    product=cart_item.product,
                    quantity=cart_item.quantity,
                    price=cart_item.product.sale_price or cart_item.product.price
                )
            
            # Clear cart
            cart_items.delete()
            
            # Show success message
            messages.success(request, 'Your order has been placed successfully!')
            return redirect('product_list')
        
        return render(request, 'myapp/checkout.html', {
            'cart_items': cart_items,
            'total': cart.get_cart_total
        })
    
    except Cart.DoesNotExist:
        messages.error(request, 'Your cart is empty!')
        return redirect('cart')

@login_required(login_url='login')
def order_confirmation(request, order_id):
    order = get_object_or_404(Order, id=order_id, customer=request.user.customer)
    
    # Calculate totals for the order
    order.subtotal = order.total_amount
    order.shipping_cost = 0  # Shipping is free
    order.total = order.subtotal + order.shipping_cost
    
    return render(request, 'myapp/order_confirmation.html', {'order': order})

@login_required(login_url='login')
def order_history(request):
    orders = Order.objects.filter(customer=request.user.customer).order_by('-order_date')
    
    # Calculate totals for all orders
    for order in orders:
        order.subtotal = order.total_amount
        order.shipping_cost = 0  # Shipping is free
        order.total = order.subtotal + order.shipping_cost
    
    return render(request, 'myapp/order_history.html', {'orders': orders})

@login_required(login_url='login')
def add_feedback(request, product_id):
    if request.method == 'POST':
        product = get_object_or_404(Product, id=product_id)
        rating = int(request.POST.get('rating'))
        comment = request.POST.get('comment')
        
        Feedback.objects.create(
            customer=request.user.customer,
            product=product,
            rating=rating,
            comment=comment
        )
        
        messages.success(request, 'Thank you for your feedback!')
        return redirect('product_detail', product_id=product_id)
    
    return redirect('product_detail', product_id=product_id)
