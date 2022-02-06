from django.contrib import messages
from django.core.mail import send_mail
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.views.generic import ListView

from BootstrapShop import settings
from .forms import PrivacyRemoveForm
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


def privacy(request):
    return render(request, 'mainapp/privacy.html', context={'title': 'Политика конфидициальности'})


def delete_privacy(request):
    if request.method == 'POST':
        form = PrivacyRemoveForm(request.POST)
        if form.is_valid():
            message = form.cleaned_data['message']
            from_email = form.cleaned_data['email']
            theme = 'Запрос на удаление данных'
            mail = send_mail(theme, message + " " + from_email, settings.EMAIL_HOST_USER, (settings.EMAIL_HOST_USER,),
                             fail_silently=False)
            if not mail:
                messages.error(request, 'Ошибка отправки. Попробуйте снова.')
            else:
                messages.success(request, 'Сообщение отправлено. Ожидайте ответ в течение 10 дней.')
                return HttpResponseRedirect(reverse('main:delete_privacy'))
    else:
        form = PrivacyRemoveForm()
    context = {
        'title': 'Запрос на удаление данных',
        'form': form
    }
    return render(request, 'delete_privacy.html', context=context)
