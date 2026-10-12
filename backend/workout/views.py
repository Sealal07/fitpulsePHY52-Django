from rest_framework import viewsets, status, generics 
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import action 

from .models import (
    WorkoutTemplate, TemplateExercise,
    WorkoutSession, WorkoutSet, PersonalRecord
)

from .serializers import (
    WorkoutTemplateSerializer, TemplateExerciseCreateSerializer,
    TemplateExerciseSerializer, WorkoutSessionSerializer,
    WorkoutSetSerializer, PersonalRecordSerializer
)

class WorkoutTemplateView(viewsets.ModelViewSet):
    """ CRUD api/templates/ """
    serializer_class = WorkoutTemplateSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return WorkoutTemplate.objects.filter(user=self.request.user)#
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    
class WorkSetViews(viewsets.ModelViewSet):
    """ CRUD api/sets/?session=<id>"""
    serializer_class = WorkoutSetSerializer
    permission_classes = (IsAuthenticated, )
    http_method_names = ['get', 'post', 'delete', 'options', 'head']

    def get_queryset(self):
        session_id = self.request.query_params.get('session')
        qs = WorkoutSet.objects.filter(session__user=self.request.user)#
        if session_id:
            qs = qs.filter(session_id=session_id)
        return qs
    

    def create(self, request, *args, **kwargs):
        """переопределяем create
        1) проверить что session принадлежит пользователю
        2) вернуть ответ {'set', 'is_pr'}"""

        session_id = request.data.get('session')
        if not session_id:
            return Response({'detail': 'session обязателен'},
                             status=status.HTTP_400_BAD_REQUEST)
        try:
            session = WorkoutSession.objects.filter(id=session_id,
                                                    user=request.user)
        except WorkoutSession.DoesNotExist:
            return Response({'detail': 'Сессия не найдена'},
                            status=status.HTTP_404_NOT_FOUND)
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        # подменяем сессию на валидный объект
        serializer.validated_data['session']=session
        result = serializer.save()
        return Response(serializer.to_representation(result),
                        status=status.HTTP_201_CREATED)
    
class PersonalRecordViews(viewsets.ModelViewSet):
    """ GET api/prs """
    serializer_class = PersonalRecordSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return PersonalRecord.objects.filter(user=self.request.user)
    
class TemplateExerciseViews(viewsets.ModelViewSet):
    """CRUD api/templates/<template_id>/exercises/"""
    permission_classes = (IsAuthenticated,)
    
    def get_serializer_class(self):
        if self.action == 'create':
            return TemplateExerciseCreateSerializer
        return TemplateExerciseSerializer
    
    def get_queryset(self):
        return TemplateExercise.objects.filter(
            template__id=self.kwargs['template_pk'],
            template__user=self.request.user
        )
    
    def perform_create(self, serializer):
        template = WorkoutTemplate.objects.get(
            id=self.kwargs['template_pk'],
            user=self.request.user
        )
        serializer.save(template=template)

class WorkoutSessionViews(viewsets.ModelViewSet):
    """CRUD api/sessions/ """
    serializer_class = WorkoutSessionSerializer
    permission_classes = (IsAuthenticated, )

    def get_queryset(self):
        return WorkoutSession.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)