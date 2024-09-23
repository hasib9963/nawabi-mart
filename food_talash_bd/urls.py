from django.contrib import admin
from django.urls import path, include
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('shop/', include('products.urls')),
    path('cart/', include('cart.urls')),
    path('customer/', include('customer.urls')),

]
urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)

