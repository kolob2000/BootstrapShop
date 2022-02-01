from django.shortcuts import render
from .models import Product, Category, Instagram


# Create your views here.
def main(request):
    context = {
        'title': 'Главная страница',
        'products': Product.objects.all().filter(is_active=True, category__is_active=True).order_by('?')[:4],
        'categories': Category.objects.all().filter(is_active=True),
        'insta_images': Instagram.objects.all().filter(is_active=True).order_by('?'),
    }
    return render(request, 'mainapp/index.html', context=context)
