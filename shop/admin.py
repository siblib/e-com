from django.contrib import admin
from django.utils.html import mark_safe
from .models.products import Product, Category, ProductImage, Store, Brand

# 1. This allows you to add images directly inside the Product page
class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1 # Shows one empty slot for a new image by default
    fields = ['image', 'is_primary', 'display_order']

@admin.register(Store)
class StoreAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'parent', 'is_featured']
    list_filter = ['is_featured', 'store']
    prepopulated_fields = {'slug': ('name',)}

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'price', 'in_stock', 'is_active', 'is_trending', 'created']
    list_filter = ['in_stock', 'is_active', 'is_trending', 'category', 'store']
    list_editable = ['price', 'in_stock', 'is_active', 'is_trending']
    prepopulated_fields = {'slug': ('name',)}
    
    # 2. Add the images section to the bottom of the Product edit page
    inlines = [ProductImageInline]


@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'store', 'is_active', 'image_preview')
    search_fields = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}
    list_filter = ('store', 'is_active')

    def image_preview(self, obj):
        if obj.image:
            return mark_safe(
                f'<img src="{obj.image.url}" width="50" height="50" '
                f'style="object-fit:cover; border-radius:4px;" alt="{obj.name}" />'
            )
        return 'No Image'
    image_preview.short_description = 'Image Preview'
