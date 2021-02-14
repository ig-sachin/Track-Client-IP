from django.shortcuts import render, HttpResponseRedirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .forms import  SignUpForm, LoginForm, Postform
from django.contrib import messages
from django.contrib.auth import logout, login, authenticate
from .models import Post
from django.contrib.auth.models import Group
# Create your views here.
def home(request):
    posts = Post.objects.all()
    return render(request, 'blog/home.html', {'posts':posts})

def about(request):
    return render(request, 'blog/about.html', {})

def contact(request):
    return render(request, 'blog/contact.html', {})

def dashboard(request):
    if request.user.is_authenticated:
        posts = Post.objects.all()
        user = request.user
        full_name = user.get_full_name()
        ip = request.session.get('ip', "lauda")
        gps = user.groups.all()
        return render(request, 'blog/dashboard.html', {'posts':posts, 'full_name':full_name, 'groups':gps, 'ip':ip})
    else:
        return HttpResponseRedirect('/login/')

def logout_user(request):
    logout(request)
    return HttpResponseRedirect('/login/')

def signup_user(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            messages.success(request, "Congratulations You Have Become an authur")
            user = form.save()
            group = Group.objects.get(name='Author')
            user.groups.add(group)
    else:
        form = SignUpForm()
    return render(request, 'blog/signup.html', {'form':form})

def login_user(request):
    if not request.user.is_authenticated:
        if request.method == 'POST':
            form = LoginForm(request=request, data=request.POST)
            if form.is_valid():
                uname = form.cleaned_data['username']
                upass = form.cleaned_data['password']
                user = authenticate(username= uname, password= upass)
                if user is not None:
                    login(request, user)
                    messages.success(request, "Logged in successfully")
                    return HttpResponseRedirect('/dashboard/')
        else:
            form = LoginForm()
        return render(request, 'blog/login.html', {'form':form})
    else:
        return HttpResponseRedirect('/dashboard/')


def add_post(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            form = Postform(request.POST)
            if form.is_valid():
                title = form.cleaned_data['title']
                desc = form.cleaned_data['desc']
                pst = Post(title=title, desc=desc)
                pst.save()
                messages.success(request, "Congratulations You Have Successfully Add a Post")
                form = Postform()
        else:
            form = Postform()
        return render(request, 'blog/addpost.html', {'form':form})
    else:
        return HttpResponseRedirect('/login/')

def update_post(request, id):
    if request.user.is_authenticated:
        if request.method == 'POST':
            pi = Post.objects.get(pk=id)
            form = Postform(request.POST, instance=pi)
            if form.is_valid():
                form.save()
        else:
            pi = Post.objects.get(pk=id)
            form = Postform(instance=pi)
        return render(request, 'blog/update.html', {'form': form})
    else:
        return HttpResponseRedirect('/login/')

def delete_post(request, id):
    if request.user.is_authenticated:
        if request.method == 'POST':
            pi = Post.objects.get(pk=id)
            pi.delete()
            return HttpResponseRedirect('/dashboard/')
    else:
        return HttpResponseRedirect('/login/')
