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


def get_category_descendants(category, include_self=True):
    """
    Finds all descendant categories for a given category using a single query
    to fetch all categories in the store to avoid N+1 queries.
    """
    from shop.models.products import Category

    # Fetch all categories in the same store once
    all_categories = list(Category.objects.filter(store=category.store))

    def build_descendants(parent_id):
        desc = []
        children = [c for c in all_categories if c.parent_id == parent_id]
        for child in children:
            desc.append(child)
            desc.extend(build_descendants(child.id))
        return desc

    descendants = []
    if include_self:
        descendants.append(category)

    descendants.extend(build_descendants(category.id))
    return descendants
