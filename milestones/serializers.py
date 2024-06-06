from rest_framework import serializers

from milestones.models import Milestone
from contracts.models import Contract
from milestonetasks.serializers import MilestoneTaskSerializer


class MilestoneSerializer(serializers.ModelSerializer):
    name = serializers.CharField(max_length=1000)
    amount = serializers.DecimalField(max_digits=10, decimal_places=2)
    submission_deadline = serializers.DateField()
    contract = serializers.SlugRelatedField(
        slug_field="slug", queryset=Contract.objects.all()
    )
    user = serializers.CharField(read_only=True, source="user.username")
    status = serializers.CharField(max_length=50, default="pending")
    milestone_tasks = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Milestone
        fields = (
            "id",
            "name",
            "amount",
            "submission_deadline",
            "contract",
            "slug",
            "status",
            "user",
            "created_at",
            "updated_at",
            "milestone_tasks",
        )

    def get_milestone_tasks(self, obj):
        milestone_tasks = obj.milestone_tasks.all()
        serializer = MilestoneTaskSerializer(milestone_tasks, many=True)
        return serializer.data
