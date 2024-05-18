"""
Definition of forms.
"""
from django.db import models 
from.models import Comment
from .models import Blog

from django import forms
from .models import VideoPost


from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.utils.translation import ugettext_lazy as _


class BootstrapAuthenticationForm(AuthenticationForm):
    """Authentication form using bootstrap classes."""

    username = forms.CharField(max_length=254, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Имя пользователя'}))
    password = forms.CharField(label="Password", widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Пароль'}))

class AnketaForm(forms.Form):
    name = forms.CharField(label='Ваше имя', min_length=2, max_length=100)
    city = forms.CharField(label='Ваш город', min_length=2, max_length=100)
    job = forms.CharField(label='Ваш род занятий', min_length=2, max_length=100)
    gender = forms.ChoiceField(label='Ваш пол',
                                choices=(('1', 'Женский'), ('2', 'Мужской')),
                                widget=forms.RadioSelect,
                                initial='1')
    size = forms.ChoiceField(label='Ваш размер одежды',
                                choices=(('1', '40-42'),
                                        ('2', '44-46'),
                                        ('3', '48-50'),
                                        ('4', '52-54'),
                                        ('5', '56-58'),
                                        ('6', '60-62'),
                                        ('7', '64-66'),
                                        ('8', 'другой')),
                                widget=forms.RadioSelect,
                                initial='1')
    style = forms.CharField(label='Ваш любимый стиль одежды', min_length=2, max_length=100) 
    noticekarta = forms.BooleanField(label='Являетесь ли Вы постоянным покупателем торговой сети Россияночка?',
                                required=False)
    kartan = forms.CharField(label='Номер карты "Любимый покупатель"', max_length=10)
    internet = forms.ChoiceField(label='Вы пользуетесь интернетом',
                                choices=(('1', 'Каждый день'),
                                        ('2', 'Несколько раз в день'),
                                        ('3', 'Несколько раз в неделю'),
                                        ('4', 'Несколько раз в месяц')),
                                widget=forms.RadioSelect,
                                initial='1')
    notice = forms.BooleanField(label='Получать новости сайта на e-mail?',
                                required=False)
    email = forms.EmailField(label='e-mail', min_length=7)
    message = forms.CharField(label='Коротко о себе',
                                widget=forms.Textarea(attrs={'rows': 12, 'cols': 20}))
    

class CommentForm (forms.ModelForm):
    class Meta:
        model = Comment                                 # используемая модель
        fields = ('text',)                              # требуется заполнить только поле text
        labels = {'text': "Комментарий"}                # метка к полю формы text      
         

class BlogForm(forms.ModelForm):
    class Meta:
        model = Blog                                    # используемая модель
        fields = ('title', 'description', 'content', 'image',) 
        labels = {'title': "Заголовок", 'description': "Краткое содержание", 'content': "Полное содержание", 'image': "Картинка"}
        
class VideoPostForm(forms.ModelForm):
    class Meta:
        model = VideoPost
        fields = ('title', 'video', 'description')
        labels = {'title': "Заголовок", 'video': "Видео", 'description': "Содержание"}

        