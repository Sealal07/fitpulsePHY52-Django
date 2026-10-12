from rest_framework import serializers
from .models import MuscleGroup, Exercise

class MuscleGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = MuscleGroup
        fields = ('id', 'name')

class ExerciseSerializer(serializers.ModelSerializer):
    muscle_group_name = serializers.CharField(source='muscle_group.name',
                                              read_only=True)
    muscle_group = serializers.PrimaryKeyRelatedField(queryset=MuscleGroup.objects.all())

    class Meta:
        model = Exercise
        fields = ('id', 'name', 'muscle_group', 
                  'muscle_group_name', 'description')