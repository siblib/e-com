from django.shortcuts import render
from shop.models.products import Product

def index(request):
    trending_products = Product.objects.filter(is_trending=True, is_active=True).prefetch_related('images', 'category')[:10]
    context = {
        'trending_products': trending_products,
    }
    return render(request, 'home/index.html', context)
