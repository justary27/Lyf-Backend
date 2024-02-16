from rest_framework import serializers
from .models import DiaryEntry
from user.models import LyfUser


class DiaryEntrySerializer(serializers.ModelSerializer):
    created_by = serializers.CharField(required=True)

    def validate_created_by(self, value):
        if LyfUser.objects.check_if_user_exists(value):
            user = LyfUser.objects.get_user_by_id(value)

            return user
        else:
            raise serializers.ValidationError("User doesn't exist")

    class Meta:
        model = DiaryEntry

        fields = [
            'id',
            'title',
            'description',
            'is_private',
            'created_by',
            'created_on',
        ]

        read_only_fields = [
            'id',
            'created_by',
            'created_on',
        ]
