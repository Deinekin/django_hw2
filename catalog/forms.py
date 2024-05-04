from django.forms import ModelForm, forms

from catalog.models import Product, Version


class StyleFormMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if field_name == 'current':
                field.widget.attrs['class'] = 'form-check-input'
            else:
                field.widget.attrs['class'] = 'form-control'


class ProductForm(StyleFormMixin, ModelForm):
    forbidden_words = ["казино", "криптовалюта", "крипта", "биржа", "дешево", "бесплатно", "обман", "полиция", "радар"]

    class Meta:
        model = Product
        exclude = ('owner', 'created_at', 'updated_at')

    def clean_name(self):
        cleaned_data = self.cleaned_data['name']
        if cleaned_data.lower() in ProductForm.forbidden_words:
            raise forms.ValidationError(f'Имя содержит запрещенное слово: {cleaned_data}. Введите другое имя продукта')
        return cleaned_data

    def clean_description(self):
        cleaned_data = self.cleaned_data['description']
        if cleaned_data.lower() in ProductForm.forbidden_words:
            raise forms.ValidationError(
                f'Описание содержит запрещенное слово: {cleaned_data}. Введите другое имя продукта')
        return cleaned_data


class ProductDescriptionForm(ProductForm):
    class Meta:
        model = Product
        fields = ('description',)


class ProductCategoryForm(ProductForm):
    class Meta:
        model = Product
        fields = ('category',)


class ProductPublishedForm(ProductForm):
    class Meta:
        model = Product
        fields = ('is_published',)


class VersionForm(StyleFormMixin, ModelForm):
    class Meta:
        model = Version
        fields = '__all__'
