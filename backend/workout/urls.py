from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_nested import routers

from .views import (
    WorkoutTemplateView, WorkSetViews, PersonalRecordViews,
    WorkoutSessionViews, TemplateExerciseViews
)

router = DefaultRouter()
router.register(r'templates', WorkoutTemplateView, basename='template')
router.register(r'sets', WorkSetViews, basename='sets')

urlpatterns = [
    path('', include(router.urls)),
    path('templates/<int:template_pk>/exercises',
         TemplateExerciseViews.as_view({'get': 'list', 'post': 'create'}),
        name='template-exercise-list'), 
    path('prs/', PersonalRecordViews.as_view({'get': 'list'}), name='prs-list'),
]