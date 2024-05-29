from rest_framework import serializers

from milestones.models import Milestone
from contracts.models import Contract


class MilestonSerializer(serializers.ModelSerializer):
    name = serializers.CharField(max_length=1000)
    amount = serializers.DecimalField(max_digits=10, decimal_places=2)
    submission_deadline = serializers.DateField()
    contract = serializers.SlugRelatedField(
        slug_field="slug", queryset=Contract.objects.all()
    )
    user = serializers.CharField(read_only=True, source="user.username")

    class Meta:
        model = Milestone
        fields = (
            "id",
            "name",
            "amount",
            "submission_deadline",
            "contract",
            "slug",
            "user",
            "created_at",
            "updated_at",
        )

    def get_fields(self):
        fields = super().get_fields()
        user = self.context["request"].user
        fields["contract"].queryset = Contract.objects.filter(user=user)
        return fields
