from django.shortcuts import render
from shop.models.products import Product, Category

def index(request):
    trending_products = Product.objects.filter(is_trending=True, is_active=True).prefetch_related('images', 'category')[:10]
    main_categories = Category.objects.filter(parent__isnull=True)
    context = {
        'trending_products': trending_products,
        'categories': main_categories,
    }
    return render(request, 'home/index.html', context)
