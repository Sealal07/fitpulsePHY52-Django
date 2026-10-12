from rest_framework import viewsets, filters
from rest_framework.permissions import IsAuthenticated 

from .models import MuscleGroup, Exercise
from .serializers import MuscleGroupSerializer, ExerciseSerializer


class MuscleGroupViewSet(viewsets.ModelViewSet):
    """ CRUD /api/muscle-groups Все операции с группами мышц"""

    queryset = MuscleGroup.objects.all()
    serializer_class = MuscleGroupSerializer
    permission_classes = (IsAuthenticated,)

class ExerciseViewSet(viewsets.ModelViewSet):
    """ CRUD /api/exercises/ фильтр ?muscle_group= """
    serializer_class = ExerciseSerializer
    permission_classes = (IsAuthenticated,)
    filter_backends = [filters.SearchFilter]
    search_field = ['name']

    def get_queryset(self):
        qs = Exercise.objects.select_related('muscle_group').all()
        muscle_group_id = self.request.query_params.get('muscle_group')
        if muscle_group_id:
            qs = qs.filter(muscle_group_id=muscle_group_id)
        search = self.request.query_params.get('search')
        if search:
            qs = qs.filter(name__icontains=search)
        return qs
    
    


