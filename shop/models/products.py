from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator

class Store(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name

class Category(models.Model):
    store = models.ForeignKey(Store, related_name='categories', on_delete=models.CASCADE, null=True, blank=True)
    parent = models.ForeignKey('self', related_name='children', on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    image = models.ImageField(upload_to='categories/', null=True, blank=True)

    class Meta:
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name

class Brand(models.Model):
    store = models.ForeignKey(Store, related_name='brands', on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

class Product(models.Model):
    category = models.ForeignKey(Category, related_name='products', on_delete=models.CASCADE)
    brand = models.ForeignKey(Brand, related_name='products', on_delete=models.SET_NULL, null=True, blank=True)
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    description = models.TextField(blank=True)
    
    price = models.DecimalField(max_digits=10, decimal_places=2)
    old_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    
    is_active = models.BooleanField(default=True)
    is_trending = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    
    # Stock tracking
    stock = models.IntegerField(default=0)
    low_stock_threshold = models.IntegerField(default=5)
    
    # Additional expandable info for accordions
    size_fit_details = models.TextField(blank=True, null=True, help_text="Details regarding sizing and fit.")
    shipping_returns_details = models.TextField(blank=True, null=True, help_text="Details about shipping and return policies.")
    
    # Relationships for 'Goes well with' and 'You may also like'
    complementary_products = models.ManyToManyField('self', blank=True, symmetrical=False, related_name='complemented_by')
    related_products = models.ManyToManyField('self', blank=True, symmetrical=False, related_name='related_to')

    def __str__(self):
        return self.name

class ProductImage(models.Model):
    product = models.ForeignKey(Product, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='products/')
    alt_text = models.CharField(max_length=255, blank=True, null=True)
    is_main = models.BooleanField(default=False)

    class Meta:
        ordering = ['-is_main', 'id']

class ProductAttribute(models.Model):
    """
    Flexible attribute system to handle properties like Color, Size, Screen Size, RAM, etc.
    """
    product = models.ForeignKey(Product, related_name='attributes', on_delete=models.CASCADE)
    name = models.CharField(max_length=50, help_text="e.g., Color, Size, RAM")
    value = models.CharField(max_length=50, help_text="e.g., Red, XL, 16GB")

    def __str__(self):
        return f"{self.product.name} - {self.name}: {self.value}"

class Review(models.Model):
    product = models.ForeignKey(Product, related_name='reviews', on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    rating = models.PositiveIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)], default=5)
    title = models.CharField(max_length=255, blank=True)
    content = models.TextField()
    helpful_votes = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Review for {self.product.name}"
