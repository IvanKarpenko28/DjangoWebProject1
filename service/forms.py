from django import forms
from .models import Service, Schedule



class DateTimeLocalInput(forms.DateTimeInput):    input_type = "datetime-local" class DateTimeLocalField(forms.DateTimeField):    # Set DATETIME_INPUT_FORMATS here because, if USE_L10N     # is True, the locale-dictated format will be applied     # instead of settings.DATETIME_INPUT_FORMATS.    # See also:     # https://developer.mozilla.org/en-US/docs/Web/HTML/Date_and_time_formats         input_formats = [        "%Y-%m-%dT%H:%M:%S",         "%Y-%m-%dT%H:%M:%S.%f",         "%Y-%m-%dT%H:%M"    ]    widget = DateTimeLocalInput(format="%Y-%m-%dT%H:%M")

SERVICE_CHOICES = [(service.id, service.title) for service in Service.objects.all()]

class ScheduleForm(forms.Form):
    begin = DateTimeLocalField(label='Время записи')
    service = forms.ChoiceField(label= 'Услуга', choices=SERVICE_CHOICES, widget=forms.Select)