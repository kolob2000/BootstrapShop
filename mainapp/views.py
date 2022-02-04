from django.shortcuts import render
from django.views.generic import ListView
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


class ProductListView(ListView):
    model = Product

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(ProductListView, self).get_context_data(**kwargs)
        context['title'] = 'Продукты' if self.kwargs['slug'] is None else Category.objects.get(
            slug=self.kwargs['slug']).title
        context['categories'] = Category.objects.all().filter(is_active=True)
        return context

    def get_queryset(self):

        query = Product.objects.all().filter(is_active=True) if self.kwargs[
                                                                    'slug'] is None else Product.objects.all().filter(
            category__slug=self.kwargs['slug'], is_active=True)
        if self.request.GET.get('price') is None or str(self.request.GET.get('price')).isalpha():
            return query
        else:
            return query.order_by('price' if int(self.request.GET.get('price')) == 1 else '-price')
