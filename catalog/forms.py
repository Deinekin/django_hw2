from django.forms import ModelForm, forms

from catalog.models import Product, Version


class StyleFormMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if field_name == 'is_active':
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
            raise forms.ValidationError(f'Содержит запрещенное слово: {cleaned_data}. Введите другое имя продукта')
        return cleaned_data


class VersionForm(ModelForm):
    class Meta:
        model = Version
        fields = '__all__'
