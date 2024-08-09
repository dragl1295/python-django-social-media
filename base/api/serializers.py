from rest_framework.serializers import ModelSerializer
from base.models import Room, User, Message
from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password



class RoomSerializer(ModelSerializer):
    class Meta:
        model = Room
        fields = '__all__'
        read_only_fields = ['host']
        
class MessageSerializer(ModelSerializer):
    class Meta:
        model = Message
        fields = '__all__'  
        read_only_fields = ['user', 'room']      
        
class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'
        
class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ('username', 'password', 'password2')

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})
        return attrs

    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data['username'],
        )
        
        user.set_password(validated_data['password'])
        user.save()

        return user                
