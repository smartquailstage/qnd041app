from django import forms
from .models import Order
from phonenumber_field.formfields import PhoneNumberField
from phonenumber_field.widgets import PhoneNumberPrefixWidget
from .widget import DatePickerInput, TimePickerInput, DateTimePickerInput
from bootstrap_datepicker_plus.widgets import DatePickerInput, TimePickerInput, MonthPickerInput, YearPickerInput


class MyDatePickerInput(DatePickerInput):
    template_name = 'orders/order/date-picker.html'


class OrderCreateForm(forms.ModelForm):
    agree_term = forms.BooleanField(required=True, help_text="I accept the terms and conditions of this services.")
    
    # Phone number field with default region (for CA in this case, but you can change it)
    phone = PhoneNumberField(
        region="CA",  # 'CA' for Canada, you can change it based on the default country you prefer
        widget=PhoneNumberPrefixWidget(
            widgets={
                'phone': forms.TextInput(attrs={'class': 'phone-input'}),
                'prefix': forms.Select(attrs={'class': 'prefix-select'})
            }
        ),
        help_text="Choice your local country extension number"
    )

    class Meta:
        model = Order
        fields = ['first_name', 'last_name', 'email', 'phone', 'arrival_date_time', 'departure_date_time', 'agree_term']
        
        widgets = {
            'arrival_date_time': DateTimePickerInput(format='%m/%d/%Y %H:%M'),
            'departure_date_time': DateTimePickerInput(format='%m/%d/%Y %H:%M'),
        }
