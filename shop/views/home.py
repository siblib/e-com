from django.shortcuts import render
from shop.models.products import Product, Category
from shop.utils import get_category_descendant_ids  # ← ADD THIS IMPORT

def index(request):
    # 1. Fetch top-level categories that specifically belong to the "Electronics" store.
    electronics_categories = Category.objects.filter(
        store__name="Electronics", 
        parent__isnull=True
    )
    
    # Fetch up to 2 trending categories deterministically (by ID)
    # Your model uses is_featured (not is_trending) for categories
    trending_categories = Category.objects.filter(is_featured=True).order_by('id')[:2]
    
    tab_config = []
    if len(trending_categories) >= 2:
        tab_config = [
            {'label': trending_categories[0].name, 'slug': trending_categories[0].slug, 'type': 'category', 'exclude': False},
            {'label': trending_categories[1].name, 'slug': trending_categories[1].slug, 'type': 'category', 'exclude': False},
        ]
    elif len(trending_categories) == 1:
        tab_config = [
            {'label': trending_categories[0].name, 'slug': trending_categories[0].slug, 'type': 'category', 'exclude': False},
            {'label': 'All Items', 'slug': None, 'type': 'store', 'exclude_category_id': trending_categories[0].id},
        ]

    tab_data = []
    for tab in tab_config:
        if tab['type'] == 'category':
            # === FIX START: Include descendant categories ===
            category = Category.objects.get(slug=tab['slug'])
            category_ids = get_category_descendant_ids(category)
            
            products = Product.objects.filter(
                category_id__in=category_ids,  # ← CHANGED: was category__slug=tab['slug']
                is_active=True,
                is_trending=True  # ← Keep this to show only products marked as trending
            ).prefetch_related('images', 'category').order_by('-created')[:12]
            # === FIX END ===
            
        else:  # tab['type'] == 'store' (Main Store with exclusion)
            # === FIX START: Exclude descendant categories ===
            trending_category = Category.objects.get(id=tab['exclude_category_id'])
            exclude_ids = get_category_descendant_ids(trending_category)
            
            products = Product.objects.exclude(
                category_id__in=exclude_ids  # ← CHANGED: was category_id=tab['exclude_category_id']
            ).filter(
                is_active=True,
                is_trending=True  # ← Keep this for consistency
            ).prefetch_related('images', 'category').order_by('-created')[:12]
            # === FIX END ===
            
        tab_data.append({**tab, 'products': products})

    # 2. Your original trending products query (Fallback if 0 trending categories)
    trending_products = Product.objects.filter(
        is_trending=True, 
        is_active=True
    ).prefetch_related('images', 'category')[:10]

    # 3. Pass variables to the template context
    context = {
        'categories': electronics_categories,
        'tab_config': tab_data,
        'trending_products': trending_products,
    }
    
    return render(request, 'home/index.html', context)