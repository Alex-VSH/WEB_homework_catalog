from django.forms import inlineformset_factory
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy, reverse
from pytils.translit import slugify

from catalog.models import Products, Note, ProductVersion

from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from catalog.forms import ProductsForm, ProductVersionForm, NoteForm


# Create your views here.


def index_base(requests):
    return render(requests, 'catalog/base.html')


class ProductsCreateView(CreateView):
    model = Products
    form_class = ProductsForm
    success_url = reverse_lazy('catalog:home')


class ProductsUpdateView(UpdateView):
    model = Products
    form_class = ProductsForm
    success_url = reverse_lazy('catalog:home')

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        ProductVersionFormset = inlineformset_factory(Products, ProductVersion, form=ProductVersionForm, extra=1)
        if self.request.method == 'POST':
            formset = ProductVersionFormset(self.request.POST, instance=self.object)
        else:
            formset = ProductVersionFormset(instance=self.object)

        context_data['formset'] = formset
        return context_data

    def form_valid(self, form):
        context_data = self.get_context_data()
        formset = context_data['formset']
        self.object = form.save()

        if formset.is_valid():
            formset.instance = self.object
            formset.save()
        return super().form_valid(form)


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
    form_class = NoteForm
    success_url = reverse_lazy('catalog:notes')

    def form_valid(self, form):
        if form.is_valid():
            new_note = form.save()
            new_note.slug = slugify(new_note.note_title)
            new_note.save()

        return super().form_valid(form)


class NoteUpdateView(UpdateView):
    model = Note
    form_class = NoteForm

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
