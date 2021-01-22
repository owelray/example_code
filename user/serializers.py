from django.contrib.auth.hashers import make_password

from rest_framework import serializers

from .models import User
from .utils import validate_user_password


class UserSerializer(serializers.ModelSerializer):
    full_name = serializers.CharField(min_length=2, max_length=124)
    password = serializers.CharField(write_only=True, validators=[validate_user_password])
    role = serializers.SerializerMethodField()
    role_in_company = serializers.SerializerMethodField()
    number_of_employees = serializers.SerializerMethodField()
    business_area = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = [
            'id',
            'view_id',
            'email',
            'full_name',
            'phone',
            'password',
            'created',
            'role',
            'is_active',
            'role_in_company',
            'number_of_employees',
            'business_area'
        ]

    def get_role(self, obj):
        return obj.object_role

    def get_role_in_company(self, obj):
        return obj.object_role_in_company

    def get_number_of_employees(self, obj):
        return obj.object_number_of_employees
    
    def get_business_area(self, obj):
        return obj.object_business_area

class UserCreateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, validators=[validate_user_password])

    class Meta:
        model = User
        fields = [
            'id',
            'email',
            'full_name',
            'phone',
            'password',
            'role',
        ]

    @staticmethod
    def validate_password(value: str) -> str:
        return make_password(value)


class UserUpdateSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=False)

    class Meta:
        model = User
        fields = [
            'id',
            'email',
            'full_name',
            'phone',
            'role',
            'role_in_company',
            'number_of_employees',
            'business_area'
        ]


class ChangePasswordSerializer(serializers.ModelSerializer):
    old_password = serializers.CharField(write_only=True)
    new_password = serializers.CharField(write_only=True, validators=[validate_user_password])

    class Meta:
        model = User
        fields = (
            'old_password',
            'new_password',
        )
