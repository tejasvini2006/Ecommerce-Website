from django.core.management.base import BaseCommand
from django.core.files import File
from django.conf import settings
import os
import requests
from myapp.models import Product, Category
from django.core.files.temp import NamedTemporaryFile

class Command(BaseCommand):
    help = 'Adds sample products with images to the database'

    def handle(self, *args, **kwargs):
        # Create categories if they don't exist
        categories = {
            'Electronics': 'Latest gadgets and electronic devices',
            'Clothing': 'Fashion items and accessories',
            'Books': 'Physical and digital books',
            'Home': 'Home decor and furniture'
        }

        for name, description in categories.items():
            category, created = Category.objects.get_or_create(
                name=name,
                defaults={'description': description}
            )
            if created:
                self.stdout.write(f'Created category: {name}')

        # Sample products with images
        products = [
            {
                'name': 'Smartphone X',
                'category': 'Electronics',
                'description': 'Latest smartphone with advanced features',
                'price': 999.99,
                'sale_price': 899.99,
                'stock': 50,
                'size': 'M',
                'color': 'Black',
                'material': 'Metal and Glass',
                'image_url': 'https://images.unsplash.com/photo-1511707171634-5f897ff02aa9?w=800&h=800&fit=crop',
                'is_featured': True
            },
            {
                'name': 'Classic T-Shirt',
                'category': 'Clothing',
                'description': 'Comfortable cotton t-shirt',
                'price': 29.99,
                'stock': 100,
                'size': 'M',
                'color': 'White',
                'material': 'Cotton',
                'image_url': 'https://images.unsplash.com/photo-1521572163474-6864f9cf17ab?w=800&h=800&fit=crop',
                'is_featured': True
            },
            {
                'name': 'Programming Guide',
                'category': 'Books',
                'description': 'Comprehensive programming guide',
                'price': 49.99,
                'sale_price': 39.99,
                'stock': 30,
                'size': 'M',
                'color': 'Blue',
                'material': 'Paper',
                'image_url': 'https://images.unsplash.com/photo-1507842217343-583bb7270b66?w=800&h=800&fit=crop',
                'is_featured': True
            },
            {
                'name': 'Modern Sofa',
                'category': 'Home',
                'description': 'Comfortable modern sofa',
                'price': 799.99,
                'stock': 15,
                'size': 'L',
                'color': 'Gray',
                'material': 'Fabric',
                'image_url': 'https://images.unsplash.com/photo-1555041469-a586c61ea9bc?w=800&h=800&fit=crop',
                'is_featured': True
            }
        ]

        for product_data in products:
            # Get the category
            category = Category.objects.get(name=product_data['category'])
            
            # Download and save the image
            response = requests.get(product_data['image_url'])
            if response.status_code == 200:
                img_temp = NamedTemporaryFile()
                img_temp.write(response.content)
                img_temp.flush()
                
                # Create the product
                product = Product.objects.create(
                    name=product_data['name'],
                    category=category,
                    description=product_data['description'],
                    price=product_data['price'],
                    sale_price=product_data.get('sale_price'),
                    stock=product_data['stock'],
                    size=product_data['size'],
                    color=product_data['color'],
                    material=product_data['material'],
                    is_featured=product_data.get('is_featured', False)
                )
                
                # Save the image
                product.product_image.save(
                    f"{product_data['name'].lower().replace(' ', '_')}.jpg",
                    File(img_temp),
                    save=True
                )
                
                self.stdout.write(f'Created product: {product_data["name"]}')
            else:
                self.stdout.write(f'Failed to download image for: {product_data["name"]}')

        self.stdout.write(self.style.SUCCESS('Successfully added sample products')) 