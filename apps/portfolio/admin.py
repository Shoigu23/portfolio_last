from django.contrib import admin
from apps.portfolio.models import Project, Category, Skill, Message

# Register your models here.

admin.site.register(Project)
admin.site.register(Category)
admin.site.register(Skill)
admin.site.register(Message)
