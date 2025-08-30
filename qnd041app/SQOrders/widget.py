from django import forms


class DatePickerInput(forms.DateInput):
    input_type = 'date'
    options= {
                    "format": "MM/DD/YYYY",
                    "locale": "bn",
                }

class TimePickerInput(forms.TimeInput):
    input_type = 'time'
    options={
                    "format": "MM/DD/YYYY",
                    "locale": "bn",
                }

class DateTimePickerInput(forms.DateTimeInput):
    input_type = 'datetime-local'
    options={
                    "format": "MM/DD/YYYY",
                    "locale": "bn",
                }