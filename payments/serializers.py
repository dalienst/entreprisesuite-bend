from rest_framework import serializers
from django.contrib.auth import get_user_model

from payments.models import PaymentMethod

User = get_user_model()


class PaymentMethodSerializer(serializers.ModelSerializer):
    user = serializers.CharField(read_only=True, source="user.username")
    name = serializers.CharField(max_length=255)
    description = serializers.CharField(max_length=10000)

    class Meta:
        model = PaymentMethod
        fields = (
            "id",
            "user",
            "name",
            "description",
            "slug",
            "created_at",
            "updated_at",
        )
