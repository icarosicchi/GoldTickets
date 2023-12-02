from django.db import models
from django.conf import settings
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse

class Category(models.Model):
    name = models.CharField(max_length=255)
    content = content = models.TextField()
    def __str__(self):
        return f'{self.name}'

class Event(models.Model):
    name = models.CharField(max_length=255, default="")
    description = models.TextField(default="")  
    location = models.CharField(max_length=255, default="")
    event_date = models.DateField(null=True, default="")
    creation_date = models.DateTimeField(default=timezone.now)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=None) 
    photo_url = models.URLField(max_length=200, null=True)
    author_id = models.IntegerField(default=1)
    categories = models.ManyToManyField(Category, related_name='events', blank=True)
    def __str__(self):
        return self.name
    def get_absolute_url(self):
        return reverse('detailView', args=[str(self.name)])

class Comment(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='comments', default=None)
    author = models.ForeignKey(User, on_delete=models.CASCADE, default=None)
    text = models.CharField(max_length=255)
    post_date = models.DateTimeField(default=timezone.now)
    def __str__(self):
        return f'{self.author.username} ({self.post_date})'
    
class Perfil(models.Model):
    user = models.OneToOneField(User,null=True,on_delete=models.CASCADE)
    bio = models.TextField()
    telefone = models.CharField(null=True, blank=True,max_length=11)
    whatsapp = models.CharField(null=True, blank=True,max_length=11)
    instagram = models.CharField(null=True, blank=True,max_length=25)