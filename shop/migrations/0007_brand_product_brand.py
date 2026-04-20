# shop/migrations/0007_brand_product_brand.py

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0006_alter_product_is_trending'),  # last existing migration
    ]

    operations = [
        migrations.CreateModel(
            name='Brand',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, unique=True)),
                ('slug', models.SlugField(blank=True, max_length=255, unique=True)),
                ('description', models.TextField(blank=True)),
                ('image', models.ImageField(blank=True, null=True, upload_to='brands/')),
                ('is_active', models.BooleanField(default=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('store', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='brands', to='shop.store')),
            ],
            options={
                'verbose_name_plural': 'Brands',
                'ordering': ['name'],
            },
        ),
        migrations.AddField(
            model_name='product',
            name='brand',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='products', to='shop.brand'),
        ),
    ]
