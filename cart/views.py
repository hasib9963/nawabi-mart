from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from products.models import Product
from .models import Cart, CartItem, Order, OrderItem
from django.http import HttpResponse
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from products.models import Product
from .models import Cart, CartItem

def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    if request.user.is_authenticated:
        cart, created = Cart.objects.get_or_create(user=request.user)
        cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
        if not created:
            cart_item.quantity += 1
            cart_item.save()
        
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            # Respond with JSON for AJAX requests
            return JsonResponse({
                'success': True,
                'message': 'Product added to cart.',
                'cart_count': cart.items.count()
            })
        else:
            return redirect('home')  # Redirect to cart page for authenticated users
    else:
        # Handle session-based cart for non-authenticated users
        cart = request.session.get('cart', {})
        if str(product_id) not in cart:
            cart[str(product_id)] = {'quantity': 1, 'price': str(product.price)}
        else:
            cart[str(product_id)]['quantity'] += 1
        request.session['cart'] = cart  # Update the session

        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            # Respond with JSON for AJAX requests
            return JsonResponse({
                'success': True,
                'message': 'Product added to cart.',
                'cart_count': len(request.session['cart'])
            })
        else:
            return redirect('home') 


def view_cart(request):
    if request.user.is_authenticated:
        # Handle authenticated users
        cart, created = Cart.objects.get_or_create(user=request.user)
        items = cart.items.all()
        # Add total_price to each item in the cart
        items_with_total = [
            {
                'product': item.product,
                'quantity': item.quantity,
                'total_price': float(item.product.price) * item.quantity  # Calculate total price for each CartItem
            }
            for item in items
        ]
        # Calculate subtotal using CartItem objects
        subtotal = sum(item['total_price'] for item in items_with_total)
    else:
        # Handle anonymous users with session-based cart
        cart = request.session.get('cart', {})
        items_with_total = [
            {
                'product': get_object_or_404(Product, id=prod_id),
                'quantity': details['quantity'],
                'price': details['price'],
                'total_price': float(details['price']) * details['quantity'],  # Calculate total price for each item
            }
            for prod_id, details in cart.items()
        ]
        # Calculate subtotal for session-based cart
        subtotal = sum(item['total_price'] for item in items_with_total)
    
    # Define shipping cost
    shipping_cost = 45
    # Calculate total
    total = subtotal + shipping_cost

    context = {
        'items': items_with_total,  # Pass the modified list with total_price
        'subtotal': subtotal,
        'shipping_cost': shipping_cost,
        'total': total,
    }
    
    return render(request, 'cart.html', context)


def remove_from_cart(request, item_id):
    if request.user.is_authenticated:
        # Handle authenticated users
        cart = get_object_or_404(Cart, user=request.user)
        cart_item = get_object_or_404(CartItem, cart=cart, product_id=item_id)
        cart_item.delete()
    else:
        # Handle non-authenticated users (session-based cart)
        cart = request.session.get('cart', {})
        if str(item_id) in cart:
            del cart[str(item_id)]
            request.session['cart'] = cart  # Update the session
    
    return redirect('cart')


def update_cart(request):
    if request.method == 'POST':
        if request.user.is_authenticated:
            # For authenticated users
            cart, created = Cart.objects.get_or_create(user=request.user)
            for item_id, quantity in request.POST.items():
                if item_id.startswith('item_'):
                    item_id = item_id.split('_')[1]
                    quantity = int(quantity)
                    cart_item = get_object_or_404(CartItem, id=item_id, cart=cart)
                    if quantity <= 0:
                        cart_item.delete()
                    else:
                        cart_item.quantity = quantity
                        cart_item.save()
        else:
            # For non-authenticated users (session-based cart)
            session_cart = request.session.get('cart', {})
            for item_id, quantity in request.POST.items():
                if item_id.startswith('item_'):
                    item_id = item_id.split('_')[1]
                    quantity = int(quantity)
                    
                    if item_id in session_cart:
                        if quantity <= 0:
                            del session_cart[item_id]  # Remove the item if the quantity is 0 or less
                        else:
                            session_cart[item_id]['quantity'] = quantity  # Update the quantity
            request.session['cart'] = session_cart  # Update the session

        return redirect('cart')
    else:
        return HttpResponse(status=405)


