from django.contrib.auth import get_user_model
from rest_framework import generics, status, serializers
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from django.utils import timezone

from users.serializers import (
    UserSerializer,
    LogoutSerializer,
    VerifyEmailSerializer,
)


User = get_user_model()


class UserRegisterView(APIView):
    """
    creating a user
    """

    def post(self, request):
        serializer = UserSerializer(data=request.data, context={"request": request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class UserListView(generics.ListAPIView):
    """
    list all users
    """

    serializer_class = UserSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        return User.objects.filter(is_active=True)
    


class UserDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    fetch user detail
    update detail
    delete account
    """

    serializer_class = UserSerializer
    permission_classes = [
        IsAuthenticated,
    ]
    lookup_field = "id"

    def get_queryset(self):
        return User.objects.filter(id=self.request.user.id)


"""Email Verification"""


class VerifyEmailView(GenericAPIView):
    serializer_class = VerifyEmailSerializer

    def patch(self, request, uidb64, token, **kwargs):
        data = {"uidb64": uidb64, "token": token}
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response(
            {
                "message": "Email verified successfully",
            },
            status=status.HTTP_200_OK,
        )


class LogoutView(GenericAPIView):
    """
    user logout view
    """

    serializer_class = LogoutSerializer

    permission_classes = (IsAuthenticated,)

    def post(self, request):  # type:ignore[no-untyped-def]
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(status=status.HTTP_204_NO_CONTENT)
