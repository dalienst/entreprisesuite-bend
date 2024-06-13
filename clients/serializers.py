from rest_framework import serializers

from clients.models import Client
from contracts.serializers import ContractSerializer
from invoices.serializers import InvoiceSerializer


class ClientSerializer(serializers.ModelSerializer):
    name = serializers.CharField(max_length=255)
    email = serializers.EmailField()
    phone = serializers.CharField(max_length=15, required=False)
    user = serializers.CharField(read_only=True, source="user.username")
    contract = serializers.SerializerMethodField(read_only=True)
    invoice = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Client
        fields = (
            "id",
            "name",
            "email",
            "phone",
            "user",
            "slug",
            "created_at",
            "updated_at",
            "contract",
            "invoice",
        )

    def get_contract(self, obj):
        contract = obj.contract.all()
        serializer = ContractSerializer(contract, many=True)
        return serializer.data

    def get_invoice(self, obj):
        invoice = obj.invoice.all()
        serializer = InvoiceSerializer(invoice, many=True)
        return serializer.data
