"""
Definition of views.
"""

from django.shortcuts import render, redirect
from django.http import HttpRequest
from django.template import RequestContext
from datetime import datetime
from django.contrib.auth.forms import UserCreationForm
from django.db import models
from .models import Blog, Comment, CustomerData
from .forms import BlogForm, CommentForm, RegistrationForm
from django.contrib.auth.decorators import login_required
from service.models import Notify
from django.contrib.auth import get_user_model



def home(request):
    """Renders the home page."""
    assert isinstance(request, HttpRequest)
    if request.user.is_authenticated == True:
        notify = Notify.objects.filter(whom=request.user)
    else:
        notify = Notify.objects.all()
    notifys_count=notify.count()
    return render(
        request,
        'app/index.html',
        {
            'title':'Главная',
            'year':datetime.now().year,
            'notifys_count': notifys_count
        }
    )

def registration (request):
    """Renders the registration page."""

    if request.method == 'POST' :
        regform = RegistrationForm(request.POST)
        if regform.is_valid():
           phone_number = regform.cleaned_data.pop('phone')
           reg_f = regform.save(commit=False)
           reg_f.is_staff = False
           reg_f.is_active = True
           reg_f.is_superuser = False
           reg_f.is_date_joined = datetime.now()
           reg_f.is_last_login = datetime.now()

           regform.save()
           customer_data = CustomerData.objects.create(user=reg_f, phone=phone_number)
           return redirect('home')
    else:
         regform = RegistrationForm()

    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/registration.html',
        {
            'regform': regform,
            'year': datetime.now().year
        }
    )

def blog(request):
    """Renders the blog page."""
    assert isinstance(request, HttpRequest)
    posts = Blog.objects.all() 
    if request.user.is_authenticated == True:
        notify = Notify.objects.filter(whom=request.user)
    else:
        notify = Notify.objects.all()
    notifys_count=notify.count()
    return render(
        request,
        'app/news.html',
        {
            'title':'Новости',
            'posts': posts, 
            'year':datetime.now().year,
            'notifys_count': notifys_count
            }
        )

def blogpost(request, parametr):
    """Renders the blogpost page."""
    post_1 = Blog.objects.get(id=parametr)
    comments = Comment.objects.filter(post=parametr)
    if request.method == "POST": 
        form = CommentForm(request.POST)
        if form.is_valid():
            comment_f = form.save(commit=False)
            comment_f.author = request.user 
            comment_f.date = datetime.now() 
            comment_f.post = Blog.objects.get(id=parametr) 
            comment_f.save() 
            return redirect('blogpost', parametr=post_1.id) 
    else:
            form = CommentForm() 
    assert isinstance(request, HttpRequest)
    if request.user.is_authenticated == True:
        notify = Notify.objects.filter(whom=request.user)
    else:
        notify = Notify.objects.all()
    notifys_count=notify.count()
    return render(
        request,
        'app/blogpost.html',
        {
            'post_1': post_1,
            'comments': comments,
            'form': form, 
            'year':datetime.now().year,
            'notifys_count': notifys_count
            }
        )

@login_required
def newpost(request):
    """Renders the blogpost page."""
    assert isinstance(request, HttpRequest)

    if request.method == "POST": 
        blogform = BlogForm(request.POST, request.FILES)
        if blogform.is_valid():
            blog_f = blogform.save(commit=False)           
            blog_f.posted = datetime.now() 
            blog_f.author = request.user  
            blog_f.save() 

            return redirect('news')
        else:
            print(blogform.errors)
    else:
        blogform = BlogForm() 
    notify = Notify.objects.filter(whom=request.user)
    notifys_count=notify.count()
    return render(
        request,
        'app/newpost.html',
        {
            'blogform': blogform,
            'title': 'Добавить новость',
            'year':datetime.now().year,
            'notifys_count': notifys_count
         }
     )
