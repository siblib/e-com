import os
import django
from django.conf import settings
from django.template import Engine

settings.configure(
    TEMPLATES=[{
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(os.getcwd(), 'templates')],
        'APP_DIRS': True,
    }]
)
django.setup()

template_path = "templates/home/index.html"
engine = Engine.get_default()

try:
    with open(template_path) as f:
        engine.from_string(f.read())
    print("✓ Template syntax valid")
except Exception as e:
    print(f"✗ Template error: {e}")
