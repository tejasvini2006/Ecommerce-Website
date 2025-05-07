from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('signup/', views.signup, name='signup'),
    path('shopkeeper/dashboard/', views.shopkeeper_dashboard, name='shopkeeper_dashboard'),
    path('customer/dashboard/', views.customer_dashboard, name='customer_dashboard'),
    path('home/', views.home, name='home'),
    
    # Product URLs
    path('products/', views.product_list, name='product_list'),
    path('product/<int:product_id>/', views.product_detail, name='product_detail'),
    path('product/<int:product_id>/add-to-cart/', views.add_to_cart, name='add_to_cart'),
    path('product/<int:product_id>/feedback/', views.add_feedback, name='add_feedback'),
    
    # Cart URLs
    path('cart/', views.cart, name='cart'),
    path('cart/update/<int:cart_item_id>/', views.update_cart, name='update_cart'),
    path('cart/remove/<int:cart_item_id>/', views.remove_from_cart, name='remove_from_cart'),
    
    # Order URLs
    path('checkout/', views.checkout, name='checkout'),
    path('order/confirmation/<int:order_id>/', views.order_confirmation, name='order_confirmation'),
    path('orders/', views.order_history, name='order_history'),
    
    # Shopkeeper URLs
    path('shopkeeper/products/add/', views.add_product, name='add_product'),
    path('shopkeeper/products/<int:product_id>/edit/', views.edit_product, name='edit_product'),
    path('shopkeeper/products/<int:product_id>/delete/', views.delete_product, name='delete_product'),
    path('shopkeeper/orders/', views.all_orders, name='all_orders'),
    path('shopkeeper/orders/<int:order_id>/', views.order_detail, name='order_detail'),
    path('shopkeeper/orders/<int:order_id>/update-status/', views.update_order_status, name='update_order_status'),
] 