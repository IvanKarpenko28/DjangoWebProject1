"""
Definition of forms.
"""

from django import forms
from django.db import models
from .models import Comment
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm
from django.utils.translation import ugettext_lazy as _
from .models import Blog, phone_validator
from django.contrib.auth.forms import UserCreationForm
from django.core.validators import MinLengthValidator

User = get_user_model()


class BootstrapAuthenticationForm(AuthenticationForm):
    """Authentication form which uses boostrap CSS."""
    username = forms.CharField(max_length=254,
                               widget=forms.TextInput({
                                   'class': 'form-control',
                                   'placeholder': 'Имя пользователя'}))
    password = forms.CharField(label=_("Password"),
                               widget=forms.PasswordInput({
                                   'class': 'form-control',
                                   'placeholder':'Пароль'}))

class CommentForm (forms.ModelForm):
    class Meta:
        model = Comment 
        fields = ('text',) 
        labels = {'text': "Комментарий"} 

class BlogForm (forms.ModelForm):
    class Meta:
        model = Blog 
        fields = ('title','description','content','image') 
        labels = {'title' : "Заголовок", 'description' : "Краткое содержание", 'content' : "Полное содержание",'image' : "Картинка"} 

class RegistrationForm(UserCreationForm):
    phone = forms.CharField(max_length=12, validators=[
            phone_validator,
            MinLengthValidator(12),
        ], label='Номер телефона')
    class Meta:
        fields = ['username', 'phone']
        model = User
