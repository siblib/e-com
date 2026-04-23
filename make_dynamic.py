import re

with open('main_part.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Replace category text
content = re.sub(
    r'<p class="rwumq w4xo0 jy5gh dark:text-neutral-500">\s*Men\'s Slippers\s*</p>',
    '<p class="rwumq w4xo0 jy5gh dark:text-neutral-500">{{ product.category.name|default:"General" }}</p>',
    content
)

# Replace product name
content = re.sub(
    r'<h1 class="cnneu a3jay c9jt8 dark:text-neutral-200">\s*Mahabis Classic\s*</h1>',
    '<h1 class="cnneu a3jay c9jt8 dark:text-neutral-200">{{ product.name }}</h1>',
    content
)

# Replace price
content = re.sub(
    r'<p class="rwavo sikx1 tbkeq c9jt8 dark:text-neutral-200">\s*\$40\s*</p>',
    '<p class="rwavo sikx1 tbkeq c9jt8 dark:text-neutral-200">${{ product.price }}</p>',
    content
)

# To wrap the main content in block content
final_content = "{% extends 'base.html' %}\n{% load static %}\n\n{% block content %}\n" + content + "\n{% endblock %}"

with open('templates/products/product_detail.html', 'w', encoding='utf-8') as f:
    f.write(final_content)

print("Dynamic replacements applied.")
