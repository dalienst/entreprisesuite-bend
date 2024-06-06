from rest_framework import serializers

from milestonetasks.models import MilestoneTask


class MilestoneTaskSerializer(serializers.ModelSerializer):
    name = serializers.CharField(max_length=1000)
    description = serializers.CharField(max_length=10000)
    due_date = serializers.DateField()
    status = serializers.CharField(max_length=50, default="pending")
    milestone = serializers.CharField(max_length=1000)
    file = serializers.FileField(required=False)
    user = serializers.CharField(read_only=True, source="user.username")

    class Meta:
        model = MilestoneTask
        fields = (
            "id",
            "name",
            "description",
            "due_date",
            "status",
            "milestone",
            "user",
            "file",
            "slug",
            "created_at",
            "updated_at",
        )
