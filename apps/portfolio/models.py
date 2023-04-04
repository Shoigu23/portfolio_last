from django.db import models

# Create your models here.
class Category(models.Model):
    title = models.CharField(max_length=255)

    def __str__(self) -> str:
        return self.title


class Project(models.Model):
    title = models.CharField(max_length=100, verbose_name='Название проекта')
    pre_description = models.ForeignKey(verbose_name= 'Категория',to=Category, on_delete=models.CASCADE)
    description = models.TextField(verbose_name='Описание')
    image = models.ImageField(verbose_name='Изображение')

    def __str__(self) -> str:
        return self.title
    
class Skill(models.Model):
    title = models.CharField(max_length=50)
    
    def __str__(self) -> str:
        return self.title

class Message(models.Model):
    name = models.CharField(max_length=100, verbose_name='Имя')
    email = models.EmailField(verbose_name='Почта')
    comments = models.TextField(verbose_name='Коментарии')

