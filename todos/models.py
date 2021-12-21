from django.db import models

# Create your models here.
class Todo(models.Model):
    content = models.TextField()
    is_complete = models.BooleanField(default=False)