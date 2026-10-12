from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .views import MuscleGroupViewSet, ExerciseViewSet

router = DefaultRouter()
router.register(r'muscle-groups', MuscleGroupViewSet, 
                basename='muscle-group')
router.register(r'exercises', ExerciseViewSet, 
                basename='exercise')

urlpatterns =[
    path('', include(router.urls)),
]