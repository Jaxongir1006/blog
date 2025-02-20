from django.shortcuts import render,redirect,get_object_or_404
from django.http import Http404
from .forms import RegisterForm,LoginForm,ProfileUpdateForm,UserUpdateForm,CreateBlogForm,UpdateBlogForm
from .models import Profile,Blog
from django.contrib.auth import authenticate,login,logout
from django.core.mail import send_mail
from django.conf import settings
# Create your views here.

def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            Profile.objects.create(user = user)
            return redirect('login')
    form = RegisterForm()
    context = {
        'form':form,
    }
    return render(request, 'user/register.html', context)

def login_view(request):
    context = {}
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(request, **form.cleaned_data)
            if user:
                login(request,user)
                if user.first_name and user.last_name:
                    return redirect('profile')
                else:
                    return redirect('update_profile')
            else:
                context['error'] = 'User topilmadi'
        else:
            context['error'] = form.errors
            
    return render(request,'user/login.html', context)

def log_out(request):
    logout(request)
    return redirect('login')

def profile(request, id):

    user = Profile.objects.get(id = id)

    context = {
        'user':user,
    }

    return render(request, 'new/about.html', context)

def update_profile(request):
    if request.method == 'GET':
        profile_form = ProfileUpdateForm(instance=request.user.profile)
        user_form = UserUpdateForm(instance=request.user)
    if request.method == 'POST':
        profile_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        user_form = UserUpdateForm(request.POST, instance=request.user)
        if profile_form.is_valid() and user_form.is_valid():
            profile_form.save()
            user_form.save()
        return redirect('profile')
    context = {
        'profile_form':profile_form,
        'user_form':user_form
    }
    return render(request, 'profile/update_profile.html', context)

def create_blog(request):
    form = CreateBlogForm()
    if request.method == 'POST':
        form = CreateBlogForm(request.POST, request.FILES)
        if form.is_valid():
            blog = form.save()
            blog.author = request.user.profile
            blog.save()
            return redirect('profile') 
    context = {
        'form':form,
        'user':request.user
    }

    return render(request, 'profile/create_blog.html', context)

def my_blogs(request):
    blogs = Blog.objects.filter(author__user = request.user)

    context = {
        'blogs':blogs
    }
    return render(request, 'profile/my_blogs.html', context)

def update_blog(request, id):
    blog = Blog.objects.get(id = id)
    form = UpdateBlogForm(instance=blog)
    if request.method == 'POST':
        form = UpdateBlogForm(request.POST, request.FILES, instance=blog)
        if form.is_valid():
            form.save()
            return redirect('my_blogs') 
    context = {
        'form':form,
    }

    return render(request, 'profile/update_blog.html', context)

def delete_blog(request, id):
    blogs = Blog.objects.get(id = id).delete()
    return redirect('my_blogs')

def sending_mail(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        text = request.POST.get('text')
        send_mail('Blog saytidan xabar', message=text, recipient_list=[email], from_email=settings.EMAIL_HOST_USER)

        return redirect(request.META.get('HTTP_REFERER'))
    
    return render(request, 'mail.html')