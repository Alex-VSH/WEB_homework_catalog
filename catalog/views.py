from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy, reverse
from pytils.translit import slugify

from catalog.models import Products, Note

from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView


# Create your views here.


def index_base(requests):
    return render(requests, 'catalog/base.html')


class ProductsDetailView(DetailView):
    model = Products


class ProductsListView(ListView):
    model = Products


def index_contacts(requests):
    return render(requests, 'catalog/contacts.html')


class NoteListView(ListView):
    model = Note


class NoteDetailView(DetailView):
    model = Note

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        self.object.note_views_count += 1
        self.object.save()
        return self.object

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(note_is_published=True)
        return queryset



class NoteCreateView(CreateView):
    model = Note
    fields = ('note_title', 'note_body', 'note_preview')
    success_url = reverse_lazy('catalog:notes')

    def form_valid(self, form):
        if form.is_valid():
            new_note = form.save()
            new_note.slug = slugify(new_note.note_title)
            new_note.save()

        return super().form_valid(form)


class NoteUpdateView(UpdateView):
    model = Note
    fields = ('note_title', 'note_body', 'note_preview')

    def get_success_url(self):
        agent_id = self.object.slug
        return reverse_lazy('catalog:note_detail', kwargs={'slug': agent_id})



class NoteDeleteView(DeleteView):
    model = Note
    success_url = reverse_lazy('catalog:notes')


def toggle_publishing(requests, pk):
    note_item = get_object_or_404(Note, pk=pk)
    if note_item.note_is_published:
        note_item.note_is_published = False
    else:
        note_item.note_is_published = True

    note_item.save()

    return redirect(reverse('catalog:notes'))

