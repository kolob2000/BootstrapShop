from django.db import models
from django.db.models.signals import pre_save
from pytils import translit


class Category(models.Model):
    title = models.CharField(max_length=255, verbose_name='Название', unique=True, null=False)
    description = models.TextField(blank=True, default='Здесь должно быть описание...', verbose_name='Описание')
    slug = models.SlugField(max_length=70, unique=True, blank=False, verbose_name='ЧПУ')
    is_active = models.BooleanField(default=True, verbose_name='Активно')

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.title


class Product(models.Model):
    title = models.CharField(max_length=255, null=False, verbose_name='Название')
    image = models.ImageField(upload_to='media', blank=True, default='default_product.jpg')
    description = models.TextField(blank=True, default='Здесь должно быть описание...', verbose_name='Описание')

    price = models.DecimalField(max_digits=8, decimal_places=2, verbose_name='Цена')
    old_price = models.DecimalField(max_digits=8, decimal_places=2, verbose_name='Старая цена', default=0)
    in_stock = models.BooleanField(default=True, verbose_name='На складе')
    quantity = models.PositiveIntegerField(default=0, verbose_name='Количество')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name='Категория')
    slug = models.SlugField(max_length=70, unique=True, blank=False, verbose_name='ЧПУ')
    is_active = models.BooleanField(default=True, verbose_name='Активно')

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'

    def __str__(self):
        return self.title


def slug_generator(sender, instance, *args, **kwargs):
    if not instance.slug:
        if sender.objects.count():
            instance.slug = translit.slugify(instance.title + '-' + str(sender.objects.order_by('-pk')[0].pk + 1))
        else:
            instance.slug = translit.slugify(instance.title + '-' + '1')


pre_save.connect(slug_generator, sender=Product)
pre_save.connect(slug_generator, sender=Category)


class Contact(models.Model):
    phone = models.CharField(max_length=50, verbose_name='Телефон')
    email = models.CharField(max_length=255, verbose_name='Эл. почта')
    city = models.CharField(max_length=255, verbose_name='Город')
    address = models.CharField(max_length=255, verbose_name='Адрес')
    is_active = models.BooleanField(default=True, verbose_name='Активно')


class Instagram(models.Model):
    image = models.ImageField(upload_to='media', blank=True, default='default_flower.png')
    url = models.CharField(max_length=255, blank=True, default=None)
    is_active = models.BooleanField(default=True, verbose_name='Активно')

    class Meta:
        verbose_name_plural = 'Наш Instagram'
        verbose_name = 'Изображение инстаграм'

