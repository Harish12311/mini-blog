from django.shortcuts import render, HttpResponseRedirect
from django.contrib.auth.forms import UserCreationForm
from .forms import SignupForm, LoginForm, PostForms
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from .models import Post
from django.contrib.auth.models import Group


# Create your views here.
#Home
def home(request):
    posts = Post.objects.all()
    return render(request, 'blog/home.html', {'posts': posts})


#About
def about(request):
    return render(request, 'blog/about.html')


#Contact
def contact(request):
    return render(request, 'blog/contact.html')


#Dashboard

def dashboard(request):
    if request.user.is_authenticated:
        posts = Post.objects.all()
        user=request.user
        full_name=user.get_full_name()
        gps=user.groups.all()

        return render(request, 'blog/dashboard.html', {'posts': posts,'full_name':full_name,'groups':gps})
    else:
        return HttpResponseRedirect('/user_login/')


#Signup
def usre_signup(request):
    if request.method == "POST":
        form = SignupForm(request.POST)
        if form.is_valid():
            messages.success(request, 'Congregations!! You have become an Author')
            user = form.save()
            group = Group.objects.get(name='author')
            user.Group.add(group)
    else:
        form = SignupForm()
    return render(request, 'blog/signup.html', {'form': form})


#Login
def user_login(request):
    #if request.user.is_authenticated:
    if request.method == "POST":
        form = LoginForm(request=request, data=request.POST)
        if form.is_valid():
            uname = form.cleaned_data['username']
            passw = form.cleaned_data['password']
            user = authenticate(request, username=uname, password=passw)
            if user is not None:
                login(request, user)
                messages.success(request, 'Logged in successfully')
                return HttpResponseRedirect('/dashboard/')
            else:
                messages.error(request, 'Invalid username or password')
        else:
            messages.error(request, 'Invalid form submission')
    else:
        form = LoginForm()
    return render(request, 'blog/login.html', {'form': form})


#else:
#  return HttpResponseRedirect('/dashboard/')


#Logout
def user_logout(request):
    logout(request)
    return HttpResponseRedirect('/')


#add new Post
def add_post(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            form = PostForms(request.POST)
            if form.is_valid():
                title = form.cleaned_data['title']
                desc = form.cleaned_data['desc']
                pst = Post(title=title, desc=desc)
                pst.save()
                form = PostForms()
        else:
            form = PostForms()
        return render(request, 'blog/addpost.html', {'form': form})
    else:
        return HttpResponseRedirect('/user_login/')


#Update post
def update_post(request, id):
    if request.user.is_authenticated:
        if request.method == 'POST':
            pi = Post.objects.get(pk=id)
            form = PostForms(request.POST, instance=pi)
            if form.is_valid():
                form.save()
        else:
            pi = Post.objects.get(pk=id)
            form = PostForms(instance=pi)
        return render(request, 'blog/updatepost.html', {'form': form})
    else:
        return HttpResponseRedirect('/user_login/')


#delete Post
def delete_post(request, id):
    if request.user.is_authenticated:
        if request.method == 'POST':
            pi = Post.objects.get(pk=id)
            pi.delete()
        return HttpResponseRedirect('/dashboard/')
    else:
        return HttpResponseRedirect('/user_login/')
