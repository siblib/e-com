from django.shortcuts import render
from typing import Any, Dict

# 1. Checkout as Guest (The Form)
def checkout_guest(request):
    """Form for users checking out without an account."""
    context: Dict[str, Any] = {
        'type': 'guest'
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
    context: Dict[str, Any] = {}
    return render(request, 'checkout/review.html', context)

def payment(request):
    """Page to process credit card / payment logic."""
    context: Dict[str, Any] = {}
    return render(request, 'checkout/payment.html', context)

def order_confirmation(request):
    """Success page shown after payment is complete."""
    context: Dict[str, Any] = {}
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
