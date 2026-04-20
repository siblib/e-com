# shop/views/products.py
from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.utils.text import slugify
from typing import Dict, Any

# Import models from the modular structure
from shop.models import Product, Store, Category, ProductImage  # ← This works due to __init__.py
from shop.models.products import Brand
from shop.utils import get_category_descendant_ids

# ... rest of your view code ...

# ======================
# Category Views
# ======================

def categories(request):
    """Display main category listing without sidebar."""
    context: Dict[str, Any] = {}
    return render(request, 'products/categories.html', context)

def categories_sidebar(request):
    """Display category listing with a persistent sidebar."""
    context: Dict[str, Any] = {}
    return render(request, 'products/categories_sidebar.html', context)


# ======================
# Product Grid Views
# ======================

def grid(request):
    """Basic product grid layout."""
    context: Dict[str, Any] = {}
    return render(request, 'products/grid.html', context)

def grid_sidebar(request):
    """Product grid with a sidebar (e.g., filters or navigation)."""
    context: Dict[str, Any] = {}
    return render(request, 'products/grid_sidebar.html', context)

def grid_hero(request):
    """Product grid with a prominent hero/banner section above."""
    context: Dict[str, Any] = {}
    return render(request, 'products/grid_hero.html', context)

def grid_with_categories(request):
    """Product grid with child-category/brand carousel, filters, sorting, and pagination."""
    category_slug = request.GET.get('category')
    store_slug = request.session.get('active_store', 'electronics')

    # 1. Identify the active category
    if category_slug:
        active_category = get_object_or_404(Category, slug=category_slug)
    else:
        # Fallback to the first top-level category of the active store
        active_category = Category.objects.filter(store__slug=store_slug, parent__isnull=True).first()

    # 2. Get immediate child categories for the top slider
    child_categories = Category.objects.filter(parent=active_category) if active_category else []

    # 3. Get all descendant category IDs to fetch associated products and brands
    category_ids = get_category_descendant_ids(active_category) if active_category else []

    # 4. Fetch relevant brands logically connected to this category structure
    brands = Brand.objects.filter(products__category_id__in=category_ids, is_active=True).distinct()

    # 5. Base QuerySet for products
    products_qs = Product.objects.filter(
        category_id__in=category_ids,
        is_active=True
    ).prefetch_related('images', 'category', 'brand')

    # 6. Apply Active Filters (Brands)
    selected_brands = request.GET.getlist('brand')
    if selected_brands:
        products_qs = products_qs.filter(brand__slug__in=selected_brands)

    # Optional dynamic filters passed directly from UI inputs
    selected_colors = request.GET.getlist('color')
    selected_sizes = request.GET.getlist('size')

    # 7. Apply Sorting
    sort_by = request.GET.get('sort', 'trending')
    if sort_by == 'price-low-to-high':
        products_qs = products_qs.order_by('price')
    elif sort_by == 'price-high-to-low':
        products_qs = products_qs.order_by('-price')
    elif sort_by == 'bestseller':
        products_qs = products_qs.order_by('-id')  # Fallback sorting for bestseller
    elif sort_by == 'trending':
        products_qs = products_qs.order_by('-is_trending', '-created')
    else:
        products_qs = products_qs.order_by('-created')

    total_products = products_qs.count()

    # 8. Pagination logic
    page_number = request.GET.get('page', 1)
    paginator = Paginator(products_qs, 12)  # 12 items per page
    page_obj = paginator.get_page(page_number)

    context: Dict[str, Any] = {
        'active_category': active_category,
        'child_categories': child_categories,
        'brands': brands,
        'products': page_obj,
        'total_products': total_products,
        'selected_brands': selected_brands,
        'selected_colors': selected_colors,
        'selected_sizes': selected_sizes,
        'sort_by': sort_by,
    }

    return render(request, 'products/grid_with_categories.html', context)

def grid_mini_categories(request):
    """Product grid with compact/minimalist category indicators."""
    context: Dict[str, Any] = {}
    return render(request, 'products/grid_mini_categories.html', context)

# ======================
# Product Detail View
# ======================

def product_detail(request, product_id: int):
    """Display detailed information for a specific product."""
    context: Dict[str, Any] = {
        'product_id': product_id,
    }
    return render(request, 'products/product_detail.html', context)

def product_sticky_sidebar(request, product_id: int):
    """Product detail page featuring a sticky info sidebar on scroll."""
    context: Dict[str, Any] = {
        'product_id': product_id,
    }
    return render(request, 'products/product_sticky_sidebar.html', context)

def product_gallery_slider(request, product_id: int):
    """Product detail page featuring a thumbnail image slider."""
    context: Dict[str, Any] = {
        'product_id': product_id,
    }
    return render(request, 'products/product_gallery_slider.html', context)

# ======================
# Product Interaction Views
# ======================

def compare(request):
    """Page to compare selected products (IDs typically passed via GET/POST)."""
    context: Dict[str, Any] = {}
    return render(request, 'products/compare.html', context)

def write_review(request, product_id: int):
    """Form page to submit a review for a specific product."""
    context: Dict[str, Any] = {
        'product_id': product_id,
    }
    return render(request, 'products/write_review.html', context)


# ======================
# Brand Views
# ======================

def products_by_brand(request, brand_slug: str):
    """
    Renders a grid of products belonging to the selected brand,
    scoped to the currently active store from the session.
    """
    brand = get_object_or_404(Brand, slug=brand_slug, is_active=True)
    store_slug = request.GET.get('store') or request.session.get('active_store', 'electronics')

    product_list = Product.objects.filter(
        brand=brand,
        brand__store__slug=store_slug,
        is_active=True,
    ).prefetch_related('images')

    context: Dict[str, Any] = {
        'brand': brand,
        'products': product_list,
    }
    return render(request, 'products/grid.html', context)
