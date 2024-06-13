from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from invoices.serializers import InvoiceSerializer, InvoiceItemSerializer
from invoices.models import Invoice, InvoiceItem


# invoices/views.py
class InvoiceListCreateView(generics.ListCreateAPIView):
    serializer_class = InvoiceSerializer
    queryset = Invoice.objects.all()
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Invoice.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class InvoiceDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = InvoiceSerializer
    queryset = Invoice.objects.all()
    permission_classes = [IsAuthenticated]
    lookup_field = "slug"

    def get_queryset(self):
        return Invoice.objects.filter(user=self.request.user)


class InvoiceItemListCreateView(generics.ListCreateAPIView):
    serializer_class = InvoiceItemSerializer
    queryset = InvoiceItem.objects.all()
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return InvoiceItem.objects.filter(invoice__user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class InvoiceItemDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = InvoiceItemSerializer
    queryset = InvoiceItem.objects.all()
    permission_classes = [IsAuthenticated]
    lookup_field = "slug"

    def get_queryset(self):
        return InvoiceItem.objects.filter(invoice__user=self.request.user)
