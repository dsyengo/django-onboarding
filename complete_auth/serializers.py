from django.contrib.auth.models import User
from rest_framework import serializers
from django.core.validators import validate_email

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)
    # Ensure email is required
    email = serializers.EmailField(required=True)

    class Meta:
        model = User
        fields = ('username', 'password', 'email', 'first_name', 'last_name')

    def validate_email(self, value):
        # Validate format
        validate_email(value)
        # Check existence and return specific message
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("A user with this email already exists. Please login.")
        return value

    def validate_username(self, value):
        # Check existence and return specific message
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError("This username is taken. Please try different username.")
        return value

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password'],
            email=validated_data.get('email'),
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', ''),
        )
        return user