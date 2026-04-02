# shop/views/products.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.utils.text import slugify
from typing import Dict, Any

# Import models from the modular structure
from shop.models import Product, Store, Category, ProductImage  # ← This works due to __init__.py

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
    """Product grid that includes visible category navigation or grouping."""
    context: Dict[str, Any] = {}
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


