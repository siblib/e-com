from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify
from django.urls import reverse

# Import the helper function from utils
from shop.utils import product_image_upload_path  # ← Add this line

class Store(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True, blank=True)
    description = models.TextField(blank=True)
    
    def __str__(self): return self.name

class Category(models.Model):
    store = models.ForeignKey('shop.Store', on_delete=models.CASCADE, related_name='categories', null=True, blank=True)
    name = models.CharField(max_length=255, db_index=True)
    slug = models.SlugField(max_length=255, unique=True)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')
    image = models.ImageField(upload_to='categories/', null=True, blank=True)
    is_featured = models.BooleanField(default=False)

    class Meta:
        verbose_name_plural = 'Categories'

    def __str__(self): return f"{self.parent.name} > {self.name}" if self.parent else self.name

class Product(models.Model):
    store = models.ForeignKey('shop.Store', on_delete=models.CASCADE, related_name='products', null=True, blank=True)    
    category = models.ForeignKey(Category, related_name='products', on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    in_stock = models.BooleanField(default=True)
    is_active = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('-created',)

    def __str__(self):
        return self.name

class ProductImage(models.Model):
    product = models.ForeignKey(
        'shop.Product', 
        on_delete=models.CASCADE, 
        related_name='images'
    )
    image = models.ImageField(
        upload_to=product_image_upload_path,  # ← Use the imported function
        max_length=255
    )
    is_primary = models.BooleanField(default=False)
    alt_text = models.CharField(max_length=255, blank=True)  # SEO/accessibility
    display_order = models.PositiveSmallIntegerField(default=0)
    
    class Meta:
        ordering = ['display_order', '-is_primary', 'id']
        verbose_name_plural = "Product Images"
    
    def __str__(self):
        return f"Image for {self.product.name} ({'Primary' if self.is_primary else 'Secondary'})"

class Review(models.Model):
    product = models.ForeignKey('shop.Product', on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    rating = models.PositiveSmallIntegerField(choices=[(i, str(i)) for i in range(1, 6)])
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

class Attribute(models.Model):
    name = models.CharField(max_length=50)
    def __str__(self): return self.name

class ProductVariant(models.Model):
    product = models.ForeignKey('shop.Product', on_delete=models.CASCADE, related_name='variants')
    sku = models.CharField(max_length=100, unique=True)
    price_modifier = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    stock = models.PositiveIntegerField(default=0)
    def __str__(self): return f"{self.product.name} - {self.sku}"

class VariantAttributeValue(models.Model):
    variant = models.ForeignKey('shop.ProductVariant', on_delete=models.CASCADE, related_name='attribute_values')
    attribute = models.ForeignKey('shop.Attribute', on_delete=models.CASCADE)
    value = models.CharField(max_length=50)
    def __str__(self): return f"{self.attribute.name}: {self.value}"
