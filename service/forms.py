from django import forms
from .models import Service, Schedule



class DateTimeLocalInput(forms.DateTimeInput):

SERVICE_CHOICES = [(service.id, service.title) for service in Service.objects.all()]

class ScheduleForm(forms.Form):
    begin = DateTimeLocalField(label='Время записи')
    service = forms.ChoiceField(label= 'Услуга', choices=SERVICE_CHOICES, widget=forms.Select)