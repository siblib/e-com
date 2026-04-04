import os
import django
from django.core.files import File
from django.utils.text import slugify

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ecommerce.settings')
django.setup()

from shop.models.products import Product, Category, Store, ProductImage

def run_upload():
    # 1. Ensure we have a Store and Category to link to
    store, _ = Store.objects.get_or_create(name="Main Store", slug="main-store")
    category, _ = Category.objects.get_or_create(name="General", slug="general", store=store)

    image_dir = os.path.join('static', 'images')
    
    # Supported image extensions
    valid_extensions = ('.webp', '.jpg', '.jpeg', '.png')

    for filename in os.listdir(image_dir):
        if filename.lower().endswith(valid_extensions):
            product_name = filename.split('.')[0].replace('-', ' ').title()
            product_slug = slugify(product_name)

            # 2. Create the Product
            product, created = Product.objects.get_or_create(
                name=product_name,
                slug=product_slug,
                defaults={
                    'category': category,
                    'store': store,
                    'price': 100.00, # Placeholder price
                    'description': f"Automated upload for {product_name}"
                }
            )

            if created:
                # 3. Create the ProductImage entry
                # This triggers your custom product_image_upload_path in utils.py
                path_to_image = os.path.join(image_dir, filename)
                with open(path_to_image, 'rb') as f:
                    product_image = ProductImage(
                        product=product,
                        is_primary=True,
                        alt_text=product_name
                    )
                    product_image.image.save(filename, File(f), save=True)
                
                print(f"Successfully added: {product_name}")

if __name__ == "__main__":
    run_upload()
