import http.client
import json
import os
import shutil
import urllib.error
import urllib.request

from PIL import Image
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from django.shortcuts import render, get_object_or_404
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.utils import timezone

from .forms import PostForm, UserForm, ComentForm
from .models import Post, Comment


# функція видалення посту
def post_dell(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if post:
        post.delete()
        posts = Post.objects.all().order_by('-published_date')
        return render(request, 'blog/post_list.html', {'posts': posts})


# функція для відображення форми лугування
def log_in(request):
    return render(request, 'blog/log_in.html')


# функція для відображення форми реєстрації
def sing_up(request):
    return render(request, 'blog/sing_up.html')


# функція реєстраці нових користувачів
def registration(request):
    if request.method == 'POST':
        user = UserForm(request.POST)
        if user.is_valid():
            new_user = user.save(False)
            new_user = User(username=user.cleaned_data['username'],
                            email=user.cleaned_data['email'],
                            password=user.cleaned_data['password'])
            new_user.set_password(new_user.password)
            new_user.save()
            message = "Thank Yuo for registrations!"
            return render(request, 'blog/base.html', {'message': message})
        else:
            m = "This e-mail: {}, has been registered.   ".format(user.cleaned_data['email'])
            return render(request, 'blog/base.html', {'message': m})
    else:
        form = UserForm()
        args = RequestContext(request, {'form': form})
        return render_to_response('blog/post_list.html', args)


# функція для перевірки даних логування
def user_login(request):
    if request.method == "POST":
        mail = request.POST.get('email', None)
        password = request.POST.get('password', None)
        if mail and password:
            user = authenticate(username=mail, password=password)
            if user:
                if user.is_active:
                    login(request, user)
                    return HttpResponseRedirect('/home')
                else:
                    m = "Invalid login details supplied. Invalid login details"
                    return render(request, 'blog/base.html', {'message': m})
            else:
                m = " ".join(["Invalid login details supplied.\n",
                              "Invalid login details: {}.\n".format(mail)])
                return render(request, 'blog/base.html', {'message': m})
    return HttpResponseRedirect('/user_login')


# функція  для виходу користувача
def user_logout(request):
    logout(request)
    return HttpResponseRedirect('/home')


def add_coment(request, pk):
    if request.method == "POST":
        post = get_object_or_404(Post, pk=pk)
        form = ComentForm(request.POST)
        if form and post:
            coment = form.save(commit=False)
            coment = Comment(comment_to=post, author=request.user,
                             comment_text=form.cleaned_data['coment_text'],
                             data=timezone.now())
            coment.save()
            return redirect('post_detail', pk=post.pk)
        else:
            m = "Fil coment field for submit."
            return render(request, 'blog/base.html', {'message': m})
    else:
        form = PostForm()
        args = RequestContext(request, {'form': form})
        return render_to_response('blog/post_list.html', args)


def get_sportnews(request):
    if request.method == "GET":
        url = urllib.request.urlopen(
            'https://newsapi.org/v1/articles?source=bbc-sport&sortBy=top&apiKey=7beff6cd7c164d58b4cc3d9dedf38cbd')
        response = url.read()
        charset = url.info().get_content_charset('utf-8')
        data = json.loads(response.decode(charset))
        articles = data['articles']
        for article in articles:
            form = PostForm()
            if not Post.objects.filter(title=article['title']):
                url = article['url']
                img_url = article['urlToImage']
                link = r'{}'.format(url)
                txt = "{}".format(article['description'])
                new_post = form.save(commit=False)
                new_post.author = request.user
                new_post.topic = "Sport"
                new_post.title = article['title']
                if article['urlToImage']:
                    img_url = article['urlToImage']
                    img = urllib.request.urlretrieve(img_url, img_url[-7:])
                    shutil.copy2(img[0], 'media/' + img[0])
                    new_post.post_img = img[0]
                    os.remove(img[0])
                new_post.text = txt
                new_post.link = link
                new_post.publish()
                return redirect('/sport')
    else:
        return redirect('/home')


def get_foodnews(request):
    if request.method == "GET":
        headers = {
            # Request headers
            'Ocp-Apim-Subscription-Key': '914781f8c1584f1893566e6eea1f5739',
        }

        params = urllib.parse.urlencode({
            # Request parameters
            'q': 'christmas food',
            'count': '10',
        })

        conn = http.client.HTTPSConnection('api.cognitive.microsoft.com')
        conn.request("GET", "/bing/v5.0/news/search?%s" % params, "{body}", headers)
        response = conn.getresponse()
        data = response.read()
        data = json.loads(data.decode('utf-8'))
        news = data['value']
        for n in news:
            form = PostForm()
            if not Post.objects.filter(title=n['name']):
                # img_url = n['image']['thumbnail']['contentUrl']
                url = n['url']
                link = r'{}'.format(url)
                new_post = form.save(commit=False)
                new_post.author = request.user
                new_post.topic = "Food"
                new_post.title = n['name']
                new_post.text = n['description']
                if n['image']['thumbnail']['contentUrl']:
                    img_url = n['image']['thumbnail']['contentUrl']
                    img = urllib.request.urlretrieve(img_url, new_post.title[:15] + '.jpeg')
                    shutil.copy2(img[0], 'media/' + img[0])
                    new_post.post_img = img[0]
                    os.remove(img[0])
                new_post.link = link
                new_post.publish()
                return redirect('/food')
    else:
        return redirect('/home')


def get_travelnews(request):
    if request.method == "GET":
        headers = {
            # Request headers
            'Ocp-Apim-Subscription-Key': '914781f8c1584f1893566e6eea1f5739',
        }

        params = urllib.parse.urlencode({
            # Request parameters
            'q': 'travel christmas',
            'count': '10',
        })

        conn = http.client.HTTPSConnection('api.cognitive.microsoft.com')
        conn.request("GET", "/bing/v5.0/news/search?%s" % params, "{body}", headers)
        response = conn.getresponse()
        data = response.read()
        data = json.loads(data.decode('utf-8'))
        news = data['value']
        for n in news:
            form = PostForm()
            if not Post.objects.filter(title=n['name']):
                # img_url = n['image']['thumbnail']['contentUrl']
                url = n['url']
                link = r'{}'.format(url)
                new_post = form.save(commit=False)
                new_post.author = request.user
                new_post.topic = "Travel"
                new_post.title = n['name']
                new_post.text = n['description']
                if 'image' in n:
                    img_url = n['image']['thumbnail']['contentUrl']
                    img = urllib.request.urlretrieve(img_url, new_post.title[:10] + '.jpeg')
                    shutil.copy2(img[0], 'media/' + img[0])
                    new_post.post_img = img[0]
                    os.remove(img[0])
                new_post.link = link
                new_post.publish()
                return redirect('/travel')
    else:
        return redirect('/home')


# функція  для виходу користувача
def user_logout(request):
    logout(request)
    return HttpResponseRedirect('/home', 'You are logout.')


# функція пошуку  посту
def search(request):
    if request.method == "GET":
        q = request.GET.get('q').lower().strip()
        if q:
            posts_all = Post.objects.all()
            posts = [p for p in posts_all if q in p.title.lower()]
            if posts:
                return render(request, 'blog/post_list.html', {'posts': posts})
            else:
                m = 'There are no post with "{}".'.format(q)
                return render(request, 'blog/base.html', {'message': m})
        else:
            m = "Fill a search form."
            return render(request, 'blog/base.html', {'message': m})
    else:
        return redirect('/home')
