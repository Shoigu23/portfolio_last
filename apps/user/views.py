from django.shortcuts import render, redirect
from apps.user.models import EmailVerification, User
from django.urls import reverse, reverse_lazy
from apps.user.forms import UserRegistrationForm, UserLoginForm, UserProfileForm, ProjectForm
from django.views.generic.edit import CreateView, UpdateView
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.contrib import auth, messages
from django.views.generic.base import TemplateView
from django.views.generic.edit import CreateView, UpdateView
from apps.portfolio.models import Message, Project
from django.core.mail import EmailMessage
from django.conf import settings
from django.template.loader import render_to_string


def registration(request):
    if request.method == 'POST':
        form = UserRegistrationForm(data = request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Вы успешно зарегестрировались на нашем сайте')
            return HttpResponseRedirect(reverse('login'))
    else:
        form = UserRegistrationForm()
    return render (request, 'registration.html', {'form':form})



def login(request):
    if request.method == 'POST':
        form = UserLoginForm(data = request.POST)
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            user = auth.authenticate(username = username, password = password)
            if user:
                auth.login(request, user)
                return render(request, 'index.html')
    else:
        form = UserLoginForm()
    return render(request, 'login.html', {'form':form})


def logout(request):
    auth.logout(request)

    return HttpResponseRedirect('/')

@login_required(login_url='login')
def profile(request):
    if request.method == 'POST':
        form = UserProfileForm(data=request.POST, instance = request.user, files = request.FILES)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('profile'))
        else:
            print(form.errors)
    else:
        form = UserProfileForm(instance = request.user)
    return render(request, 'profile.html', {'form':form})


class UserProfileView(UpdateView):
    model = User
    template_name = 'profile.html'
    success_url = reverse_lazy('main')
    form_class = UserProfileForm

    def get_context_data(self, **kwargs):
        context = super(UserProfileView, self).get_context_data()
        return context
    
class CreateView(CreateView):
    model = User
    template_name = 'registration.html'
    form_class = UserRegistrationForm
    success_url = reverse_lazy('login')

    def get_context_data(self, **kwargs):
        context = super(CreateView, self).get_context_data(**kwargs)
        return context

class EmailVerificationView(TemplateView):
    template_name = 'verification.html'

    def get(self, request, *args, **kwargs):
        code = kwargs['code']
        user = User.objects.get(email = kwargs['email'])
        email_verification = EmailVerification.objects.filter(user=user, code = code)
        if email_verification.exists():
            user.is_confirm_email = True
            user.save()
            return super(EmailVerificationView, self).get(request, *args, **kwargs)
        else:
            return HttpResponseRedirect('/')
        
def contact(request):
    return render(request, 'contact.html')


@login_required(login_url='main')
def message(request):
    return render(request, 'contact.html')

@login_required(login_url='main')
def sendEmail(request):
    if request.method == 'POST':
        template = render_to_string('email_template.html', {
            'name':request.POST['name'],
            'email':request.POST['email'],
            'subject':request.POST['subject'],
        })
        email = EmailMessage(
            request.POST['subject'],
            template,
            settings.EMAIL_HOST_USER,
            ['toichubaev3930@mail.ru']
        )
        email12 = Message()
        email12.name = request.POST['name']
        email12.email = request.POST['email']
        email12.comments = request.POST['subject']
        email12.save()
        email.fail_silently=False
        email.send()
        message = ('Вы успешно отправили сообщение')
        
    return render(request, 'contact.html', {'message': message})

def comment(request):
    comment = Message.objects.all()
    return render(request, 'index.html', {'comment': comment})


def create_project(request):
    if request.method == 'POST':
        forma = ProjectForm(request.POST)
        if forma.is_valid():
            forma.save()
            return redirect('main')
    else:
        forma = ProjectForm()
    return render(request, 'addproject.html', {'forma': forma})