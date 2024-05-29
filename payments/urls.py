from django.urls import path

from payments.views import PaymentMethodListCreateView, PaymentMethodDetailView

urlpatterns = [
    path("", PaymentMethodListCreateView.as_view()),
    path("<str:slug>/", PaymentMethodDetailView.as_view()),
]
