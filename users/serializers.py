from rest_framework import serializers
from django.contrib.auth import get_user_model
from rest_framework.validators import UniqueValidator
from rest_framework_simplejwt.tokens import RefreshToken, TokenError
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode

from users.validators import (
    validate_password_symbol,
    validate_password_uppercase,
    validate_password_lowercase,
    validate_password_digit,
)
from users.token import account_activation_token
from suite.settings.base import EMAIL_USER, DOMAIN
from contracts.serializers import ContractSerializer
from clients.serializers import ClientSerializer
from payments.serializers import PaymentMethodSerializer

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    """
    serializer for user
    - create user
    - fetch data related to user
    """

    username = serializers.CharField(
        max_length=20,
        min_length=4,
        validators=[UniqueValidator(queryset=User.objects.all())],
    )
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())],
    )
    first_name = serializers.CharField(max_length=255)
    last_name = serializers.CharField(max_length=255)
    password = serializers.CharField(
        max_length=128,
        min_length=5,
        write_only=True,
        validators=[
            validate_password_digit,
            validate_password_uppercase,
            validate_password_symbol,
            validate_password_lowercase,
        ],
    )
    contracts = serializers.SerializerMethodField(read_only=True)
    clients = serializers.SerializerMethodField(read_only=True)
    payment_methods = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = User
        fields = (
            "id",
            "username",
            "email",
            "first_name",
            "last_name",
            "password",
            "is_verified",
            "is_active",
            "is_staff",
            "is_superuser",
            "contracts",
            "clients",
            "payment_methods",
        )

    @staticmethod
    def send_activation_email(user, request):
        """
        send verification email
        """
        email_body = render_to_string(
            "email_verification.html",
            {
                "user": user,
                "domain": DOMAIN,
                "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                "token": account_activation_token.make_token(user),
            },
        )

        send_mail(
            "Activate your account",
            email_body,
            EMAIL_USER,
            [user.email],
            fail_silently=False,
        )

    def create(self, validated_data):
        request = self.context.get("request")
        user = User.objects.create_user(**validated_data)
        user.save()
        self.send_activation_email(user, request)
        return user

    def get_contracts(self, obj):
        contracts = obj.contracts.all()
        serializers = ContractSerializer(contracts, many=True)
        return serializers.data
    
    def get_clients(self, obj):
        clients = obj.clients.all()
        serializers = ClientSerializer(clients, many=True)
        return serializers.data
    
    def get_payment_methods(self, obj):
        payment_methods = obj.payment_methods.all()
        serializers = PaymentMethodSerializer(payment_methods, many=True)
        return serializers.data


class VerifyEmailSerializer(serializers.Serializer):
    uidb64 = serializers.CharField()
    token = serializers.CharField()

    class Meta:
        fields = ("uidb64", "token")

    def validate(self, data):
        user = None
        try:
            user_id = force_str(urlsafe_base64_decode(data.get("uidb64")))
            user = User.objects.get(id=user_id)

        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            raise serializers.ValidationError("Invalid user id", code="invalid_code")

        token = data.get("token")
        if user and not account_activation_token.check_token(user, token):
            raise serializers.ValidationError("Invalid token", code="invalid_token")

        return data

    def save(self, **kwargs):
        user_id = force_str(urlsafe_base64_decode(self.validated_data.get("uidb64")))
        user = User.objects.get(id=user_id)
        user.is_verified = True
        user.save()
        return user


class LogoutSerializer(serializers.Serializer):
    refresh = serializers.CharField()

    def validate(self, attrs):  # type:ignore[no-untyped-def]
        self.token = attrs["refresh"]
        return attrs

    def save(self, **kwargs):  # type:ignore[no-untyped-def]
        try:
            RefreshToken(self.token).blacklist()

        except TokenError:
            raise serializers.ValidationError(
                "Invalid or expired token", code="invalid_token"
            )
