from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import (
    WorkoutTemplateView, TemplateExerciseViews,
    WorkoutSessionViews, WorkSetViews,
    PersonalRecordViews,
)

router = DefaultRouter()
router.register(r'templates', WorkoutTemplateView, basename='template')
router.register(r'sessions', WorkoutSessionViews, basename='session')
router.register(r'sets', WorkSetViews, basename='set')

urlpatterns = [
    path('', include(router.urls)),
    path(
        'templates/<int:template_pk>/exercises/',
        TemplateExerciseViews.as_view({
            'get': 'list',
            'post': 'create'
        }),
        name='template-exercises-list'
    ),
    path(
        'templates/<int:template_pk>/exercises/<int:pk>/',
        TemplateExerciseViews.as_view({
            'get': 'retrieve',
            'put': 'update',
            'patch': 'partial_update',
            'delete': 'destroy'
        }),
        name='template-exercises-detail'
    ),
    path('prs/', PersonalRecordViews.as_view(), name='prs-list'),
]