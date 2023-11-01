from django.contrib import admin

from catalog.models import Products, Category

# Register your models here.

@admin.register(Products)
class ProductsAdmin(admin.ModelAdmin):
    list_display = ('id', 'prod_name', 'prod_price', 'prod_category',)
    list_filter = ('prod_category',)
    search_fields = ('prod_name', 'prod_description',)

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'cat_name', 'cat_description',)