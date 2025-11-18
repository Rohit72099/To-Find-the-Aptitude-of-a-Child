from django.conf import settings
from django.db import models
from django.contrib.auth.models import User


class ParentProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='parent_profile')
    phone = models.CharField(max_length=32, blank=True)
    consent_given = models.BooleanField(default=False)
    consent_date = models.DateTimeField(null=True, blank=True)
    locale = models.CharField(max_length=10, default='en')

    def __str__(self):
        return f"ParentProfile({self.user.email})"


class ChildProfile(models.Model):
    parent = models.ForeignKey(ParentProfile, on_delete=models.CASCADE, related_name='children')
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100, blank=True)
    dob = models.DateField(null=True, blank=True)
    gender = models.CharField(max_length=16, blank=True)
    grade = models.CharField(max_length=16, blank=True)
    avatar_url = models.CharField(max_length=512, blank=True)
    notes = models.TextField(blank=True)

    def __str__(self):
        return f"Child({self.first_name} {self.last_name})"
