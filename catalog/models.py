from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from psycopg2._psycopg import connection

NULLABLE = {'blank': True, 'null': True}


# Create your models here.


class Products(models.Model):
    prod_name = models.CharField(max_length=100, verbose_name='наименование')
    prod_description = models.TextField(max_length=500, verbose_name='описание')
    prod_preview = models.ImageField(upload_to='products/', verbose_name='превью', **NULLABLE)
    prod_category = models.CharField(max_length=100, verbose_name='категория')
    prod_price = models.IntegerField(verbose_name='цена за покупку')
    prod_date_of_create = models.DateTimeField(verbose_name='дата создания')
    prod_date_of_last_change = models.DateTimeField(verbose_name='дата последнего изменения')

    def __str__(self):
        return f'''{self.prod_name}
{self.prod_description}'''

    class Meta:
        verbose_name = 'продукт'
        verbose_name_plural = 'продукты'
        ordering = ('prod_name',)


class Category(models.Model):
    cat_name = models.CharField(max_length=100, verbose_name='наименование')
    cat_description = models.TextField(max_length=500, verbose_name='описание')

    def __str__(self):
        return f'''{self.cat_name}
    {self.cat_description}'''

    class Meta:
        verbose_name = 'категория'
        verbose_name_plural = 'категории'
        ordering = ('cat_name',)


class Note(models.Model):
    note_title = models.CharField(max_length=100, verbose_name='заголовок')
    slug = models.CharField(max_length=100, verbose_name='slug', null=True, blank=True)
    note_body = models.TextField(verbose_name='содержимое')
    note_preview = models.ImageField(upload_to='notes/', verbose_name='превью', **NULLABLE)
    note_date_of_create = models.DateTimeField(auto_now_add=True, verbose_name='дата создания')
    note_views_count = models.IntegerField(default=0, verbose_name='просмотры')
    note_is_published = models.BooleanField(default=True)

    def __str__(self):
        return self.note_title

    class Meta:
        verbose_name = 'блоговая запись'
        verbose_name_plural = 'блоговые записи'
        ordering = ('note_title',)

    def get_absolute_url(self):
        return f'{self.slug}'


class ProductVersion(models.Model):
    product = models.ForeignKey(Products, on_delete=models.CASCADE)
    version_number = models.IntegerField(verbose_name='номер версии')
    version_name = models.CharField(max_length=100, verbose_name='название версии')
    version_is_active = models.BooleanField(default=False)

    def __str__(self):
        return self.version_name

    class Meta:
        verbose_name = 'версия продукта'
        verbose_name_plural = 'версии продукта'
        ordering = ('version_number',)


@receiver(post_save, sender=ProductVersion)
def set_current_version(sender, instance, **kwargs):
    if instance.version_is_active:
        ProductVersion.objects.filter(product=instance.product).exclude(pk=instance.pk).update(version_is_active=False)
