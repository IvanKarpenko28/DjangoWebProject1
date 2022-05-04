"""
Definition of urls for DjangoWebProject1.
"""

from datetime import datetime
from django.conf.urls import url
import django.contrib.auth.views

import app.forms
import app.views

from django.conf.urls import include
from django.contrib import admin
#admin.autodiscover()

from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf import settings 
import service.views



urlpatterns = [
    # Examples:
    url(r'^admin/', admin.site.urls),
    url(r'^$', app.views.home, name='home'),
    url(r'^news$', app.views.blog, name='news'),
    url(r'^about$', service.views.service_list, name='about'),
    url(r'^schedule_list$', service.views.schedule_list, name='schedule_list'),
    url(r'^notify_list$', service.views.notify_list, name='notify_list'),
    url(r'^schedule/(?P<pk>\d+)/delete$', service.views.schedule_delete, name='schedule_delete'),
    url(r'^notify/(?P<pk>\d+)/delete$', service.views.notify_delete, name='notify_delete'),
    url(r'^sign_up$', service.views.sign_up_for_a_service, name='sign_up'),
    url(r'^newpost$', app.views.newpost, name='newpost'),
    url(r'^(?P<parametr>\d+)/$', app.views.blogpost, name='blogpost'),
    url(r'^login/$',
        django.contrib.auth.views.login,
        {
            'template_name': 'app/login.html',
            'authentication_form': app.forms.BootstrapAuthenticationForm,
            'extra_context':
            {
                'title': 'Войти',
                'year': datetime.now().year,
            }
        },
        name='login'),
    url(r'^logout$',
        django.contrib.auth.views.logout,
        {
            'next_page': '/',
        },
        name='logout'),
    url(r'^registration$', app.views.registration, name='registration'),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += staticfiles_urlpatterns()