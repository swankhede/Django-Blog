from django.shortcuts import render, redirect
from blogApp2.models import blogpost, profile
from blogApp2.forms import saveblog, updateblog, profileUpdate
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate, logout
from django.http import HttpResponseRedirect, HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.views.generic.edit import UpdateView
from DBlog2 import settings
import os
import json
import datetime


def index(request):
    # print(post)
    pr = profile.objects.filter(username=request.user)
    posts = blogpost.objects.all().order_by("time").reverse()
    return render(request, 'index.html', {'u': 'guest', 'blogs': posts, 'pr': pr})


def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']

        name = str(username)
        password = request.POST['password']

        user = authenticate(username=username, password=password)

        if user is not None:
            print(user.is_authenticated)
            login(request, user)

            return redirect(reverse('home'))
        else:
            return render(request, 'login.html', {'error': 'user and password does not match'})

    return render(request, 'login.html')


def signup(request):
    if request.method == 'POST':
        first_name = request.POST['first name']
        last_name = request.POST['last name']
        username = request.POST['username']
        password = request.POST['password']

        if request.POST['password'] == request.POST['password2']:
            if first_name != " " and last_name != " " and username != " " and password != " ":
                if User.objects.filter(username=username).exists():
                    return render(request, 'signup.html', {'error': "user already exists"})
                else:
                    user = User.objects.create_user(username=username,
                                                    password=password, first_name=first_name,
                                                    last_name=last_name)

                    user.save()
                    pr = profile(username=username)
                    pr.save()
                    return redirect(reverse(login_view))
            else:

                print("enter valid details")

                return render(request, 'signup.html', {'error': "pls feel all details"})
        else:
            return render(request, 'signup.html', {'error': "password does not match"})

    return render(request, 'signup.html')


@login_required
def logout_view(request):
    logout(request)
    return redirect(reverse('index'))


@login_required
def home(request):
    if request.user.is_authenticated:
        profile_obj = profile.objects.filter(username=request.user)
        posts = blogpost.objects.all().order_by("time").reverse()

        if request.method == 'POST':
            print(request.POST.get('search'))
            search_query = request.POST.get('search')
            posts = blogpost.objects.filter(title__contains=search_query)

            if not posts:
                posts = blogpost.objects.filter(content__contains=search_query)

            return render(request, 'home.html', context={'profile': profile_obj, 'posts': posts})

        return render(request, 'home.html', context={'profile': profile_obj, 'posts': posts})


@login_required
def post_blog(request):
    if request.user.is_authenticated:
        if request.method == 'POST':

            form2 = saveblog(request.POST, request.FILES)

            if form2.is_valid():
                inst = form2.save(commit=False)
                inst.author = request.user

                inst.save()
                return redirect(reverse('home'))
            else:
                return render(request, 'post-blog.html', {'error': form2.errors})
    else:
        return HttpResponse("<h1>User Not Found</h1>")

    return render(request, 'post-blog.html')


@login_required
def view_blog(request, title, author):
    if request.user.is_authenticated:

        post = blogpost.objects.get(title=title, author=author)

        return render(request, 'view_blog.html', {'blog': post})
    else:
        return HttpResponse("<h1>User Not Found</h1>")


@login_required
def profile_view(request, msg=None):
    if request.user.is_authenticated:
        user = User.objects.filter(username=request.user)

        post = blogpost.objects.filter(
            author=request.user).order_by("time").reverse()
        profile_obj = profile.objects.get(username=request.user)

        return render(request, 'profile.html', {'posts': post, 'profile': profile_obj})
    else:
        return HttpResponse("<h1>User Not Found</h1>")


def remove_image(image_name):
    try:

        os.remove(image_name)
        return True
    except FileExistsError as e:
        print(e)


def delete_blog(request, pk):
    if request.user.is_authenticated:
        post = blogpost.get_blog_post(pk)
        user = profile.objects.filter(username=request.user)
        if post.pic:
            remove_image(post.pic.file.name)

        blogpost.objects.filter(pk=pk).delete()
        return redirect(reverse('profile'))
    else:
        return HttpResponse("<h1>User Not Found</h1>")


def edit_blog(request, pk):

    if request.user.is_authenticated:
        post = blogpost.objects.get(pk=pk)

        title = request.POST.get('title')
        content = request.POST.get('content')

        if request.method == 'POST':
            post.title = title
            post.content = content
            post.author = post.author
            post.time = post.time

            if request.FILES.get('pic'):
                post.pic = request.FILES.get('pic')

            post.save()
            print("post updated")

        if request.GET.get('action'):
            print('here..')
            remove_image(post.pic)
            post.pic.delete()

            return render(request, 'edit.html', {'post': post, 'msg': "post has been updated"})
        return render(request, 'edit.html', {'post': post})
    else:
        return HttpResponse("<h1>User Not Found</h1>")


@login_required
def edit_accounts(request):
    if request.user.is_authenticated:

        profile_obj = profile.objects.get(username=request.user)
        blogs = blogpost.objects.filter(author=request.user)
        user = User.objects.get(username=request.user)
        print(profile_obj, user)
        print(request.method)
        print(request.POST.get('username'))

        if request.method == "POST":
            print("here....")

            User.objects.filter(username=request.user).update(

                username=request.POST.get('username'),
                first_name=request.POST.get('first_name'),
                last_name=request.POST.get('last_name'),

            )

            blogs.author = request.POST.get('username')
            profile_obj.username = request.POST.get('username')
            profile_obj.save()

            for i in blogs:
                print(i.author)
                i.author = request.POST.get('username')
                i.save()

            if request.FILES:
                if profile_obj.pic:
                    print("file name", profile_obj.pic.file.name)
                    remove_image(profile_obj.pic.file.name)
                profile_obj.pic = request.FILES.get('pic')
                profile_obj.save()

            return render(request, 'edit_profile.html', {'profile': profile_obj, 'msg': 'Profile Updated'})

    return render(request, 'edit_profile.html', {'profile': profile_obj})


@login_required
def accounts(request, author):
    author_obj = User.objects.get(username=author)
    post = blogpost.objects.filter(author=author).order_by("time").reverse()
    profile_obj = profile.objects.get(username=author)
    print(request.user)
    print(author_obj.first_name)
    print(author == request.user)
    if author == request.user.username:
        return redirect(reverse('profile'))
    else:
        return render(request, 'user_profile.html', {'posts': post, 'profile': profile_obj, 'author': author_obj})
