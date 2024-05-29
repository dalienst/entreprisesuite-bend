from rest_framework import serializers

from clients.models import Client


class ClientSerializer(serializers.ModelSerializer):
    name = serializers.CharField(max_length=255)
    email = serializers.EmailField()
    phone = serializers.CharField(max_length=15, blank=True, null=True)
    user = serializers.CharField(read_only=True, source="user.username")

    class Meta:
        model = Client
        fields = (
            "id",
            "name",
            "email",
            "phone",
            "user",
        )
