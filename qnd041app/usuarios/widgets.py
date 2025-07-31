# widgets.py
from django import forms

class CustomDatePickerWidget(forms.DateInput):
    input_type = 'date'


    def __init__(self, attrs=None, format=None):
        default_attrs = {
            'class': 'unfold-input w-full custom-datepicker',
            'autocomplete': 'off',
        }
        if attrs:
            default_attrs.update(attrs)
        super().__init__(attrs=default_attrs, format=format or '%Y-%m-%d')



class CustomTimePickerWidget(forms.TimeInput):
    input_type = 'time'


    def __init__(self, attrs=None, format=None):
        default_attrs = {
            'class': 'unfold-input w-full custom-timepicker',
            'autocomplete': 'off',
        }
        if attrs:
            default_attrs.update(attrs)
        super().__init__(attrs=default_attrs, format=format or '%H:%M')



class CustomDateTimePickerWidget(forms.DateTimeInput):
    input_type = 'datetime-local'

    def __init__(self, attrs=None, format=None):
        format = format or '%Y-%m-%dT%H:%M'
        super().__init__(attrs=attrs, format=format)

    class Media:
        css = {
            'all': (
                'https://cdnjs.cloudflare.com/ajax/libs/datepicker/0.6.5/datepicker.min.css',
            )
        }
        js = (
            'https://code.jquery.com/jquery-3.4.1.min.js',
            'https://cdnjs.cloudflare.com/ajax/libs/datepicker/0.6.5/datepicker.min.js',
            'https://cdnjs.cloudflare.com/ajax/libs/datepicker/0.6.5/i18n/datepicker.es-ES.min.js',
        )