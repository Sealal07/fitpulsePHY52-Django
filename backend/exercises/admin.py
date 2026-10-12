from django.contrib import admin
from .models import MuscleGroup, Exercise

@admin.register(MuscleGroup)
class MuscleGroupAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)

@admin.register(Exercise)
class ExerciseAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'muscle_group')
    search_fields = ('name',)
    list_filter = ('muscle_group',)