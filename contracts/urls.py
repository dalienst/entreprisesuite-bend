from django.urls import path

from contracts.views import (
    ContractListCreateView,
    ContractDetailView,
)


urlpatterns = [
    path("", ContractListCreateView.as_view(), name="contract-list"),
    path("<str:slug>/", ContractDetailView.as_view(), name="contract-detail"),
]
