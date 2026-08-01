from django import forms
from .models import CarListing, CarImage
import re


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

    # ============ ВАЛИДАЦИЯ ============

    def clean_year(self):
        """Проверка года выпуска (1900-2026)"""
        year = self.cleaned_data.get('year')
        current_year = 2026

        if year:
            try:
                year = int(year)
                if year < 1900:
                    raise forms.ValidationError('Год выпуска не может быть раньше 1900')
                if year > current_year:
                    raise forms.ValidationError(f'Год выпуска не может быть позже {current_year}')
            except (ValueError, TypeError):
                raise forms.ValidationError('Введите корректный год')
        return year

    def clean_price(self):
        """Проверка цены (не отрицательная, не слишком большая)"""
        price = self.cleaned_data.get('price')

        if price is not None and price != '':
            try:
                price = float(price)
                if price < 0:
                    raise forms.ValidationError('Цена не может быть отрицательной')
                if price > 100000000:
                    raise forms.ValidationError('Цена не может превышать 100 000 000 ₽')
            except (ValueError, TypeError):
                raise forms.ValidationError('Введите корректную цену')
        return price

    def clean_mileage(self):
        """Проверка пробега (не отрицательный, не слишком большой)"""
        mileage = self.cleaned_data.get('mileage')

        if mileage is not None and mileage != '':
            try:
                mileage = int(mileage)
                if mileage < 0:
                    raise forms.ValidationError('Пробег не может быть отрицательным')
                if mileage > 1000000:
                    raise forms.ValidationError('Пробег не может превышать 1 000 000 км')
            except (ValueError, TypeError):
                raise forms.ValidationError('Введите корректный пробег')
        return mileage

    def clean_engine_volume(self):
        """Проверка объёма двигателя"""
        engine_volume = self.cleaned_data.get('engine_volume')

        if engine_volume:
            try:
                engine_volume = float(engine_volume)
                if engine_volume < 0:
                    raise forms.ValidationError('Объём двигателя не может быть отрицательным')
                if engine_volume > 20:
                    raise forms.ValidationError('Объём двигателя не может превышать 20 л')
            except (ValueError, TypeError):
                # Если это выбор из списка (строка) — пропускаем проверку
                pass
        return engine_volume

    def clean_horsepower(self):
        """Проверка мощности"""
        horsepower = self.cleaned_data.get('horsepower')

        if horsepower:
            try:
                horsepower = int(horsepower)
                if horsepower < 0:
                    raise forms.ValidationError('Мощность не может быть отрицательной')
                if horsepower > 2000:
                    raise forms.ValidationError('Мощность не может превышать 2000 л.с.')
            except (ValueError, TypeError):
                # Если это выбор из списка (строка) — пропускаем проверку
                pass
        return horsepower

    def clean_vin(self):
        """Проверка VIN-кода (17 символов, только латиница и цифры)"""
        vin = self.cleaned_data.get('vin')

        if vin:
            vin = vin.upper().strip()
            if len(vin) != 17:
                raise forms.ValidationError('VIN-код должен содержать ровно 17 символов')
            if any(char in vin for char in ['I', 'O', 'Q']):
                raise forms.ValidationError('VIN-код не должен содержать буквы I, O, Q')
            if not re.match(r'^[A-HJ-NPR-Z0-9]{17}$', vin):
                raise forms.ValidationError('VIN-код должен содержать только латинские буквы и цифры')
        return vin

    def clean(self):
        """Общая проверка формы (комбинация полей)"""
        cleaned_data = super().clean()
        year = cleaned_data.get('year')
        price = cleaned_data.get('price')

        # Если цена слишком низкая для нового автомобиля
        if year and price:
            try:
                year = int(year)
                price = float(price)
                if year >= 2020 and price < 50000:
                    raise forms.ValidationError('Цена слишком низкая для автомобиля такого года выпуска')
            except (ValueError, TypeError):
                pass

        return cleaned_data


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