from django.urls import path
from apps.portfolio.views import MainListView, projects

urlpatterns = [
    path('', MainListView.as_view(), name='main'),
    path('project/', projects, name='projects')
]