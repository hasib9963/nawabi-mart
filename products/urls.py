from django.urls import path
from . import views

urlpatterns = [
        path('shop/', views.shop, name='shop'),
        path('product/details/<int:id>/', views.DetailProductView.as_view(), name='product_details'),
        path('order/payment/', views.payment, name='payment'),
        path('order/payment/success/', views.payment_success, name='payment_success'),
]