from django import template
from shop.models import Cart

register = template.Library()

def get_cart_data(request):
    if not request:
        return {'item_count': 0, 'total': 0.0, 'items': []}
    
    cart = None
    if request.user.is_authenticated:
        cart = Cart.objects.filter(user=request.user).first()
    else:
        session_key = request.session.session_key
        if session_key:
            cart = Cart.objects.filter(session_id=session_key).first()
            
    if cart:
        items = cart.items.all().select_related('product', 'variant').prefetch_related('product__images')
        return {
            'item_count': cart.get_item_count,
            'total': cart.get_total,
            'items': items
        }
    return {
        'item_count': 0,
        'total': 0.0,
        'items': []
    }

@register.inclusion_tag('cart/cart_button.html', takes_context=True)
def cart_button(context):
    request = context.get('request')
    return get_cart_data(request)

@register.inclusion_tag('cart/cart_panel.html', takes_context=True)
def cart_panel(context):
    request = context.get('request')
    return get_cart_data(request)
