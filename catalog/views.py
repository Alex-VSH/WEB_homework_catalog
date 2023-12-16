from datetime import datetime

from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin, UserPassesTestMixin
from django.core.exceptions import PermissionDenied
from django.forms import inlineformset_factory
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy, reverse
from pytils.translit import slugify

from catalog.models import Products, Note, ProductVersion

from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from catalog.forms import ProductsForm, ProductVersionForm, NoteForm, ProductsModeratorForm


# Create your views here.


def index_base(requests):
    return render(requests, 'catalog/base.html')


class ProductsCreateView(LoginRequiredMixin, CreateView):
    model = Products
    form_class = ProductsForm
    success_url = reverse_lazy('catalog:home')

    def form_valid(self, form):
        product = form.save(commit=False)
        product.prod_owner = self.request.user
        product.save()
        return super().form_valid(form)

class ProductsUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Products
    success_url = reverse_lazy('catalog:home')

    def get_form_class(self):
        if self.request.user.is_superuser:
            return ProductsForm
        elif self.request.user.groups.filter(name='moderator') and self.request.user == self.object.prod_owner:
            return ProductsForm
        elif self.request.user.groups.filter(name='moderator'):
            return ProductsModeratorForm
        elif self.request.user == self.object.prod_owner:
            return ProductsForm

    def test_func(self):
        _user = self.request.user
        _instance: Products = self.get_object()

        if _user == _instance.prod_owner:
            return True
        elif _user.groups.filter(name='moderator'):
            return True
        elif self.request.user.is_superuser:
            return True
        else:
            return self.handle_no_permission()


    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        if self.object.prod_owner != self.request.user and not self.request.user.is_staff:
            raise PermissionDenied()
        return self.object



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
        product = form.save(commit=False)
        product.prod_date_of_last_change = datetime.now()
        product.save()
        context_data = self.get_context_data()
        formset = context_data['formset']
        self.object = form.save()

        if formset.is_valid():
            formset.instance = self.object
            formset.save()
        return super().form_valid(form)


class ProductsDetailView(LoginRequiredMixin, DetailView):
    model = Products


class ProductsListView(LoginRequiredMixin, ListView):
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
