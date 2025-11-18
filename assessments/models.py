from django.db import models
from django.contrib.auth.models import User
from users.models import ChildProfile
import uuid


class Assessment(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    age_min = models.IntegerField(null=True, blank=True)
    age_max = models.IntegerField(null=True, blank=True)
    language = models.CharField(max_length=10, default='en')
    time_limit = models.IntegerField(null=True, blank=True)
    adaptive = models.BooleanField(default=False)
    published = models.BooleanField(default=False)
    version = models.CharField(max_length=32, default='1.0')

    def __str__(self):
        return self.title


class Section(models.Model):
    assessment = models.ForeignKey(Assessment, on_delete=models.CASCADE, related_name='sections')
    title = models.CharField(max_length=255)
    order = models.IntegerField(default=0)


class Question(models.Model):
    TYPE_CHOICES = [('mcq', 'Multiple Choice'), ('text', 'Text')]
    section = models.ForeignKey(Section, on_delete=models.CASCADE, related_name='questions')
    text = models.TextField()
    type = models.CharField(max_length=32, choices=TYPE_CHOICES, default='mcq')
    options = models.JSONField(null=True, blank=True)
    media_url = models.CharField(max_length=512, blank=True)
    difficulty = models.FloatField(null=True, blank=True)
    time_limit = models.IntegerField(null=True, blank=True)
    order = models.IntegerField(default=0)


class Result(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    child = models.ForeignKey(ChildProfile, on_delete=models.CASCADE, related_name='results')
    assessment = models.ForeignKey(Assessment, on_delete=models.CASCADE)
    started_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    raw_scores = models.JSONField(null=True, blank=True)
    normalized_scores = models.JSONField(null=True, blank=True)
    recommendations = models.JSONField(null=True, blank=True)


class Response(models.Model):
    result = models.ForeignKey(Result, on_delete=models.CASCADE, related_name='responses')
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    answer = models.JSONField()
    correct = models.BooleanField(null=True)
    time_taken = models.IntegerField(null=True, blank=True)


class ScoringRule(models.Model):
    assessment = models.ForeignKey(Assessment, on_delete=models.CASCADE, related_name='scoring_rules')
    rule_definition = models.JSONField()
