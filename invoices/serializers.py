from rest_framework import serializers

from invoices.models import Invoice, InvoiceItem
from clients.models import Client


class InvoiceItemSerializer(serializers.ModelSerializer):
    invoice = serializers.SlugRelatedField(
        slug_field="slug", queryset=Invoice.objects.all()
    )
    description = serializers.CharField(max_length=10000)
    quantity = serializers.IntegerField(default=1)
    unit_price = serializers.DecimalField(max_digits=10, decimal_places=2)
    user = serializers.CharField(read_only=True, source="user.username")

    class Meta:
        model = InvoiceItem
        fields = (
            "id",
            "invoice",
            "description",
            "quantity",
            "unit_price",
            "total_price",
            "item_slug",
            "user",
            "created_at",
            "updated_at",
        )


class InvoiceSerializer(serializers.ModelSerializer):
    client = serializers.SlugRelatedField(
        slug_field="slug", queryset=Client.objects.all()
    )
    user = serializers.CharField(read_only=True, source="user.username")
    title = serializers.CharField(max_length=255)
    issue_date = serializers.DateField()
    due_date = serializers.DateField()
    status = serializers.CharField(max_length=50, default="pending")
    items = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Invoice
        fields = (
            "id",
            "client",
            "user",
            "title",
            "issue_date",
            "due_date",
            "status",
            "total_amount",
            "items",
            "slug",
            "created_at",
            "updated_at",
        )

    def create(self, validated_data):
        # Remove items from validated_data if present, otherwise default to an empty list
        items_data = validated_data.pop("items", [])
        invoice = Invoice.objects.create(**validated_data)

        for item_data in items_data:
            InvoiceItem.objects.create(invoice=invoice, user=invoice.user, **item_data)

        invoice.update_total_amount()
        return invoice

    def get_items(self, obj):
        items = obj.items.all()
        serializer = InvoiceItemSerializer(items, many=True)
        return serializer.data

    def update(self, instance, validated_data):
        # Remove items from validated_data if present, otherwise default to an empty list
        items_data = validated_data.pop("items", None)

        instance.title = validated_data.get("title", instance.title)
        instance.issue_date = validated_data.get("issue_date", instance.issue_date)
        instance.due_date = validated_data.get("due_date", instance.due_date)
        instance.status = validated_data.get("status", instance.status)
        instance.save()

        if items_data is not None:
            # Delete existing items and recreate them only if 'items' is in the request
            instance.items.all().delete()
            for item_data in items_data:
                InvoiceItem.objects.create(
                    invoice=instance, user=instance.user, **item_data
                )

        instance.update_total_amount()
        return instance


class MinimalClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = (
            "id",
            "name",
            "email",
            "phone",
            "slug",
        )


class MimimalInvoiceSerializer(serializers.ModelSerializer):
    client = MinimalClientSerializer(read_only=True)
    items = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Invoice
        fields = (
            "id",
            "client",
            "title",
            "issue_date",
            "due_date",
            "status",
            "items",
            "slug",
            "total_amount",
            "created_at",
            "updated_at",
        )

    def get_items(self, obj):
        items = obj.items.all()
        serializer = InvoiceItemSerializer(items, many=True)
        return serializer.data
