from rest_framework import serializers
from django.contrib.auth import get_user_model

from clients.models import Client
from contracts.models import Contract
from payments.models import PaymentMethod
from milestones.serializers import MilestoneSerializer

User = get_user_model()


class ContractSerializer(serializers.ModelSerializer):
    name = serializers.CharField(max_length=255)
    introduction = serializers.CharField(max_length=10000)
    details = serializers.CharField(max_length=10000)
    scope = serializers.CharField(max_length=10000)
    services_provided = serializers.CharField(max_length=10000)
    compensation_terms = serializers.CharField(max_length=10000)
    termination_clause = serializers.CharField(max_length=10000)
    legal_relationship = serializers.CharField(max_length=10000)
    nda_clause = serializers.CharField(max_length=10000)
    start_date = serializers.DateField()
    end_date = serializers.DateField()
    status = serializers.CharField(max_length=50, default="pending")
    currency = serializers.CharField(max_length=15)
    client = serializers.SlugRelatedField(
        slug_field="slug", queryset=Client.objects.all()
    )
    user = serializers.CharField(read_only=True, source="user.username")
    payment_method = serializers.SlugRelatedField(
        slug_field="slug", queryset=PaymentMethod.objects.all()
    )
    milestones = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Contract
        fields = (
            "id",
            "name",
            "introduction",
            "details",
            "scope",
            "services_provided",
            "compensation_terms",
            "termination_clause",
            "legal_relationship",
            "nda_clause",
            "start_date",
            "end_date",
            "client",
            "currency",
            "user",
            "payment_method",
            "status",
            "slug",
            "created_at",
            "updated_at",
            "milestones",
        )

    def get_fields(self):
        fields = super().get_fields()
        user = self.context["request"].user

        # Filter queryset to the logged-in user's objects
        fields["client"].queryset = Client.objects.filter(user=user)
        fields["payment_method"].queryset = PaymentMethod.objects.filter(user=user)
        return fields

    def get_milestones(self, obj):
        milestones = obj.milestones.all()
        serializer = MilestoneSerializer(milestones, many=True)
        return serializer.data
