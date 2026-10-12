from django.contrib.auth.models import User
from rest_framework import serializers

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True,
                                     min_length=6)
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password')


    def validate_username(self, value):
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError('Уже существует')
        return value

    def create(self, validate_data):
        user = User.objects.create_user(
            username=validate_data['username'],
            email=validate_data['email'],
            password=validate_data['password']
        ) 
        return user 
    
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User 
        fields = ('id', 'username', 'email', 'date_joined')
        read_only_fields = fields 