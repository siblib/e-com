from django.shortcuts import render
from shop.models.products import Product, Category, Store, Brand
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

    # 1.5. DYNAMIC BRANDS BY STORE
    featured_brands = Brand.objects.filter(
        store=active_store,
        is_active=True,
        products__is_active=True
    ).distinct().order_by('name')[:6]

    # 2. TOP LEVEL CATEGORIES 
    categories = Category.objects.filter(
        store=active_store, 
        parent__isnull=True
    )

    # ---------------------------------------------------------------------
    # 2.5 TOP CATEGORIES BY PRODUCT COUNT (For the Categories Section)
    # ---------------------------------------------------------------------
    all_store_categories = Category.objects.filter(store=active_store)
    cat_counts = []
    
    # Calculate total products in each category (including subcategories)
    for cat in all_store_categories:
        cat_ids = get_category_descendant_ids(cat)
        count = Product.objects.filter(category_id__in=cat_ids, is_active=True).count()
        cat_counts.append((cat, count))
    
    # Sort by product count descending, pick the top 3
    cat_counts.sort(key=lambda x: x[1], reverse=True)
    top_categories = [x[0] for x in cat_counts[:3]]

    top_categories_data = []
    
    # Original placeholders to be used if a category doesn't have 3 product images
    default_placeholders = [
        [
            "images/photo-1699595749116-33a4a869503c(1)",
            "images/photo-1699593022913-7068606059c8",
            "images/photo-1600185365483-26d7a4cc7519"
        ],
        [
            "images/photo-1708443683276-8a3eb30faef2(1)",
            "images/photo-1627225924765-552d49cf47ad",
            "images/photo-1708443683198-a2b77a54c36e(1)"
        ],
        [
            "images/photo-1654512697735-d7ff21350443",
            "images/photo-1585487000160-6ebcfceb0d03",
            "images/photo-1593164842264-854604db2260(1)"
        ]
    ]

    for idx, cat in enumerate(top_categories):
        cat_ids = get_category_descendant_ids(cat)
        cat_products = Product.objects.filter(
            category_id__in=cat_ids, 
            is_active=True
        ).prefetch_related('images')
        
        # Safely determine the starting price
        starting_price = 0
        try:
            first_product = cat_products.order_by('price').first()
            if first_product and hasattr(first_product, 'price'):
                starting_price = first_product.price
            elif first_product and hasattr(first_product, 'regular_price'):
                starting_price = first_product.regular_price
        except Exception:
            # Safe fallback in case "price" field is named differently
            valid_prices = []
            for p in cat_products[:20]:
                if hasattr(p, 'price') and p.price is not None:
                    valid_prices.append(p.price)
                elif hasattr(p, 'regular_price') and p.regular_price is not None:
                    valid_prices.append(p.regular_price)
            if valid_prices:
                starting_price = min(valid_prices)

        # Gather up to 3 distinct product images from the category
        cat_images = []
        for prod in cat_products:
            first_img = prod.images.first()
            if first_img and hasattr(first_img, 'image') and first_img.image:
                cat_images.append(first_img.image.url)
            if len(cat_images) >= 3:
                break
                
        # Pad remaining required images with the original HTML placeholders
        placeholders = default_placeholders[idx] if idx < len(default_placeholders) else default_placeholders[0]
        final_images = []
        
        for i in range(3):
            if i < len(cat_images):
                final_images.append({'url': cat_images[i], 'is_static': False})
            else:
                final_images.append({'url': placeholders[i], 'is_static': True})

        top_categories_data.append({
            'category': cat,
            'starting_price': starting_price,
            'images': final_images,
        })
    # ---------------------------------------------------------------------

    # 3. TRENDING CATEGORIES
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
        # SAFEGUARD
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
                    category__store=active_store,
                    is_active=True,
                    is_trending=True
                ).prefetch_related('images', 'category').order_by('-created')[:12]
            else:
                products = Product.objects.filter(
                    category__store=active_store,
                    is_active=True,
                    is_trending=True
                ).prefetch_related('images', 'category').order_by('-created')[:12]
            
        tab_data.append({**tab, 'products': products})

    # 4. TRENDING PRODUCTS FALLBACK (Bottom of page)
    trending_products = Product.objects.filter(
        category__store=active_store,
        is_trending=True, 
        is_active=True
    ).prefetch_related('images', 'category')[:10]

    # 5. CONTEXT
    context = {
        'categories': categories,
        'tab_config': tab_data,
        'top_categories_data': top_categories_data,  # NEW: Categories specific data
        'trending_products': trending_products,
        'active_store': active_store,
        'featured_brands': featured_brands,
    }
    
    return render(request, 'home/index.html', context)