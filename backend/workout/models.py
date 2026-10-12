from django.db import models
from django.contrib.auth.models import User
from exercises.models import Exercise


class WorkoutTemplate(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='templates')
    name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)


class TemplateExercise(models.Model):
    template = models.ForeignKey(WorkoutTemplate, on_delete=models.CASCADE, related_name='exercises')
    exercise = models.ForeignKey(Exercise, on_delete=models.PROTECT)
    order = models.PositiveSmallIntegerField()
    class Meta:
        ordering = ['order']


class WorkoutSession(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sessions')
    template = models.ForeignKey(WorkoutTemplate, null=True, blank=True, on_delete=models.SET_NULL)
    name = models.CharField(max_length=100)
    date = models.DateTimeField(auto_now_add=True)


class WorkoutSet(models.Model):
    session = models.ForeignKey(WorkoutSession, on_delete=models.CASCADE, related_name='sets')
    exercise = models.ForeignKey(Exercise, on_delete=models.PROTECT)
    weight = models.DecimalField(max_digits=6, decimal_places=2)
    reps = models.PositiveSmallIntegerField()
    estimated_1rm = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)


class PersonalRecord(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='prs')
    exercise = models.ForeignKey(Exercise, on_delete=models.CASCADE)
    weight = models.DecimalField(max_digits=6, decimal_places=2)
    estimated_1rm = models.DecimalField(max_digits=6, decimal_places=2)
    achieved_at = models.DateTimeField(auto_now=True)
    class Meta: 
        unique_together = [('user', 'exercise')]
