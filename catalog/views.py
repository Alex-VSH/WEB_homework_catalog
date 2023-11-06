from django.shortcuts import render

from catalog.models import Products


# Create your views here.


def index_base(requests):
    return render(requests, 'catalog/base.html')


def index_home(requests):
    goods_list = Products.objects.all()
    context = {
        "object_list": goods_list
    }
    return render(requests, 'catalog/home.html', context)


def index_contacts(requests):
    return render(requests, 'catalog/contacts.html')


def index_show_good(requests, pk):
    context = {
        "object": Products.objects.get(pk=pk)
    }
    return render(requests, 'catalog/show_good.html', context)
