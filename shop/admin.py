from django.contrib import admin
from .models.products import Product, Category, ProductImage, Store

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
