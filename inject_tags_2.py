import re

def process_html():
    with open('templates/products/product_detail.html', 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Breadcrumbs
    # The first breadcrumb "Men" -> "{{ breadcrumbs.0.name }}"
    content = re.sub(
        r'<a class="vf29a a6bs9 flex items-center n6i5x w4xo0 m74u5 fd43e d05xb r17tr focus:outline-hidden dark:text-neutral-400 dark:hover:bg-neutral-800 dark:focus:bg-neutral-800"\s*href="https://www.preline.co/pro/shop/listing-grid-with-categories.html">\s*Men\s*</a>',
        '''<a class="vf29a a6bs9 flex items-center n6i5x w4xo0 m74u5 fd43e d05xb r17tr focus:outline-hidden dark:text-neutral-400 dark:hover:bg-neutral-800 dark:focus:bg-neutral-800" href="#">{% if breadcrumbs %}{{ breadcrumbs.0.name }}{% else %}Home{% endif %}</a>''',
        content
    )

    # The second breadcrumb "Slippers" -> "{{ product.category.name }}"
    content = re.sub(
        r'<a class="vf29a a6bs9 flex items-center truncate n6i5x w4xo0 truncate m74u5 fd43e d05xb r17tr focus:outline-hidden dark:text-neutral-400 dark:hover:bg-neutral-800 dark:focus:bg-neutral-800"\s*href="https://www.preline.co/pro/shop/listing-grid-with-categories.html">\s*<span class="truncate">Slippers</span>\s*</a>',
        '''<a class="vf29a a6bs9 flex items-center truncate n6i5x w4xo0 truncate m74u5 fd43e d05xb r17tr focus:outline-hidden dark:text-neutral-400 dark:hover:bg-neutral-800 dark:focus:bg-neutral-800" href="#"><span class="truncate">{{ product.category.name }}</span></a>''',
        content
    )

    # The third breadcrumb "Mahabis Classic" -> "{{ product.name }}"
    content = re.sub(
        r'<li\s*class="u4i8k flex items-center truncate cnneu c9jt8 dark:text-neutral-200 w4xo0 truncate">\s*<span class="truncate">Mahabis Classic</span>\s*</li>',
        '''<li class="u4i8k flex items-center truncate cnneu c9jt8 dark:text-neutral-200 w4xo0 truncate"><span class="truncate">{{ product.name }}</span></li>''',
        content
    )

    # 2. Main Image
    # Replace the main preview active slide
    content = re.sub(
        r'<div class="hs-carousel-slide active"[^>]*>\s*<img class="[^"]*"[^>]*src=[^>]*alt="Product Image">\s*</div>',
        '''<div class="hs-carousel-slide active" style="width: 514.391px;">
            <img class="f4yn1 fp3m4 x1s1r pb094 dark:bg-neutral-800" src="{% if main_image %}{{ main_image.image.url }}{% else %}{% static 'images/placeholder.png' %}{% endif %}" alt="{{ product.name }}">
        </div>''',
        content,
        count=1
    )

    # 3. Reviews Count
    content = re.sub(
        r'<span\s*class="rbr78 xs2f2 c9jt8 dark:text-neutral-200">\s*\(99\)\s*</span>',
        '''<span class="rbr78 xs2f2 c9jt8 dark:text-neutral-200">({{ total_reviews }})</span>''',
        content
    )

    with open('templates/products/product_detail.html', 'w', encoding='utf-8') as f:
        f.write(content)

if __name__ == '__main__':
    process_html()
