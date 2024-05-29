from rest_framework import serializers
from django.contrib.auth import get_user_model

from clients.models import Client
from contracts.models import Contract, ContractTemplate, Milestone, PaymentMethod

User = get_user_model()


class ContractTemplateSerializer(serializers.ModelSerializer):
    name = serializers.CharField(max_length=1000)
    introduction = serializers.CharField(max_length=10000)
    details = serializers.CharField(max_length=10000)
    service_provided = serializers.CharField(max_length=10000)
    termination_policy = serializers.CharField(max_length=10000)
    nda = serializers.CharField(max_length=10000)
    user = serializers.CharField(read_only=True, source="user.username")

    class Meta:
        model = ContractTemplate
        fields = (
            "id",
            "name",
            "introduction",
            "details",
            "service_provided",
            "termination_policy",
            "nda",
            "slug",
        )


class ContractSerializer(serializers.ModelSerializer):
    user = serializers.CharField(read_only=True, source="user.username")
    client = serializers.SlugRelatedField(
        queryset=Client.objects.all(), slug_field="slug"
    )
    template = serializers.SlugRelatedField(
        queryset=ContractTemplate.objects.all(), slug_field="slug"
    )
    project_scope = serializers.CharField(max_length=10000)
    services_provided = serializers.CharField(max_length=10000)
    start_date = serializers.DateField()
    end_date = serializers.DateField()
    legal_relationship = serializers.CharField(max_length=10000)
    compensation_terms = serializers.CharField(max_length=10000)
    termination_clause = serializers.CharField(max_length=10000)
    status = serializers.ChoiceField(choices=Contract.STATUS_CHOICES)

    class Meta:
        model = Contract
        fields = (
            "id",
            "user",
            "client",
            "template",
            "project_scope",
            "services_provided",
            "start_date",
            "end_date",
            "legal_relationship",
            "compensation_terms",
            "termination_clause",
            "status",
            "slug",
        )
