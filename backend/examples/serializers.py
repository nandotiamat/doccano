from rest_framework import serializers

from .models import Comment, Example, ExampleState


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = (
            "id",
            "user",
            "username",
            "example",
            "text",
            "created_at",
        )
        read_only_fields = ("user", "example")


class ExampleSerializer(serializers.ModelSerializer):
    annotation_approver = serializers.SerializerMethodField()
    annotation_approver_role = serializers.SerializerMethodField()
    is_confirmed = serializers.SerializerMethodField()

    @classmethod
    def get_annotation_approver(cls, instance):
        approver = instance.annotations_approved_by
        return approver.username if approver else None

    @classmethod
    def get_annotation_approver_role(cls, instance):
        role = instance.annotations_approved_by_role
        return role.name if role else None

    def get_is_confirmed(self, instance):
        user = self.context.get("request").user
        if instance.project.collaborative_annotation:
            states = instance.states.all()
        else:
            states = instance.states.filter(confirmed_by_id=user.id)
        return states.count() > 0

    class Meta:
        model = Example
        fields = [
            "id",
            "filename",
            "meta",
            "annotation_approver",
            "annotation_approver_role",
            "comment_count",
            "text",
            "is_confirmed",
            "upload_name",
            "score",
        ]
        read_only_fields = ["filename", "is_confirmed", "upload_name"]


class ExampleStateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExampleState
        fields = ("id", "example", "confirmed_by", "confirmed_at")
        read_only_fields = ("id", "example", "confirmed_by", "confirmed_at")
