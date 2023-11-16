from django.contrib import admin

from catalog.models import Products, Category, Note, ProductVersion


# Register your models here.

@admin.register(Products)
class ProductsAdmin(admin.ModelAdmin):
    list_display = ('id', 'prod_name', 'prod_price', 'prod_category',)
    list_filter = ('prod_category',)
    search_fields = ('prod_name', 'prod_description',)

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'cat_name', 'cat_description',)


@admin.register(Note)
class NoteAdmin(admin.ModelAdmin):
    list_display = ('id', 'note_title', 'slug',)

@admin.register(ProductVersion)
class ProductVersionAdmin(admin.ModelAdmin):
    list_display = ('id', 'product', 'version_number', 'version_name', 'version_is_active',)