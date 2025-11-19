from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers

from authentication.models import CustomUser


class UserSerializer(serializers.ModelSerializer):
    age = serializers.SerializerMethodField()

    class Meta:
        model = CustomUser
        fields = [
            'id', 'username', 'email', 'first_name', 'last_name', 'date_of_birth',
            'age', 'can_be_contacted', 'can_data_be_shared', 'created_at'
        ]
        read_only_fields = ['id', 'age', 'created_at']

    def get_age(self, obj):
        return obj.age


class SignupSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True, required=True, validators=[validate_password]
    )

    class Meta:
        model = CustomUser
        fields = [
            'username', 'email', 'password', 'first_name', 'last_name', 'date_of_birth',
            'can_be_contacted', 'can_data_be_shared',
        ]

        extra_kwargs = {
            'username': {'required': True},
            'email': {'required': True},
            'date_of_birth': {'required': True},
        }

    def validate_email(self, value):
        if CustomUser.objects.filter(email=value).exists():
            raise serializers.ValidationError("L'adresse email est déjà utilisée")
        return value

    def create(self, validated_data):
        user = CustomUser.objects.create_user(**validated_data)
        return user