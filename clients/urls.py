from django.urls import path

from clients.views import ClientListCreateView, ClientDetailView

urlpatterns = [
    path("", ClientListCreateView.as_view(), name="client-list"),
    path("<str:slug>/", ClientDetailView.as_view(), name="client-detail"),
]
