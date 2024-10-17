from django.db import models
from django.contrib.auth.models import User
from datetime import datetime
from django.contrib.auth.models import AbstractUser
from django.utils import timezone

# Create your models here.

class UserTextAssignment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    assigned_list = models.JSONField()  # Store the assigned list of text
    assigned_text = models.TextField(max_length=350)
    used = models.BooleanField(default=False)  # Track if the list has been used



# class Clues(models.Model):
#     location = models.CharField(max_length=30,null=True, blank=True)
#     clue = models.CharField(null=True, blank=True,max_length=30)
#     solved = models.BooleanField()


class Profile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,null=True)
    clue_solved = models.IntegerField(blank=True, default=0, null=True)
    
    # Add other fields as needed

class Finish(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    timeout = models.DateTimeField(blank=True, default=timezone.now, null=True) 
