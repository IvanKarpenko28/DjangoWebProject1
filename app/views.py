"""
Definition of views.
"""

from django.shortcuts import render, redirect
from django.http import HttpRequest
from django.template import RequestContext
from datetime import datetime
from .forms import Feedback 
from django.contrib.auth.forms import UserCreationForm
from django.db import models
from .models import Blog
from .models import Comment 
from .forms import CommentForm
from .forms import BlogForm
from django.contrib.auth.decorators import login_required


def home(request):
    """Renders the home page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/index.html',
        {
            'title':'Главная',
            'year':datetime.now().year,
        }
    )

def contact(request):
    """Renders the contact page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/contact.html',
        {
            'title':'Контакты',
            'year':datetime.now().year,
        }
    )

def about(request):
    """Renders the about page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/about.html',
        {
            'title':'О нас',
            'message':'Сведения о нас.',
            'year':datetime.now().year,
        }
    )

def links (request):
    """Renders the about page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/links.html',
        {
            'title':'Полезные приобретения',
            'message':'Материалы для самостоятельной закупки.',
            'year':datetime.now().year,
        }
    )

@login_required
def feedback (request):
    assert isinstance(request, HttpRequest)
    data = None
    
    type = {'1': 'Положительный', '2': 'Отрицательный', '3': 'Нейтральный'}
    answer = {'1': 'Да', '2': 'Нет'}
    if request.method == 'POST' :
        form = Feedback(request.POST)
        if form.is_valid():
            data = dict()
            data['name'] = form.cleaned_data['name']
            data['type'] = type[ form.cleaned_data['type'] ]
            data['answer'] = answer[ form.cleaned_data['answer'] ]
            if (form.cleaned_data['notice'] == True):
                data['notice'] = 'Да'
            else:
                data['notice'] = 'Нет'
            data['feedback'] = form.cleaned_data['feedback']
            form = None
    else:
        form = Feedback()
    return render(
        request,
        'app/feedback.html',
        {
            'form': form,
            'data': data
        }
    )

def registration (request):
    """Renders the registration page."""

    if request.method == 'POST' :
        regform = UserCreationForm(request.POST)
        if regform.is_valid():
           reg_f = regform.save(commit=False)
           reg_f.is_staff = False
           reg_f.is_active = True
           reg_f.is_superuser = False
           reg_f.is_date_joined = datetime.now()
           reg_f.is_last_login = datetime.now()

           regform.save()

           return redirect('home')
    else:
         regform = UserCreationForm()

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

    return render(
        request,
        'app/news.html',
        {
            'title':'Новости',
            'posts': posts, 
            'year':datetime.now().year,
            }
        )

@login_required
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
    return render(
        request,
        'app/blogpost.html',
        {
            'post_1': post_1,
            'comments': comments,
            'form': form, 
            'year':datetime.now().year,
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
            blog_f.autor = request.user  
            blog_f.save() 

            return redirect('news') 
    else:
        blogform = BlogForm() 

    return render(
        request,
        'app/newpost.html',
        {
            'blogform': blogform,
            'title': 'Добавить новость',
 
            'year':datetime.now().year,
         }
     )

def videopost(request):
    """Renders the about page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/videopost.html',
        {
            'title':'Полезные видео',
            'year':datetime.now().year,
        }
    )