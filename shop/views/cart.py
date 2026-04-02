from django.shortcuts import render

def index(request):
    """Main cart page."""
    return render(request, 'cart/cart.html')

# --- ADD THIS NEW FUNCTION ---
def empty_cart(request):
    """Page shown when the user's cart has no items."""
    return render(request, 'cart/empty_cart.html')
