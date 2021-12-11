from django.shortcuts import render, redirect
from .models import Service, Schedule
from .forms import ScheduleForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages



def service_list(request):
    """Renders the home page."""
    services = Service.objects.all()
    return render(
        request,
        'app/about.html',
        {
            'title':'Услуги',
            'services': services
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
            if not schedule.id:
                messages.add_message(request, messages.WARNING, 'Данное время уже занято.')
                return render(
                    request,
                    'app/sign_up.html',
                    {
                        'title':'Записаться',
                        'form': form
                        })
            return redirect('about')
    return render(
        request,
        'app/sign_up.html',
        {
            'title':'Записаться',
            'form': form
        }
    )

@login_required
def schedule_list(request):
    """Renders the home page."""
    profile = None
    schedules = Schedule.objects.all()
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
            'schedules': schedules
        }
    )

@login_required
def schedule_delete(request,pk):
    """Renders the home page."""
    schedule = Schedule.objects.get(id=pk)
    schedule.delete()
    return redirect('schedule_list')
# Create your views here.
