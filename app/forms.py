"""
Definition of forms.
"""

from django import forms
from django.db import models
from .models import Comment
from django.contrib.auth.forms import AuthenticationForm
from django.utils.translation import ugettext_lazy as _
from .models import Blog

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

class Feedback(forms.Form):
    name = forms.CharField(label= 'Заголовок', min_length=2, max_length=100)
    type = forms.ChoiceField(label= 'Тип отзыва', choices=(('1','Положительный'),('2','Отрицательный'),('3','Нейтральный')), initial=1)
    answer = forms.ChoiceField(label= 'Отзыв требует ответа?', choices=[('1','Да'),('2','Нет')], widget=forms.RadioSelect, initial=2)
    notice = forms.BooleanField(label= 'Отправить ответ на Email', required=False);
    feedback = forms.CharField(label= 'Введите отзыв', widget=forms.Textarea(attrs={'rows':7,'cols':40}))

class CommentForm (forms.ModelForm):
    class Meta:
        model = Comment 
        fields = ('text',) 
        labels = {'text': "Комментарий"} 

class BlogForm (forms.ModelForm):
    class Meta:
        model = Blog 
        fields = ('title','description','content','image',) 
        labels = {'title' : "Заголовок", 'description' : "Краткое содержание", 'content' : "Полное содержание",'image' : "Картинка"} 