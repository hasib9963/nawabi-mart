from django.urls import path
from . import views

urlpatterns = [
    path('add/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('', views.view_cart, name='cart'),
    path('remove/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),  # New URL pattern
    path('update/', views.update_cart, name='update_cart'),
    path('checkout/', views.checkout, name='checkout'),
    path('place-order/', views.place_order, name='place_order'),
    path('orders/', views.user_orders, name='user_orders'),
    path('checkout-success/', views.checkout_success, name='checkout_success'),
]
