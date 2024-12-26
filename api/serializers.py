from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import get_default_password_validators
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework_simplejwt.serializers import TokenObtainSerializer
from rest_framework_simplejwt.tokens import RefreshToken

UserModel = get_user_model()


def validate_password(password, user=None, password_validators=None):
    """
    Validate whether the password meets all validator requirements.

    If the password is valid, return ``None``.
    If the password is invalid, raise ValidationError with all error messages.
    """
    errors = []
    if password_validators is None:
        password_validators = get_default_password_validators()
    for validator in password_validators:
        try:
            validator.validate(password, user)
        except ValidationError as error:
            errors.append(error)
    if errors:
        raise ValidationError(errors)


class UserSignUpSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        required=True,
        error_messages={
            'invalid': 'Invalid credentials',
        }, validators=[validate_password]
    )
    confirm_password = serializers.CharField(
        required=True,
        error_messages={
            'invalid': 'Invalid credentials',
        }
    )

    class Meta:
        model = UserModel
        fields = ('username', 'email', 'password', 'confirm_password', 'first_name', 'last_name')


class UserResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserModel
        fields = ('username', 'email', 'first_name', 'last_name')


class TokenObtainPairSerializer(TokenObtainSerializer):
    @classmethod
    def get_token(cls, user):
        return RefreshToken.for_user(user), user

    def validate(self, attrs):
        data = super().validate(attrs)
        refresh, user = self.get_token(self.user)
        data['refresh'] = str(refresh)
        data['access'] = str(refresh.access_token)
        return data
