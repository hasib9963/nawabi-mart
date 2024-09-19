from django.shortcuts import render
from products.models import Product
from categories.models import Category

def home(request, category_slug = None):
    data = Product.objects.all()
    if category_slug is not None:
        category = Category.objects.get(slug = category_slug)
        data = Product.objects.filter(category = category)
    categorys = Category.objects.all()
    return render(request, 'index.html', {'data' : data, 'category' : categorys})

def about(request):
    return render(request, 'about.html')

def contact(request):
    return render(request, 'contact.html')

def shop(request):
    return render(request, 'shop.html')

def cart(request):
    return render(request, 'cart.html')

