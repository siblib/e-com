from django.shortcuts import render
from django.contrib import messages

def dashboard(request): # "Account"
    return render(request, 'account/dashboard.html')

def personal_info(request):
    return render(request, 'account/personal_info.html')

def addresses(request):
    return render(request, 'account/addresses.html')

def my_orders(request):
    return render(request, 'account/my_orders.html')

def order_details(request):
    # TEMPORARY: Without order_id for testing
    return render(request, 'account/order_details.html', {'order_id': 1})  # Provide dummy data

def favorites(request):
    return render(request, 'account/favorites.html')

def payment_methods(request):
    """Render user's saved payment methods page."""
    # Placeholder context - replace with real data from database later
    context = {
        'saved_cards': [
            {'id': 1, 'brand': 'Visa', 'last4': '4242', 'expiry': '12/25', 'is_default': True},
            {'id': 2, 'brand': 'Mastercard', 'last4': '8888', 'expiry': '08/24', 'is_default': False},
        ],
        'billing_address': {
            'street': '123 Main St',
            'city': 'New York',
            'state': 'NY',
            'zip': '10001',
            'country': 'USA'
        }
    }
    return render(request, 'account/payment_methods.html', context)

def account_returns(request):
    """Render user's return history and initiate new returns."""
    # Placeholder context - replace with real order/return data later
    context = {
        'eligible_orders': [
            {'order_id': 1001, 'date': '2024-01-15', 'total': 89.99, 'status': 'Delivered', 'return_window_ends': '2024-02-14'},
            {'order_id': 1005, 'date': '2024-01-20', 'total': 124.50, 'status': 'Delivered', 'return_window_ends': '2024-02-19'},
        ],
        'return_requests': [
            {'request_id': 'RET-2024-001', 'order_id': 998, 'status': 'Approved', 'refund_amount': 45.00},
            {'request_id': 'RET-2024-003', 'order_id': 1002, 'status': 'Pending', 'refund_amount': 29.99},
        ]
    }
    return render(request, 'account/returns.html', context)
