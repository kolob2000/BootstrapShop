from django.urls import path
import mainapp.views as mainapp

app_name = 'mainapp'

urlpatterns = [
    path('', mainapp.main, name='index'),
    path('product/', mainapp.ProductListView.as_view(), kwargs={'slug': None}, name='product'),
    path('product/<slug:slug>/', mainapp.ProductListView.as_view(), name='category'),
    path('privacy/', mainapp.privacy, name='privacy'),
    path('delete_privacy/', mainapp.delete_privacy, name='delete_privacy'),
]
