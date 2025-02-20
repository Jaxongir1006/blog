from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django import forms
from .models import Profile
from .models import Blog

class RegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class LoginForm(forms.Form):
    username = forms.CharField(max_length=160)
    password = forms.CharField(max_length=20)

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['age', 'bio', 'image', 'phone']

class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name']

class CreateBlogForm(forms.ModelForm):
    class Meta:
        model = Blog
        fields = "__all__"

class UpdateBlogForm(forms.ModelForm):
    class Meta:
        model = Blog
        fields = "__all__"