# shop/utils.py or shop/helpers.py
import os
from django.utils.text import slugify

# In shop/utils.py - enhanced version
def product_image_upload_path(instance, filename):
    import uuid
    from django.utils.text import slugify
    
    # Safe attribute access
    product = getattr(instance, 'product', None)
    if not product:
        return f"products/temp/{filename}"
    
    store = getattr(product, 'store', None)
    store_slug = slugify(getattr(store, 'slug', None) or getattr(store, 'name', 'unknown'))
    
    # Build category path
    category_parts = []
    current_cat = getattr(product, 'category', None)
    while current_cat:
        cat_slug = slugify(getattr(current_cat, 'slug', None) or getattr(current_cat, 'name', 'uncategorized'))
        category_parts.insert(0, cat_slug)
        current_cat = getattr(current_cat, 'parent', None)
    category_path = '/'.join(category_parts) if category_parts else 'uncategorized'
    
    product_slug = slugify(
        getattr(product, 'slug', None) or 
        getattr(product, 'name', 'unnamed')
    )
    
    # Use UUID for unsaved instances to guarantee uniqueness
    ext = os.path.splitext(filename)[1].lower()
    product_id = getattr(product, 'id', None) or 'new'
    unique_id = getattr(instance, 'pk', None) or uuid.uuid4().hex[:8]
    unique_filename = f"{product_id}_{unique_id}{ext}"
    
    return f"products/{store_slug}/{category_path}/{product_slug}/{unique_filename}"

# === TRENDING CATEGORY HELPERS ===
def get_category_descendant_ids(category):
    """
    Recursively collect IDs of a category and all its descendants.
    Works with simple parent ForeignKey hierarchy (no MPTT).
    
    Usage:
        ids = get_category_descendant_ids(accessories_category)
        Product.objects.filter(category_id__in=ids)
    """
    # Local import to avoid circular refs
    from shop.models.products import Category
    
    ids = [category.id]
    children = Category.objects.filter(parent=category)
    for child in children:
        ids.extend(get_category_descendant_ids(child))
    return ids