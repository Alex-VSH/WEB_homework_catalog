from django.shortcuts import render, redirect

# Create your views here.

def index_home(requests):
    return render(requests, 'catalog/home.html')

def index_contacts(requests):
    return render(requests, 'catalog/contacts.html')