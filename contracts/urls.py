from django.urls import path

from contracts.views import (
    ContractListCreateView,
    ContractDetailView,
    PaymentMethodListCreateView,
    PaymentMethodDetailView,
)


urlpatterns = [
    path("", ContractListCreateView.as_view(), name="contract-list"),
    path("<str:slug>/", ContractDetailView.as_view(), name="contract-detail"),
    path(
        "payment-method/",
        PaymentMethodListCreateView.as_view(),
        name="payment-method-list",
    ),
    path(
        "payment-method/<str:slug>/",
        PaymentMethodDetailView.as_view(),
        name="payment-method-detail",
    ),
]
