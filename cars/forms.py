from django import forms
from .models import CarListing, CarImage


# ============ КАСТОМНЫЙ ВИДЖЕТ ДЛЯ МНОЖЕСТВЕННОЙ ЗАГРУЗКИ ============

class MultipleFileInput(forms.ClearableFileInput):
    """Виджет для загрузки нескольких файлов"""
    allow_multiple_selected = True


class MultipleFileField(forms.FileField):
    """Поле для загрузки нескольких файлов"""

    def __init__(self, *args, **kwargs):
        kwargs.setdefault("widget", MultipleFileInput())
        super().__init__(*args, **kwargs)

    def clean(self, data, initial=None):
        single_file_clean = super().clean
        if isinstance(data, (list, tuple)):
            result = [single_file_clean(d, initial) for d in data]
        else:
            result = [single_file_clean(data, initial)]
        return result


# ============ ФОРМЫ ============

class CarListingForm(forms.ModelForm):
    """Форма для создания/редактирования объявления"""

    # Цвета (5 самых популярных)
    COLOR_CHOICES = [
        ('', 'Выберите цвет...'),
        ('Белый', 'Белый'),
        ('Черный', 'Черный'),
        ('Серебристый', 'Серебристый'),
        ('Серый', 'Серый'),
        ('Синий', 'Синий'),
    ]

    # Объём двигателя (5 самых популярных)
    ENGINE_VOLUME_CHOICES = [
        ('', 'Выберите объём...'),
        ('1.6', '1.6 л'),
        ('2.0', '2.0 л'),
        ('2.5', '2.5 л'),
        ('3.0', '3.0 л'),
        ('4.0', '4.0 л'),
    ]

    # Мощность (5 самых популярных)
    HORSEPOWER_CHOICES = [
        ('', 'Выберите мощность...'),
        ('150', '150 л.с.'),
        ('200', '200 л.с.'),
        ('250', '250 л.с.'),
        ('300', '300 л.с.'),
        ('400', '400 л.с.'),
    ]

    color = forms.ChoiceField(
        choices=COLOR_CHOICES,
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    engine_volume = forms.ChoiceField(
        choices=ENGINE_VOLUME_CHOICES,
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    horsepower = forms.ChoiceField(
        choices=HORSEPOWER_CHOICES,
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    class Meta:
        model = CarListing
        fields = [
            'brand', 'model', 'year', 'price', 'mileage',
            'body_type', 'engine_type', 'transmission', 'drive_type',
            'engine_volume', 'horsepower', 'color', 'description', 'city',
        ]
        widgets = {
            'year': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '2020'}),
            'price': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '2500000'}),
            'mileage': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '45000'}),
            'description': forms.Textarea(
                attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Опишите состояние автомобиля...'}),
            'city': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Москва'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if 'class' not in field.widget.attrs:
                field.widget.attrs['class'] = 'form-control'
            if field_name in ['brand', 'model', 'body_type', 'engine_type', 'transmission', 'drive_type']:
                field.empty_label = 'Выберите...'


class CarImageForm(forms.ModelForm):
    """Форма для загрузки одного изображения"""

    class Meta:
        model = CarImage
        fields = ['image', 'is_main']
        widgets = {
            'image': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'is_main': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }


class MultipleCarImageForm(forms.Form):
    """Форма для множественной загрузки изображений"""
    images = MultipleFileField(
        required=False,
        label='Фотографии (можно выбрать несколько)'
    )