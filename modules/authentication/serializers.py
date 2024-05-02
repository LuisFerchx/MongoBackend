from rest_framework import serializers
from .models import User


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "first_name",
            "last_name",
            "email",
            "identification_card",
            "phone",
            "is_active",
            # "user_type",
            # "sucursal",
            # "menu_options",
            "is_superuser",
            # "password",
            # "password2",
            # "token",
            # "language",
        ]

    def create(self, validated_data):
        # user_type = validated_data['user_type']
        email = validated_data['email']

        if email and User.objects.filter(email=email).exists():
            raise serializers.ValidationError(
                {'email': 'Email addresses must be unique.'}
            )
        user = User(
            email=email,
            # user_type=user_type,
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            sucursal_id=validated_data['sucursal_id']
        )

        user.save()
        return user
