from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Todo(models.Model):
    title=models.CharField(max_length=100)
    text=models.TextField(blank=True)
    created=models.DateTimeField(auto_now_add=True)
    data_completed = models.DateTimeField(blank=True,null=True)
    important = models.BooleanField(default=False)
    image = models.ImageField(null=True,blank=True)
    user=models.ForeignKey(User, on_delete=models.CASCADE)

    def __Str__(self):
        return f'{self.id}-{self.title}'