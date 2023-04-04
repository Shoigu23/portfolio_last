from apps.user.models import User, EmailVerification
from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, UserChangeForm
from apps.user.tasks import send_verification_email
from django.utils import timezone
import uuid
from apps.portfolio.models import *
from datetime import timedelta

class UserRegistrationForm(UserCreationForm):
    first_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'Введите имя', 'class':'login-input' }))
    last_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'Введите фамилию', 'class':'login-input' }))
    username= forms.CharField(widget=forms.TextInput(attrs={'placeholder':'Имя пользователя', 'class':'login-input' }))
    email= forms.CharField(widget=forms.TextInput(attrs={'placeholder':'Введите электронную почту','class':'login-input', 'type':'email'}))
    password1= forms.CharField(widget=forms.TextInput(attrs={'placeholder':'Введите пароль', 'class':'login-input', 'type':'password'}))
    password2= forms.CharField(widget=forms.TextInput(attrs={'placeholder':'Потвердите пароль', 'class':'login-input', 'type':'password'}))
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'email', 'password1', 'password2')

    def save(self, commit=True):
        user = super(UserRegistrationForm, self).save(commit=True)
        expiration = timezone.now() + timedelta(hours=48)
        record = EmailVerification.objects.create(code=uuid.uuid4(), user=user, expiration=expiration)
        record.send_verification_email()
        # send_verification_email.delay(user.id)
        return user

class UserLoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'Имя пользователя', 'class':'login-input' }))
    password = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'Введите пароль', 'class':'login-input', 'type':'password'}))
    class Meta:
        model = User
        fields = ('username', 'password')

class UserProfileForm(UserChangeForm):
    first_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Введите имя', 'style': 'margin-left: 70px; font-size: 20px; margin-bottom: 10px; color: black'}))
    last_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Введите фамилию', 'style': 'font-size: 20px; margin-bottom: 10px; color: black'}))
    image = forms.ImageField(widget=forms.FileInput(attrs={'class': 'form-control', 'style': 'margin-left: 58px; font-size: 20px; margin-bottom: 10px; color: black'}), required=False)
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Введите имя пользователя', 'readonly':True, 'style': 'margin-left: 15px; font-size: 20px; margin-bottom: 10px; color: black'}))
    email = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'type': 'email', 'placeholder': 'Введите Email', 'readonly':True, 'style': 'margin-left: 58px; font-size: 20px; margin-bottom: 10px; color: black'}))
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'image', 'username', 'email',]


class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['title', 'image', 'description', 'pre_description',]