from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from myapp.models import UserProfile, Shopkeeper

class Command(BaseCommand):
    help = 'Sets up the predefined shopkeeper account'

    def handle(self, *args, **kwargs):
        # Create shopkeeper user
        shopkeeper, created = User.objects.get_or_create(
            username='shopkeeper',
            defaults={
                'first_name': 'Shop',
                'last_name': 'Keeper',
                'email': 'shopkeeper@example.com',
                'is_staff': True
            }
        )
        
        if created:
            shopkeeper.set_password('shopkeeper123')
            shopkeeper.save()
            self.stdout.write('Created shopkeeper user')
        else:
            self.stdout.write('Shopkeeper user already exists')

        # Create UserProfile
        user_profile, created = UserProfile.objects.get_or_create(
            user=shopkeeper,
            defaults={'user_type': 'shopkeeper'}
        )
        if created:
            self.stdout.write('Created shopkeeper user profile')
        else:
            self.stdout.write('Shopkeeper user profile already exists')

        # Create Shopkeeper profile
        shopkeeper_profile, created = Shopkeeper.objects.get_or_create(
            user=shopkeeper,
            defaults={
                'shop_name': 'My Shop',
                'address': 'Shop Address',
                'mobile': '1234567890',
                'is_verified': True
            }
        )
        if created:
            self.stdout.write('Created shopkeeper profile')
        else:
            self.stdout.write('Shopkeeper profile already exists')

        self.stdout.write(self.style.SUCCESS('Successfully set up shopkeeper account')) 