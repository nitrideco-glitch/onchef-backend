from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from django.core import exceptions
from .models import User

class UserRegistrationSerializer(serializers.ModelSerializer):
    """Serializer for user registration"""
    
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)
    
    class Meta:
        model = User
        fields = ['id', 'email', 'password', 'password2', 'first_name', 'last_name', 'age', 'nationality']
        extra_kwargs = {
            'email': {'required': True},
            'first_name': {'required': False},
            'last_name': {'required': False},
        }
    
    def validate(self, attrs):
        """Validate that passwords match"""
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})
        return attrs
    
    def create(self, validated_data):
        """Create and return a new user"""
        validated_data.pop('password2')
        user = User.objects.create_user(**validated_data)
        return user

class UserProfileSerializer(serializers.ModelSerializer):
    """Serializer for user profile retrieval and update"""
    
    full_name = serializers.SerializerMethodField()
    
    class Meta:
        model = User
        fields = ['id', 'email', 'first_name', 'last_name', 'full_name', 'age', 'nationality', 
                 'stellar_points', 'level', 'date_joined']
        read_only_fields = ['id', 'email', 'stellar_points', 'level', 'date_joined']
    
    def get_full_name(self, obj):
        """Get user's full name"""
        return obj.get_full_name()
    
    def update(self, instance, validated_data):
        """Update user profile with validation"""
        # Prevent updating sensitive fields
        validated_data.pop('stellar_points', None)
        validated_data.pop('level', None)
        validated_data.pop('email', None)
        
        return super().update(instance, validated_data)

class UserPublicSerializer(serializers.ModelSerializer):
    """Serializer for public user information"""
    
    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'level', 'stellar_points']
        read_only_fields = ['id', 'first_name', 'last_name', 'level', 'stellar_points']