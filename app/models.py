"""
Definition of models.
"""

from django.db import models

# Create your models here.
from datetime import datetime
from django.contrib import admin
from django.core.urlresolvers import reverse
from django.contrib.auth import get_user_model


User = get_user_model()
    

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile', verbose_name='пользователь')
    is_manager = models.BooleanField(default=False, verbose_name='пользователь является менеджером')

    def __str__(self):
        return self.user.username
admin.site.register(Profile)

class Blog(models.Model):
    title = models.CharField(max_length = 100, unique_for_date = "posted", verbose_name = "Заголовок")
    description = models.TextField(verbose_name = "Краткое содержание")
    content = models.TextField(verbose_name = "Полное содержание")
    image = models.FileField(default = 'temp.jpg', verbose_name = "Картинка")
    author = models.ForeignKey(User, null=True, blank=True, on_delete = models.SET_NULL, verbose_name = "Автор")
    posted = models.DateTimeField(default = datetime.now(), db_index = True, verbose_name = "Опубликована")

    def get_absolute_url(self): 
        return reverse("blogpost", args=[str(self.id)])

    def __str__(self): 
        return self.title

    class Meta:
        db_table = "Posts" 
        ordering = ["-posted"] 
        verbose_name = "Новости" 
        verbose_name_plural = "Новости" 
admin.site.register(Blog)

class Comment(models.Model):
    text = models.TextField(verbose_name = "Комментарий")
    date = models.DateTimeField(default = datetime.now(), db_index = True, verbose_name = "Дата")
    author = models.ForeignKey(User, on_delete = models.CASCADE, verbose_name = "Автор")
    post = models.ForeignKey(Blog, on_delete = models.CASCADE, verbose_name = "Статья")

    def __str__(self): 
        return 'Комментарий %s к %s' % (self.author, self.post)

    class Meta:
        db_table = "Comments" 
        verbose_name = "Новости" 
        verbose_name_plural = "Комментарии к новостям"
        ordering = ["-date"] 

admin.site.register(Comment)