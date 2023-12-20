from django.urls import path
from django.views.decorators.cache import cache_page

from catalog.views import index_contacts, ProductsListView, ProductsDetailView, NoteListView, NoteDetailView, \
    NoteDeleteView, NoteCreateView, NoteUpdateView, toggle_publishing, ProductsCreateView, ProductsUpdateView
from catalog.apps import CatalogConfig

app_name = CatalogConfig.name

urlpatterns = [
    path('', ProductsListView.as_view(), name='home'),
    path('contacts/', index_contacts, name='contacts'),
    path('create_product/', ProductsCreateView.as_view(), name='create_product'),
    path('update_product/<int:pk>', ProductsUpdateView.as_view(), name='update_product'),
    path('view/<int:pk>', cache_page(60)(ProductsDetailView.as_view()), name='show_good'),
    path('note_list/', NoteListView.as_view(), name='notes'),
    path('note_detail/<slug:slug>', NoteDetailView.as_view(), name='note_detail'),
    path('create_note/', NoteCreateView.as_view(), name='create'),
    path('edit_note/<slug:slug>', NoteUpdateView.as_view(), name='update'),
    path('delete/<slug:slug>', NoteDeleteView.as_view(), name='delete'),
    path('is_published/<slug:slug>', toggle_publishing, name='toggle_publishing')
]