from django.shortcuts import render, redirect
from typing import Any, Dict
from django.utils.crypto import get_random_string
from .cart import _get_or_create_cart, _cart_data
from shop.models import Order, OrderItem, Address

# 1. Checkout as Guest (The Form)
def checkout_guest(request):
    """Form for users checking out without an account."""
    cart = _get_or_create_cart(request)
    cart_data = _cart_data(cart)
    
    if request.method == 'POST':
        request.session['checkout_guest_data'] = {
            'guest_email': request.POST.get('guest_email', ''),
            'first_name': request.POST.get('first_name', ''),
            'last_name': request.POST.get('last_name', ''),
            'country': request.POST.get('country', ''),
            'address1': request.POST.get('address1', ''),
            'address2': request.POST.get('address2', ''),
            'city': request.POST.get('city', ''),
            'state': request.POST.get('state', ''),
            'zip_code': request.POST.get('zip_code', ''),
            'phone': request.POST.get('phone', ''),
            'shipping_method': request.POST.get('hs-pro-esdo', ''),
        }
        return redirect('shop:review_and_pay')

    context: Dict[str, Any] = {
        'type': 'guest',
        'cart_data': cart_data,
    }
    return render(request, 'checkout/checkout_guest.html', context)

# 2. Checkout Logged In (The Form)
def checkout_member(request):
    """Form for logged-in users (pre-filled with saved data)."""
    context: Dict[str, Any] = {
        'type': 'member',
        # In the future, you will query the user's address here
        'user_name': 'John Doe', 
    }
    return render(request, 'checkout/checkout_member.html', context)

# 3. Checkout Not Logged In (The Selection Page)
def checkout_options(request):
    """The 'interstitial' page: asks user to Login, Register, or Guest Checkout."""
    context: Dict[str, Any] = {}
    return render(request, 'checkout/checkout_options.html', context)

def review_and_pay(request):
    """Page to review order summary before final payment."""
    cart = _get_or_create_cart(request)
    cart_data = _cart_data(cart)
    guest_data = request.session.get('checkout_guest_data', {})

    if request.method == 'POST':
        # Create Address
        address = Address.objects.create(
            user=None,
            first_name=guest_data.get('first_name', ''),
            last_name=guest_data.get('last_name', ''),
            street_address=guest_data.get('address1', ''),
            address2=guest_data.get('address2', ''),
            city=guest_data.get('city', ''),
            state=guest_data.get('state', ''),
            postal_code=guest_data.get('zip_code', ''),
            country=guest_data.get('country', ''),
            phone=guest_data.get('phone', ''),
        )
        
        # Create Order
        order_number = get_random_string(10).upper()
        order = Order.objects.create(
            user=None,
            guest_email=guest_data.get('guest_email', ''),
            order_number=order_number,
            status='Pending',
            shipping_address=address,
        )
        
        # Create Order Items
        for item in cart.items.all():
            OrderItem.objects.create(
                order=order,
                product=item.product,
                quantity=item.quantity,
                price_at_purchase=item.variant.price if item.variant and item.variant.price else item.product.price,
            )
            
        # Clear cart
        cart.items.all().delete()
        
        # Store order in session
        request.session['last_order_number'] = order.order_number
        return redirect('shop:order_confirmation')

    context: Dict[str, Any] = {
        'cart_data': cart_data,
        'guest_data': guest_data,
    }
    return render(request, 'checkout/review.html', context)

def payment(request):
    """Page to process credit card / payment logic."""
    context: Dict[str, Any] = {}
    return render(request, 'checkout/payment.html', context)

def order_confirmation(request):
    """Success page shown after payment is complete."""
    order_number = request.session.get('last_order_number')
    order = None
    if order_number:
        order = Order.objects.filter(order_number=order_number).first()
        
    context: Dict[str, Any] = {
        'order': order,
    }
    return render(request, 'checkout/confirmation.html', context)

# --- RENAMED TO: order_status ---
def order_status(request):
    """Page that DISPLAYS the actual order status results."""
    context: Dict[str, Any] = {}
    return render(request, 'checkout/order_status.html', context)

# --- KEPT AS: order_checkup ---
def order_checkup(request):
    """Entry page for guests to SEARCH for their order using ID and Email."""
    context: Dict[str, Any] = {}
    return render(request, 'checkout/order_checkup.html', context)
