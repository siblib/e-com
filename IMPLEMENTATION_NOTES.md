# Implementation Notes: Dynamic Brand Carousel

## Overview
Replaced the hardcoded "Shoes by classics" brand carousel with a fully dynamic,
store-filtered brand system. Brands are now managed from the Django Admin and the
carousel renders only brands belonging to the currently active store that have at
least one active product.

---

## Files Changed

| File | Change |
|---|---|
| `shop/models/products.py` | Added `Brand` model; added `brand` FK to `Product` |
| `shop/models/__init__.py` | Exported `Brand` from the models package |
| `shop/migrations/0007_brand_product_brand.py` | New migration (depends on `0006_alter_product_is_trending`) |
| `shop/admin.py` | Registered `BrandAdmin` with image preview |
| `shop/views/home.py` | Added `Brand` import; injected `featured_brands` into context |
| `shop/views/products.py` | Added `products_by_brand` view |
| `shop/urls.py` | Added `brands/<slug:brand_slug>/` route |
| `templates/home/index.html` | Replaced 6 hardcoded slides with `{% for brand in featured_brands %}` loop |
| `static/images/placeholder-brand.jpg` | Auto-generated placeholder (440×440 px) |

---

## Key Technical Decisions

### 1. Model Hierarchy
`Brand` is connected by:
- `ForeignKey → Store` (CASCADE): deleting a store cleans up its brands automatically.
- `ForeignKey ← Product` (SET_NULL): products survive brand deletion with `brand=None`.

### 2. Query — No Ghost Brands
```python
Brand.objects.filter(
    store=active_store,
    is_active=True,
    products__is_active=True   # ← only brands with ≥1 live product
).distinct().order_by('name')[:6]
```
`.distinct()` prevents duplicate rows from the reverse FK join.

### 3. Carousel Fallback
`{% empty %}` renders a single placeholder slide so Preline UI's carousel JS
always finds at least one `.active` slide to initialise widths from.

### 4. Placeholder Image
Generated at `static/images/placeholder-brand.jpg` via Pillow. Replace it with any
440×440 image; the template falls back to it whenever `brand.image` is not set.

---

## Admin Setup
1. Go to **Admin → Brands → Add Brand**.
2. Select the correct **Store**, upload an image, tick **Is active**.
3. Assign the brand to products via **Admin → Products** (new "Brand" dropdown).

---

## Migration Command
```bash
python manage.py migrate shop 0007_brand_product_brand
```
*(Already applied — `shop.0007_brand_product_brand... OK`)*
