from rest_framework import serializers
from exercises.models import Exercise
from .models import (
    TemplateExercise, WorkoutTemplate,
    WorkoutSession, WorkoutSet, PersonalRecord
)
from decimal import Decimal

class TemplateExerciseSerializer(serializers.ModelSerializer):
    exercise_name = serializers.CharField(source='exercise.name',
                                          read_only=True)
    class Meta:
        model = TemplateExercise
        fields = ('id', 'exercise', 'exercise_name', 'order')


class WorkoutTemplateSerializer(serializers.ModelSerializer):
    # вложенные упражнения, добавляются отдельным эндпоинтом
    exercises = TemplateExerciseSerializer(many=True,read_only=True)

    class Meta:
        model = WorkoutTemplate
        fields = ('id', 'name', 'created_at', 'exercises') 
        read_only_fields = ('created_at',)

class TemplateExerciseCreateSerializer(serializers.ModelSerializer):
    order = serializers.IntegerField(required=False, allow_null=True)

    class Meta:
        model = TemplateExercise
        fields = ('id', 'exercise', 'order')

    def validate_exercise(self, value):
        if not Exercise.objects.filter(id=value.id).exists():
            raise serializers.ValidationError('Упражнение не найдено')
        return value

    def create(self, validated_data):
        if validated_data.get('order') is None:
            template = validated_data['template']
            max_order = TemplateExercise.objects.filter(template=template).count()
            validated_data['order'] = max_order + 1
        return super().create(validated_data)

    
class WorkoutSetSerializer(serializers.ModelSerializer):
    exercise_name = serializers.CharField(source='exercise.name',
                                          read_only=True)
    estimated_1rm = serializers.DecimalField(max_digits=6, decimal_places=2, read_only=True)

    class Meta:
        model = WorkoutSet
        fields = ('id', 'exercise', 'exercise_name', 'weight', 'reps', 'estimated_1rm')

    def create(self, validated_data):
        session = validated_data['session']
        user = session.user
        exercise = validated_data['exercise']
        weight = validated_data['weight']
        reps = validated_data['reps']

        new_1rm = (Decimal(str(weight)) * (Decimal('1') + Decimal(str(reps)) / Decimal('30'))).quantize(Decimal('0.01'))

        workout_at = WorkoutSet.objects.create(
            session=session, exercise=exercise, weight=weight,
            reps=reps, estimated_1rm=new_1rm
        )

        is_pr = False
        pr, created = PersonalRecord.objects.get_or_create(
            user=user, exercise=exercise,
            defaults={'weight': weight, 'estimated_1rm': new_1rm}
        )
        if not created and new_1rm > pr.estimated_1rm:
            pr.weight = weight
            pr.estimated_1rm = new_1rm
            pr.save()
            is_pr = True
        elif created:
            is_pr = True

        return {'set': workout_at, 'is_pr': is_pr} 
    
    def to_representation(self, instance):
        """instance-словарь после create. приводи к нужному виду ответа"""
        if isinstance(instance, dict) and 'set' in instance:
            workout_set = instance['set']
            data = super().to_representation(workout_set)
            data['is_pr'] = instance['is_pr']
            return data
        return super().to_representation(instance)
    
class WorkoutSessionSerializer(serializers.ModelSerializer):
    sets = WorkoutSetSerializer(many=True, read_only=True)
    template_name = serializers.CharField(source='template.name',
                                          read_only=True, default=None)
    class Meta:
        model = WorkoutSession
        fields = ('id', 'name', 'template', 'template_name', 'date', 'sets')
        read_only_fields = ('date',)

class PersonalRecordSerializer(serializers.ModelSerializer):
      exercise_name = serializers.CharField(source='exercise.name',
                                          read_only=True)
      class Meta:
          model = PersonalRecord
          fields = ('id', 'exercise', 'exercise_name', 'weight', 
                    'estimated_1rm', 'achieved_at')      
    
