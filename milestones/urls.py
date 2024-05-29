from django.urls import path

from milestones.views import MilestoneListCreateView, MilestoneDetailView


urlpatterns = [
    path("", MilestoneListCreateView.as_view(), name="milestone-list"),
    path("<str:slug>/", MilestoneDetailView.as_view(), name="milestone-detail"),
]
