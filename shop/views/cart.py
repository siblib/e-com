import json
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from shop.models import Cart, CartItem, Product, ProductVariant

def index(request):
    """Main cart page."""
    return render(request, 'cart/cart.html')

def empty_cart(request):
    """Page shown when the user's cart has no items."""
    return render(request, 'cart/empty_cart.html')

def _get_or_create_cart(request):
    if request.user.is_authenticated:
        cart, created = Cart.objects.get_or_create(user=request.user)
    else:
        session_key = request.session.session_key
        if not session_key:
            request.session.create()
            session_key = request.session.session_key
        cart, created = Cart.objects.get_or_create(session_id=session_key)
    return cart

def _cart_data(cart):
    items = []
    for item in cart.items.all().select_related('product', 'variant'):
        variant_data = None
        if item.variant:
            variant_data = {
                'id': item.variant.id,
                'name': ' / '.join([v.value for v in item.variant.values.all()]),
                'price': float(item.variant.price) if item.variant.price else None
            }
        
        main_image = item.product.images.filter(is_main=True).first()
        if not main_image:
            main_image = item.product.images.first()
            
        items.append({
            'id': item.id,
            'product_id': item.product.id,
            'product_name': item.product.name,
            'product_slug': item.product.slug,
            'image_url': main_image.image.url if main_image else '',
            'price': float(item.variant.price) if item.variant and item.variant.price else float(item.product.price),
            'quantity': item.quantity,
            'subtotal': float(item.get_subtotal()),
            'variant': variant_data
        })
    
    return {
        'id': cart.id,
        'items': items,
        'total': float(cart.get_total),
        'item_count': cart.get_item_count
    }

@require_http_methods(["GET"])
def api_cart(request):
    cart = _get_or_create_cart(request)
    return JsonResponse(_cart_data(cart))

@csrf_exempt
@require_http_methods(["POST"])
def api_add_to_cart(request):
    cart = _get_or_create_cart(request)
    try:
        data = json.loads(request.body)
        product_id = data.get('product_id')
        selected_values = data.get('selected_values', [])
        quantity = int(data.get('quantity', 1))
        
        product = Product.objects.get(id=product_id)
        
        variant = None
        if selected_values:
            for v in product.variants.all():
                v_values = list(v.values.values_list('value', flat=True))
                if set(v_values) == set(selected_values):
                    variant = v
                    break
        
        cart_item, created = CartItem.objects.get_or_create(
            cart=cart,
            product=product,
            variant=variant,
            defaults={'quantity': quantity}
        )
        
        if not created:
            cart_item.quantity += quantity
            cart_item.save()
            
        return JsonResponse({'success': True, 'cart': _cart_data(cart)})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=400)

@csrf_exempt
@require_http_methods(["POST"])
def api_update_cart_item(request):
    cart = _get_or_create_cart(request)
    try:
        data = json.loads(request.body)
        item_id = data.get('item_id')
        quantity = int(data.get('quantity', 1))
        
        cart_item = CartItem.objects.get(id=item_id, cart=cart)
        if quantity > 0:
            cart_item.quantity = quantity
            cart_item.save()
        else:
            cart_item.delete()
            
        return JsonResponse({'success': True, 'cart': _cart_data(cart)})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=400)

@csrf_exempt
@require_http_methods(["POST"])
def api_remove_from_cart(request):
    cart = _get_or_create_cart(request)
    try:
        data = json.loads(request.body)
        item_id = data.get('item_id')
        
        CartItem.objects.filter(id=item_id, cart=cart).delete()
            
        return JsonResponse({'success': True, 'cart': _cart_data(cart)})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=400)
