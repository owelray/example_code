from django_filters import rest_framework as filter
from rest_framework.filters import OrderingFilter
from rest_framework import permissions, viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response

from core.pagination import CustomPagination
from core.permissions import IsAdminRole
from core.email_verification import sendConfirm

from apps.constants import USER_ROLE, MICROSERVICE_EMAIL, USER_ROLE_IN_COMPANY, NUMBER_OF_EMPLOYEES, BUSINESS_AREA

from .filters import UserFilter
from .models import User
from .serializers import (UserSerializer, UserUpdateSerializer, UserCreateSerializer, ChangePasswordSerializer)


class UserViewSet(viewsets.ModelViewSet):
    permission_classes = []
    queryset = User.objects.all()
    serializer_class = UserSerializer
    filter_backends = (filter.DjangoFilterBackend, OrderingFilter)
    filterset_class = UserFilter
    ordering_fields = ('view_id', 'full_name', 'email', 'phone', 'role', 'created')
    pagination_class = CustomPagination

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return UserCreateSerializer
        elif self.request.method == 'PUT':
            return UserUpdateSerializer
        return UserSerializer


    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        user = User.objects.filter(email=request.data['email'])
        if user:
            sendConfirm(user.first())
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def update(self, request, *args, **kwargs):
        result = super(UserViewSet, self).update(request, *args, **kwargs)
        result.data['role'] = self.instance.object_role
        result.data['role_in_company'] = self.instance.object_role_in_company
        result.data['number_of_employees'] = self.instance.object_number_of_employees
        result.data['business_area'] = self.instance.object_business_area
        return result

    def perform_update(self, serializer):
        self.instance = serializer.save()

    @action(detail=False, methods=['get'])
    def roles(self, request, *args, **kwargs):
        data = [
            {"id": num, "name": name}
            for num, name in USER_ROLE
        ]
        return Response(data)

    @action(detail=False, methods=['get'])
    def roles_in_company(self, request, *args, **kwargs):
        data = [
            {"id": num, "name": name}
            for num, name in USER_ROLE_IN_COMPANY
        ]
        return Response(data)

    @action(detail=False, methods=['get'])
    def number_of_employees(self, request, *args, **kwargs):
        data = [
            {"id": num, "name": name}
            for num, name in NUMBER_OF_EMPLOYEES
        ]
        return Response(data)

    @action(detail=False, methods=['get'])
    def business_areas(self, request, *args, **kwargs):
        data = [
            {"id": num, "name": name}
            for num, name in BUSINESS_AREA
        ]
        return Response(data)

    @action(detail=False, methods=['PUT'], permission_classes=[permissions.IsAuthenticated],
            serializer_class=ChangePasswordSerializer)
    def change_password(self, request):
        user = self.request.user
        serializer = ChangePasswordSerializer(data=request.data)

        if serializer.is_valid():
            # Check old password
            if not user.check_password(request.data.get("old_password")):
                response = {
                    "old_password": ['Wrong old password.']
                }
                return Response(response, status=status.HTTP_400_BAD_REQUEST)
            # set_password also hashes the password that the user will get
            user.set_password(request.data.get("new_password"))
            user.save()

            return Response("Password has been updated", status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['POST'], permission_classes=[permissions.IsAuthenticated, IsAdminRole])
    def reset_password(self, request):
        email = request.data.get('email')
        password = request.data.get('password')

        user = User.objects.get(email=email)
        user.set_password(password)
        user.save()

        return Response("OK!")
    @action(detail=False, methods=['POST'])
    def check_email(self, request):
        email = request.data.get('email')
        response = {}
        if User.objects.filter(email=email):
            response['message'] = {"detail": 'User with this email is already exist'}
            response['status_code'] = status.HTTP_400_BAD_REQUEST
            return Response(response, status=status.HTTP_400_BAD_REQUEST)
        return Response("OK", status=status.HTTP_200_OK)
