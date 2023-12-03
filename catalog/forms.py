from django import forms

from catalog.models import Products, ProductVersion, Note


class StyleFormMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if field_name != 'version_is_active':
                field.widget.attrs['class'] = 'form-control'


class ProductsForm(StyleFormMixin, forms.ModelForm):
    class Meta:
        model = Products
        fields = ('prod_name', 'prod_description', 'prod_preview', 'prod_category', 'prod_price',)

    def clean_prod_name(self):
        cleaned_data = self.cleaned_data['prod_name']
        forbidden_words = ['казино', 'криптовалюта', 'крипта', 'биржа', 'дешево', 'бесплатно', 'обман', 'полиция',
                           'радар']
        for word in forbidden_words:
            if word in cleaned_data:
                raise forms.ValidationError(f'Вы использовали одно из запрещенных слов: {forbidden_words}')

        return cleaned_data

    def clean_prod_description(self):
        cleaned_data = self.cleaned_data['prod_description']
        forbidden_words = ['казино', 'криптовалюта', 'крипта', 'биржа', 'дешево', 'бесплатно', 'обман', 'полиция',
                           'радар']
        for word in forbidden_words:
            if word in cleaned_data:
                raise forms.ValidationError(f'Вы использовали одно из запрещенных слов: {forbidden_words}')

        return cleaned_data


class ProductVersionForm(StyleFormMixin, forms.ModelForm):
    class Meta:
        model = ProductVersion
        fields = ('__all__')


class NoteForm(StyleFormMixin, forms.ModelForm):
    class Meta:
        model = Note
        fields = ('note_title', 'note_body', 'note_preview',)
