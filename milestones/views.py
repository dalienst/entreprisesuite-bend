from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from milestones.serializers import MilestoneSerializer
from milestones.models import Milestone


class MilestoneListCreateView(generics.ListCreateAPIView):
    serializer_class = MilestoneSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Milestone.objects.filter(user=user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class MilestoneDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = MilestoneSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = "slug"

    def get_queryset(self):
        user = self.request.user
        return Milestone.objects.filter(user=user)
