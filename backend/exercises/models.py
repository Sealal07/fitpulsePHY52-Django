from django.db import models

class MuscleGroup(models.Model):
    name = models.CharField(max_length=50, unique=True)
    
class Exercise(models.Model):
    name = models.CharField(max_length=100, unique=True)
    muscle_group = models.ForeignKey(MuscleGroup, on_delete=models.PROTECT)
    description = models.TextField(blank=True)