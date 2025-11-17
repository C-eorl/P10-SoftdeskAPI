
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
