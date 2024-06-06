from django.urls import path

from milestonetasks.views import MilestoneTaskListCreateView, MilestoneTaskDetailView


urlpatterns = [
    path("", MilestoneTaskListCreateView.as_view(), name="milestonetask-list"),
    path("<str:slug>/", MilestoneTaskDetailView.as_view(), name="milestonetask-detail"),
]
