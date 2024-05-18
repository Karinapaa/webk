﻿
from django.db import models 
from django.contrib import admin 
from datetime import datetime 
from django.urls import reverse
from django.contrib.auth.models import User

class Blog (models. Model):
    title = models. CharField(max_length = 100, unique_for_date = "posted", verbose_name = "Заголовок")
    description = models. TextField(verbose_name = "Краткое содержание")
    content = models. TextField(verbose_name = "Полное содержание")
    author = models.ForeignKey(User, null=True, blank=True, on_delete = models.SET_NULL, verbose_name = "Автор")
    posted = models.DateTimeField(default = datetime.now(), db_index= True, verbose_name = "Опубликована")
    image = models.FileField(default = 'temp.jpg', verbose_name="Путь к картинке")
    # video = models.FileField(default='temp.mp4', verbose_name="Путь к видео")
    
   
    # Методы класса:
    def get_absolute_url(self): # метод возвращает строку с URL-адресом записи
        return reverse("blogpost", args=[str(self.id)])
    def __str__(self): # метод возвращает название, используемое для представления отдельных записей в администр
        return self.title
    # Метаданные - вложенный класс, который задает дополнительные параметры модели:
    class Meta:
        db_table = "Posts" # имя таблицы для модели
        ordering = ["-posted"] # порядок сортировки данных в модели ("-" означает по убыванию)
        verbose_name = "статья блога" # имя, под которым модель будет отображаться в административном разделе  
        verbose_name_plural = "статьи блога" # тоже для всех статей блога
        
admin.site.register(Blog)

class Comment (models. Model):
    text = models. TextField(verbose_name = "Текст комментария")
    date = models.DateTimeField(default = datetime.now(), db_index = True, verbose_name = "Дата комментария")
    author= models.ForeignKey (User, on_delete = models.CASCADE, verbose_name = "Автор комментария")
    post = models.ForeignKey(Blog, on_delete = models.CASCADE, verbose_name = "Статья комментария")
    # Методы класса:
    def __str__(self): # метод возвращает название, используемое для представления отдельных записей в административном разделе
        return 'Комментарий %d %s к %s' % (self.id, self.author, self.post)
    # Метаданные - вложенный класс, который задает дополнительные параметры модели:
    class Meta:
        db_table = "Comment"
        ordering = ["-date"]
        verbose_name = "Комментарии к статье блога"
        verbose_name_plural = "Комментарии к статьям блога"
admin.site.register (Comment)

class VideoPost(models.Model):
    title = models.CharField(max_length=100, verbose_name="Заголовок")
    video = models.FileField(upload_to='videos/', default='temp.mp4', verbose_name="Путь к видео")
    description = models.TextField(verbose_name="Содержание")

    def __str__(self):
        return self.title