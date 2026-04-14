from django.shortcuts import render
from shop.models.products import Product, Category

def index(request):
    # 1. Fetch top-level categories that specifically belong to the "Electronics" store.
    # (If your store name field is named differently, e.g., 'title', change 'store__name' to 'store__title')
    electronics_categories = Category.objects.filter(
        store__name="Electronics", 
        parent__isnull=True
    )
    
    # 2. Your original trending products query
    trending_products = Product.objects.filter(
        is_trending=True, 
        is_active=True
    ).prefetch_related('images', 'category')[:10]

    # 3. Pass both variables to the template context
    context = {
        'categories': electronics_categories,
        'trending_products': trending_products,
    }
    
    return render(request, 'home/index.html', context)