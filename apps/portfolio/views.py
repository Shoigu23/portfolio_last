from django.shortcuts import render
from apps.portfolio.models import Project, Category, Skill, Message
from django.views.generic.list import ListView
from django.core.cache import cache

# def comment(request):
#     comment = Message.objects.all()
#     return render(request, {'comment': comment})

class MainListView(ListView):
    model = Project
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super(MainListView,self).get_context_data(**kwargs)
        cache_category = cache.get('category')
        if not cache_category:
            category = Category.objects.all()
            cache.set('category', category, 10)
        else:
            category = cache_category
        skill = Skill.objects.all()
        project = Project.objects.all()
        comment = Message.objects.all()
        context['skill'] = skill
        context['category'] = category
        context['project'] = project
        context['comment'] = comment
        return context
    
def projects(request):
    projects = Project.objects.all()
    return render(request, 'addproject.html', {'projects':projects})