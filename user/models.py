from django.db import models
from django.contrib.auth.models import (AbstractBaseUser, BaseUserManager,
                                        PermissionsMixin)
from core.models import BaseModel
from .constants import *


class UserManager(BaseUserManager):
    def create_user(self, email=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return super().create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin, BaseModel):
    email = models.CharField(null=False, unique=True, max_length=225)
    full_name = models.CharField(max_length=286, default='User')
    phone = models.CharField(max_length=20, null=True, blank=True)
    view_id = models.PositiveIntegerField(default=1)
    role = models.PositiveSmallIntegerField(choices=USER_ROLE, default=USER_ROLE_USER)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(
        default=False,
        help_text='Designates whether the user can log into this admin site.'
    )
    facebook_user_id = models.PositiveBigIntegerField(null=True, blank=True, unique=True)
    """ Due to amount of big numbers we have to edit google_user_id to a charfield """
    google_user_id = models.CharField(null=True, blank=True, unique=True, max_length=100)
    role_in_company = models.PositiveSmallIntegerField(choices=USER_ROLE_IN_COMPANY,
                                                       null=True, blank=True)
    number_of_employees = models.PositiveSmallIntegerField(choices=NUMBER_OF_EMPLOYEES, null=True, blank=True)
    business_area = models.PositiveSmallIntegerField(choices=BUSINESS_AREA, null=True, blank=True)

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'

    objects = UserManager()
    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email

    @property
    def object_role(self):
        return self.get_choice_object(self.role, USER_ROLE)

    @property
    def object_role_in_company(self):
        return self.get_choice_object(self.role_in_company, USER_ROLE_IN_COMPANY)

    @property
    def object_number_of_employees(self):
        return self.get_choice_object(self.number_of_employees, NUMBER_OF_EMPLOYEES)

    @property
    def object_business_area(self):
        return self.get_choice_object(self.business_area, BUSINESS_AREA)

    def save(self, *args, **kwargs):

        if self._state.adding:
            last_id = User.objects.all().aggregate(largest=models.Max('view_id'))['largest']

            if last_id:
                self.view_id = last_id + 1

        super(User, self).save(*args, **kwargs)


class UserResetPassword(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    token = models.CharField(max_length=100, null=True, default=None)


class UserSocialHash(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    token = models.CharField(max_length=100, null=True, default=None)
