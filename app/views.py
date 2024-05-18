"""
Definition of views.
"""

from datetime import datetime
from django.shortcuts import render
from django.http import HttpRequest
from .forms import AnketaForm 
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect

from django.db import models
from .models import Blog
from .forms import BlogForm
from .forms import VideoPostForm

from .models import Comment                                     # использование модели комментариев
from .forms import CommentForm                                  # использование формы ввода комментария


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
            'message':'Страница с нашими контактами.',
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

def links(request):
    """Renders the contact page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/links.html',
        {
            'title':'Полезные ресурсы',
             'message':'Сведения о нас.',
            'year':datetime.now().year,
        }
    )

def anketa(request):
    assert isinstance(request, HttpRequest)
    data = None
    gender = {'1': 'Женщина', '2': 'Мужчина'}
    size = {
         '1': '40-42',
         '2': '44-46',
         '3': '48-50',
         '4': '52-54',
         '5': '56-58',
         '6': '60-62',
         '7': '64-66',
         '8': 'другой'
    }
    internet = {
        '1': 'Каждый день', 
        '2': 'Несколько раз в день', 
        '3': 'Несколько раз в неделю',
        '4': 'Несколько раз в месяц'
    } 
    if request.method == 'POST':
        form = AnketaForm(request.POST)
        if form.is_valid():
            data = {
                'name': form.cleaned_data['name'],
                'city': form.cleaned_data['city'],
                'job': form.cleaned_data['job'],
                'gender': gender[form.cleaned_data['gender']],
                'size': size[form.cleaned_data['size']],
                'style': form.cleaned_data['style'],
                'noticekarta': 'Да' if form.cleaned_data['noticekarta'] else 'Нет',
                'kartan': form.cleaned_data['kartan'],
                'internet': internet[form.cleaned_data['internet']],
                'notice': 'Да' if form.cleaned_data['notice'] else 'Нет',
                'email': form.cleaned_data['email'],
                'message': form.cleaned_data['message']
            }
            form = None
    else:
        form = AnketaForm()
    return render(request, 'app/anketa.html', {'form': form, 'data': data})



def registration(request):
    """Renders the registration page."""
    if request.method == "POST":                        # после отправки формы
        regform = UserCreationForm(request.POST)
        if regform.is_valid():
            reg_f= regform.save(commit=False) 
            reg_f.is_staff = False                      # запрещен вход в административный раздел
            reg_f.is_active = True                      # активный пользователь
            reg_f.is_superuser = False                  # не является суперпользователем
            reg_f.date_joined = datetime.now()          # дата регистрации
            reg_f.last_login = datetime.now()           # дата последней авторизации
            
            regform.save()                              # сохраняем изменения после добавления полей 
            return redirect('home')                     # переадресация на главную страницу после регистрации
    else:
        regform = UserCreationForm()                    # создание объекта формы для ввода данных
    assert isinstance(request, HttpRequest) 
    return render(
        request,
        'app/registration.html',
        {
            'regform': regform,                         # передача формы в шаблон веб-страницы
            'year': datetime.now().year,
        }
    )


def blog(request):
    """Renders the blog page."""
    posts = Blog.objects.all()                          # запрос на выбор всех статей блога из модели
    assert isinstance(request, HttpRequest) 
    return render(
        request,
        'app/blog.html',
        {
            "title":"Блог", 
            'posts': posts,
            'year':datetime.now().year,                 # передача списка статей в шаблок веб-страницы
        }
    )


def blogpost (request, parametr):
    """Renders the blogpost page.""" 
    assert isinstance (request, HttpRequest) 
    post_1 = Blog.objects.get(id=parametr)                  #запрос на выбор конкретной статьи по параметру
    comments = Comment.objects.filter(post=parametr)
    
    if request.method == "POST":                            # после отправки данных формы на сервер методом POST
        form = CommentForm (request.POST) 
        if form.is_valid():
            comment_f = form.save(commit=False) 
            comment_f.author = request.user                 # добавляем (так как этого поля нет в форме) в модель Комментария (Comment) 
            comment_f.date = datetime.now()                 # добавляем в модель Комментария (Comment) текущую дату
            comment_f.post = Blog.objects.get(id=parametr)  # добавляем в модель Комментария (Comment) статью, для которой данный комментарий
            comment_f.save()                                # сохраняем изменения после добавления полей
            return redirect('blogpost', parametr=post_1.id) # переадресация на ту же страницу
    else:
        form = CommentForm()                                # создание формы для ввода комментария
    
    return render(
        request,
        'app/blogpost.html',
        {
            'post_1': post_1,                               # передача конкретной статьи в шаблон веб-страницы
            'comments': comments,                           # передача всех комментариев к данной статье в шаблон веб-страницы
            'form': form,                                   # передача формы добавления комментария в шаблон веб-страницы
            'year': datetime.now(). year,
        }
    )


def newpost(request):
    """Renders the newpost page."""
    assert isinstance(request, HttpRequest)
    
    if request.method == "POST":                            #после отправки формы
        blogform = BlogForm(request.POST, request.FILES) 
        if blogform.is_valid():
            blog_f = blogform.save(commit=False) 
            blog_f.posted = datetime.now()
            blog_f.autor = request.user
            blog_f.save()                                   #сохраняем изменения после добавления полей
        
            return redirect('blog')                         #переадресация на страницу Блог после создания стотьи Блога
    else:
        blogform = BlogForm()                                 #создание объекта формы для ввода данных 

    return render(
        request,
        'app/newpost.html',
        {
            'blogform': blogform,                           #передача формы в шаблон веб-страницы
            'title': 'Добавить статью блога',
            'year':datetime.now().year,
        }
    )

def videopost(request):
    """Renders the videopost page."""
    assert isinstance(request, HttpRequest)
    
    if request.method == "POST":
        videopost_form = VideoPostForm(request.POST, request.FILES)
        if videopost_form.is_valid():
            video_post = videopost_form.save(commit=False)
            video_post.posted = datetime.now()
            video_post.author = request.user
            video_post.save()
            
            return redirect('video_blog')
    else:
        videopost_form = VideoPostForm()  # Создание объекта формы для ввода данных

    return render(
        request,
        'app/videopost.html',
        {
            'videopost_form': videopost_form,
            'title': 'Добавить видеопост',
            'year': datetime.now().year,
        }
    )








