from django.contrib import admin

from mainapp.models import Product, Category, Contact, Instagram


class ProductAdmin(admin.ModelAdmin):
    list_filter = ('category',)
    list_display_links = ('title',)
    list_display = ('title', 'image', 'is_active',)
    list_editable = ('image', 'is_active',)


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('title', 'is_active',)
    list_display_links = ('title',)
    list_editable = ('is_active',)


admin.site.register(Product, ProductAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Contact)
admin.site.register(Instagram)
