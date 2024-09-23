from django.shortcuts import render
from products.models import Product
from categories.models import Category

def shop(request, category_slug = None):
    data = Product.objects.all()
    if category_slug is not None:
        category = Category.objects.get(slug = category_slug)
        data = Product.objects.filter(category = category)
    categorys = Category.objects.all()
    return render(request, 'shop.html', {'data' : data, 'category' : categorys})
