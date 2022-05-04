from django.shortcuts import render, redirect
from .models import Service, Schedule, Notify
from .forms import ScheduleForm, NotifyForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone



def service_list(request):
    """Renders the home page."""
    services = Service.objects.all()
    if request.user.is_authenticated == True:
        notify = Notify.objects.filter(whom=request.user)
    else:
        notify = Notify.objects.all()
    notifys_count=notify.count()
    return render(
        request,
        'app/about.html',
        {
            'title':'Услуги',
            'services': services,
            'notifys_count': notifys_count
        }
    )

@login_required
def sign_up_for_a_service(request):
    """Renders the home page."""
    form = ScheduleForm()
    if request.method == 'POST':
        form = ScheduleForm(request.POST)
        if form.is_valid():
            user = request.user
            begin = form.cleaned_data['begin']
            service = Service.objects.get(id=form.cleaned_data['service'])
            schedule = Schedule.objects.create(begin=begin,client=user,service=service)
            now = timezone.now()
            if begin<now:
                messages.add_message(request, messages.WARNING, 'Нельзя записаться на прошедшее и текущее время')
                return render(
                    request,
                    'app/sign_up.html',
                    {
                        'title':'Записаться',
                        'form': form
                        })
            if begin.hour<9:
                messages.add_message(request, messages.WARNING, 'Мы работаем с 9 утра')
                return render(
                    request,
                    'app/sign_up.html',
                    {
                        'title':'Записаться',
                        'form': form
                        })
            if begin.hour>=20:
                messages.add_message(request, messages.WARNING, 'Нельзя записаться на 8 вечера и позже')
                return render(
                    request,
                    'app/sign_up.html',
                    {
                        'title':'Записаться',
                        'form': form
                        })
            if not schedule.id:
                messages.add_message(request, messages.WARNING, 'Данное время уже занято')
                return render(
                    request,
                    'app/sign_up.html',
                    {
                        'title':'Записаться',
                        'form': form
                        })
            return redirect('about')
    notify = Notify.objects.filter(whom=request.user)
    notifys_count=notify.count()
    return render(
        request,
        'app/sign_up.html',
        {
            'title':'Записаться',
            'form': form,
            'notifys_count': notifys_count
        }
    )

@login_required
def schedule_list(request):
    """Renders the home page."""
    profile = None
    schedules = Schedule.objects.all()
    now = timezone.now()
    schedule = Schedule.objects.filter(end__lt=now)
    schedule.delete()
    notify = Notify.objects.filter(whom=request.user)
    notifys_count=notify.count()
    try:        profile = request.user.profile    except:        pass
    if request.user.is_superuser or profile:
        pass
        if profile:
            if profile.is_manager:
                pass
    else:
        schedules = schedules.filter(client=request.user)
    return render(
        request,
        'app/schedule_list.html',
        {
            'title':'Услуги',
            'schedules': schedules,
            'notifys_count': notifys_count
        }
    )

@login_required
def schedule_delete(request,pk):
    """Renders the home page."""
    schedule = Schedule.objects.get(id=pk)
    profile = None
    try:        profile = request.user.profile    except:        pass
    if request.user.is_superuser:
        whom = schedule.client
        sdel = schedule.service.title
        notify = Notify.objects.create(whom=whom,sdel=sdel)
    if profile:
        if profile.is_manager:
            whom = schedule.client
            sdel = schedule.service.title
            notify = Notify.objects.create(whom=whom,sdel=sdel)
    schedule.delete()
    return redirect('schedule_list')
    
@login_required
def notify_list(request):
    """Renders the home page."""
    notify = Notify.objects.filter(whom=request.user)
    notifys_count=notify.count()
    return render(
        request,
        'app/notify.html',
        {
            'title':'Уведомления',
            'notify': notify,
            'notifys_count': notifys_count
        }
    )

@login_required
def notify_delete(request,pk):
    """Renders the home page."""
    notify = Notify.objects.get(id=pk)
    notify.delete()
    return redirect('notify_list')
