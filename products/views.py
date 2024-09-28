from django.shortcuts import render
from . import models
from products.models import Product
from categories.models import Category
from django.views.generic import DetailView


def shop(request, category_slug = None):
    data = Product.objects.all()
    if category_slug is not None:
        category = Category.objects.get(slug = category_slug)
        data = Product.objects.filter(category = category)
    categorys = Category.objects.all()
    return render(request, 'shop.html', {'data' : data, 'category' : categorys})

class DetailProductView(DetailView):
    model = models.Product
    pk_url_kwarg = 'id'
    template_name = 'product-details.html'

    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        product = self.get_object()

        context['product'] = product
        return context

def payment(request):
    return render(request, 'payment.html')

def payment_success(request):
    return render(request, 'payment_success.html')