def checkout(request):
    if not request.user.is_authenticated:
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            # Respond with JSON for AJAX requests when user is not authenticated
            return JsonResponse({
                'success': False,
                'message': 'Please log in first to proceed the checkout.',
                'redirect_url': '/login/'  # Provide the login URL for redirection
            })
        else:
            # If not an AJAX request, redirect to login
            return redirect('login')

    # Handle authenticated users
    cart, created = Cart.objects.get_or_create(user=request.user)
    items = cart.items.all()
    subtotal = sum(float(item.product.price) * item.quantity for item in items)
    
    shipping_cost = 45
    total = subtotal + shipping_cost

    context = {
        'items': items,
        'subtotal': subtotal,
        'shipping_cost': shipping_cost,
        'total': total,
    }

    return render(request, 'checkout.html', context)



@login_required
def place_order(request):
    if request.method == 'POST':
        user = request.user
        try:
            cart = Cart.objects.get(user=user)
        except Cart.DoesNotExist:
            return redirect('cart')  # Redirect if no cart exists

        # Retrieve billing information from the form
        billing_address = request.POST.get('billing_address')
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        note = request.POST.get('note', '')

        # Create an Order
        order = Order.objects.create(
            user=user,
            billing_address=billing_address,
            name=name,
            email=email,
            phone=phone,
            note=note,
            total_price=cart.get_total_price(),
        )

        # Move items from the cart to the order
        cart_items = CartItem.objects.filter(cart=cart)
        for cart_item in cart_items:
            OrderItem.objects.create(
                order=order,
                product=cart_item.product,
                price=cart_item.product.price,
                quantity=cart_item.quantity,
            )

        # Clear the cart
        cart_items.delete()  # Clear cart items
        cart.delete()  # Optionally delete the cart

        # Redirect to the success page
        return redirect('checkout_success')

    return redirect('checkout')



def checkout_success(request):
    return render(request, 'checkout_success.html')


def user_orders(request):
    if request.user.is_authenticated:
        # Handle authenticated users
        cart, created = Cart.objects.get_or_create(user=request.user)
        items = cart.items.all()
        # Calculate subtotal using CartItem objects
        subtotal = sum(float(item.product.price) * item.quantity for item in items)
    else:
        # Handle anonymous users with session-based cart
        cart = request.session.get('cart', {})
        items = [
            {
                'product': get_object_or_404(Product, id=prod_id),
                'quantity': details['quantity'],
                'price': details['price'],
            }
            for prod_id, details in cart.items()
        ]
        subtotal = sum(float(item['price']) * item['quantity'] for item in items)

    # Define shipping cost
    shipping_cost = 45
    # Calculate total
    total = subtotal + shipping_cost

    context = {
        'items': items,
        'subtotal': subtotal,
        'shipping_cost': shipping_cost,
        'total': total,
    }
    
    return render(request, 'orders.html', context)



# if you want tp clear item when user added to cart as a login user 

# from django.contrib.auth.signals import user_logged_in
# from django.dispatch import receiver

# @receiver(user_logged_in)
# def merge_cart_on_login(sender, request, user, **kwargs):
#     # Check if the session has a cart
#     session_cart = request.session.get('cart', None)
    
#     if session_cart:
#         # Get or create the cart for the logged-in user
#         cart, created = Cart.objects.get_or_create(user=user)
        
#         # Clear the user's previous cart items
#         cart.items.all().delete()

#         # Add the session cart items to the user's cart
#         for prod_id, details in session_cart.items():
#             product = get_object_or_404(Product, id=prod_id)
#             CartItem.objects.create(cart=cart, product=product, quantity=details['quantity'])
        
#         # Clear the session cart
#         del request.session['cart']


# if you want to keep items when user added to cart as a login user with non login user 

from django.contrib.auth.signals import user_logged_in
from django.dispatch import receiver

@receiver(user_logged_in)
def merge_cart_on_login(sender, request, user, **kwargs):
    # Check if the session has a cart
    session_cart = request.session.get('cart', None)

    if session_cart:
        # Get or create the cart for the logged-in user
        cart, created = Cart.objects.get_or_create(user=user)

        for prod_id, details in session_cart.items():
            product = get_object_or_404(Product, id=prod_id)

            # Check if the product is already in the user's cart
            cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)

            if not created:
                # If product already exists, increase the quantity
                cart_item.quantity += details['quantity']
            else:
                # If product doesn't exist, add it to the cart
                cart_item.quantity = details['quantity']

            cart_item.save()

        # Clear the session cart after merging
        del request.session['cart']
