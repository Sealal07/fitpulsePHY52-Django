from rest_framework import generics, status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import RegisterSerializer, UserSerializer

class RegisterView(generics.CreateAPIView):
    """ POST /api/auth/register/"""
    serializer_class = RegisterSerializer
    permission_classes = (AllowAny,)

class MeView(generics.RetrieveAPIView):
    """ GET /api/me возвращает один объект"""
    serializer_class = UserSerializer
    permission_classes = (IsAuthenticated,)

    def get_object(self):
        return self.request.user 
    

class LogoutView(APIView):
    """ POST api/auth/logout/ """
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        return Response(status=status.HTTP_204_NO_CONTENT)
