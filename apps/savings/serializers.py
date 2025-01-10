from rest_framework import serializers

from apps.savings.models import Saving, Goal


class GoalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Goal
        fields = [
            "id",
            "title",
            "target_date",
            "amount",
            "user",
            "description",
            "is_completed"
        ]
        read_only_fields = ["id", "user", "is_completed"]


class SavingReadSerializer(serializers.ModelSerializer):
    goal = GoalSerializer()

    class Meta:
        model = Saving
        fields = [
            "id",
            "operation_type",
            "user",
            "amount",
            "goal",
            "date",
            "description",
        ]
        read_only_fields = ["id", "user"]


class SavingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Saving
        fields = [
            "id",
            "operation_type",
            "user",
            "amount",
            "goal",
            "date",
            "description",
        ]
        read_only_fields = ["id", "user"]

    def to_representation(self, instance):
        return SavingReadSerializer(instance).data
