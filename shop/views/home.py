from django.shortcuts import render
from shop.models.products import Product, Category, Store
from shop.utils import get_category_descendants

def index(request):
    # 1. Fetch top-level categories for navigation
    electronics_categories = Category.objects.filter(
        store__name="Main Store",
        parent__isnull=True
    )
    
    # 2. Dynamic Trending Tabs Logic
    electronics_store = Store.objects.filter(name="Main Store").first()
    trending_tabs = []
    trending_products_by_tab = {}

    if electronics_store:
        # Get the root category for this store
        # Assuming the root is a category with no parent in this store
        store_root = Category.objects.filter(store=electronics_store, parent__isnull=True).first()

        if store_root:
            featured_children = Category.objects.filter(
                parent=store_root,
                is_featured=True
            )

            # Determine which categories to show as tabs
            resolved_categories = []
            if not featured_children.exists():
                resolved_categories = [store_root]
            elif featured_children.count() == 1:
                resolved_categories = [store_root, featured_children.first()]
            else:
                resolved_categories = list(featured_children)

            # Prepare tabs and products
            for cat in resolved_categories:
                is_default = (cat == resolved_categories[0])
                tab_id = cat.slug.replace('-', '_')

                # Use helper to get all descendants for filtering
                descendants = get_category_descendants(cat, include_self=True)

                products = Product.objects.filter(
                    is_trending=True,
                    is_active=True,
                    category__in=descendants
                ).select_related('category', 'store').prefetch_related('images')[:10]

                trending_tabs.append({
                    "id": tab_id,
                    "name": "All Electronics" if cat == store_root else cat.name,
                    "slug": cat.slug,
                    "is_default": is_default,
                    "products": products
                })

    context = {
        'categories': electronics_categories,
        'trending_tabs': trending_tabs,
    }
    
    return render(request, 'home/index.html', context)