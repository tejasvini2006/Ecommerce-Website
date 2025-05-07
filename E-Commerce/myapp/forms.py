from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Customer, Shopkeeper, UserProfile

class CustomerSignupForm(UserCreationForm):
    email = forms.EmailField(required=True)
    phone = forms.CharField(max_length=15, required=True)
    address = forms.CharField(widget=forms.Textarea, required=True)
    profile_pic = forms.ImageField(required=False)

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2', 'phone', 'address', 'profile_pic')

    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        if not phone.isdigit():
            raise forms.ValidationError('Phone number must contain only digits.')
        return phone

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
            # Create UserProfile
            UserProfile.objects.create(
                user=user,
                user_type='customer',
                profile_pic=self.cleaned_data.get('profile_pic')
            )
            # Create Customer profile
            Customer.objects.create(
                user=user,
                address=self.cleaned_data.get('address'),
                mobile=self.cleaned_data.get('phone'),
                profile_pic=self.cleaned_data.get('profile_pic')
            )
        return user

class ShopkeeperSignupForm(UserCreationForm):
    shop_name = forms.CharField(max_length=100)
    address = forms.CharField(max_length=200)
    mobile = forms.CharField(max_length=20)
    business_license = forms.CharField(max_length=50, required=False)
    profile_pic = forms.ImageField(required=False)

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2', 
                 'shop_name', 'address', 'mobile', 'business_license', 'profile_pic')

    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()
            # Create UserProfile
            UserProfile.objects.create(
                user=user,
                user_type='shopkeeper',
                profile_pic=self.cleaned_data.get('profile_pic')
            )
            # Create Shopkeeper profile
            Shopkeeper.objects.create(
                user=user,
                shop_name=self.cleaned_data.get('shop_name'),
                address=self.cleaned_data.get('address'),
                mobile=self.cleaned_data.get('mobile'),
                business_license=self.cleaned_data.get('business_license'),
                profile_pic=self.cleaned_data.get('profile_pic')
            )
        return user 