from django.utils.translation import gettext_lazy as _
from rest_framework import exceptions, status
from rest_framework_simplejwt.exceptions import TokenError, AuthenticationFailed


class TokenError(Exception):
    pass


class InvalidToken(AuthenticationFailed):
    status_code = status.HTTP_401_UNAUTHORIZED
    default_detail = _('Token is invalid or expired')
    default_code = 'token_not_valid'