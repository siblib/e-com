from django.shortcuts import render
from shop.models.products import Product, Category, Store
from shop.utils import get_category_descendant_ids

def index(request):
    # 1. STORE SWITCHING LOGIC (Safely defaults to Electronics)
    store_slug = request.GET.get('store') or request.session.get('active_store', 'electronics')
    
    active_store = Store.objects.filter(slug=store_slug).first()
    if not active_store:
        active_store = Store.objects.filter(name__iexact=store_slug).first() or \
                       Store.objects.filter(slug='electronics').first() or \
                       Store.objects.first()
        if active_store:
            store_slug = active_store.slug
            
    request.session['active_store'] = store_slug

    # 2. TOP LEVEL CATEGORIES (Now dynamic instead of hardcoded "Electronics")
    categories = Category.objects.filter(
        store=active_store, 
        parent__isnull=True
    )
    
    # 3. TRENDING CATEGORIES (Dynamic by Active Store)
    trending_categories = Category.objects.filter(
        store=active_store,
        is_featured=True
    ).order_by('id')[:2]
    
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
    else:
        # NEW SAFEGUARD: If a store has 0 featured categories, just show an All Items tab
        tab_config = [
            {'label': 'All Items', 'slug': None, 'type': 'store', 'exclude_category_id': None},
        ]

    tab_data = []
    for tab in tab_config:
        if tab['type'] == 'category':
            category = Category.objects.get(slug=tab['slug'])
            category_ids = get_category_descendant_ids(category)
            
            products = Product.objects.filter(
                category_id__in=category_ids,
                is_active=True,
                is_trending=True
            ).prefetch_related('images', 'category').order_by('-created')[:12]
            
        else:  # All Items tab
            if tab.get('exclude_category_id'):
                trending_category = Category.objects.get(id=tab['exclude_category_id'])
                exclude_ids = get_category_descendant_ids(trending_category)
                
                products = Product.objects.exclude(
                    category_id__in=exclude_ids
                ).filter(
                    category__store=active_store,  # ← THE SECRET FIX: Filters by category's store
                    is_active=True,
                    is_trending=True
                ).prefetch_related('images', 'category').order_by('-created')[:12]
            else:
                # Runs only if 0 trending categories exist
                products = Product.objects.filter(
                    category__store=active_store,  # ← THE SECRET FIX
                    is_active=True,
                    is_trending=True
                ).prefetch_related('images', 'category').order_by('-created')[:12]
            
        tab_data.append({**tab, 'products': products})

    # 4. TRENDING PRODUCTS FALLBACK (Bottom of page)
    trending_products = Product.objects.filter(
        category__store=active_store,  # ← THE SECRET FIX
        is_trending=True, 
        is_active=True
    ).prefetch_related('images', 'category')[:10]

    # 5. CONTEXT
    context = {
        'categories': categories, # Matches your template `{% for category in categories %}`
        'tab_config': tab_data,
        'trending_products': trending_products,
        'active_store': active_store,
    }
    
    return render(request, 'home/index.html', context)