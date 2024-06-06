from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from milestonetasks.serializers import MilestoneTaskSerializer
from milestonetasks.models import MilestoneTask


class MilestoneTaskListCreateView(generics.ListCreateAPIView):
    serializer_class = MilestoneTaskSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return MilestoneTask.objects.filter(user=user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class MilestoneTaskDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = MilestoneTaskSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = "slug"

    def get_queryset(self):
        user = self.request.user
        return MilestoneTask.objects.filter(user=user)
