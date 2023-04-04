from django.urls import path
from apps.user.views import create_project, CreateView, registration, login, logout, UserProfileView, contact , EmailVerificationView, message ,sendEmail

urlpatterns = [
    path('registration/', CreateView.as_view(), name='registration'),
    path('verify/<str:email>/<uuid:code>', EmailVerificationView.as_view(), name='registration'),
    path('registration/', registration, name='verify'),
    path('login/', login, name='login'),
    path('profile/<int:pk>', UserProfileView.as_view(), name='profile'),
    path('logout/', logout, name='logout'),
    path('contact/', contact, name='contact'),
    path('sendemail/', sendEmail, name='sendemail'),
    path('message/', message, name='message'),
    path('create_project/', create_project, name='create_project'),
]