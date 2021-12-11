from django.db import models
from datetime import timedelta, datetime
from django.contrib.auth import get_user_model
from django.db.models import Q



User = get_user_model()

class Service(models.Model):
    title = models.CharField(max_length = 100, verbose_name = "название")
    description = models.TextField(verbose_name = "полное содержание")
    length = models.TimeField(verbose_name = "продолжительность")

    class Meta: 
        verbose_name = "услуга"
        verbose_name_plural = "услуги"

    def __str__(self): 
        return self.title

class Schedule(models.Model):
    begin = models.DateTimeField(verbose_name="начало в")
    end = models.DateTimeField(blank=True, null = True, verbose_name="окончание в")
    service = models.ForeignKey(Service, on_delete=models.CASCADE, verbose_name="услуга")
    client = models.ForeignKey(User, blank=True, null = True, on_delete=models.CASCADE, verbose_name="клиент")
    
    class Meta: 
        verbose_name = "расписание"
        verbose_name_plural = "расписания"

    def __str__(self): 
        return f'{self.begin}: {self.end} | {self.service.title}'

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        end = self.begin + timedelta(days=0, hours=self.service.length.hour, minutes=self.service.length.minute)
        schedules = Schedule.objects.filter(Q(begin__range=[self.begin, end])|Q(end__range=[self.begin, end]))
        if schedules.count():
            pass
        else:
            self.end = end
            return super().save()

# Create your models here.
