from django.urls import path

from catalog.views import index_home, index_contacts, index_show_good
from catalog.apps import CatalogConfig

app_name = CatalogConfig.name

urlpatterns = [
    path('', index_home, name='home'),
    path('contacts/', index_contacts, name='contacts'),
    path('<int:pk>/show_good/', index_show_good, name='show_good')
]