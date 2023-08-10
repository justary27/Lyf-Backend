from rest_framework import serializers
from .models import Todo
from user.models import LyfUser


class TodoSerializer(serializers.ModelSerializer):
    created_by = serializers.CharField(required=True)

    def validate_created_by(self, value):
        if LyfUser.objects.check_if_user_exists(value):
            user = LyfUser.objects.get_user_by_id(value)
            
            return user
        else:
            raise serializers.ValidationError("User doesn't exist")

    class Meta:
        model = Todo

        fields = [
            'id',
            'title',
            'description',
            'created_by',
            'created_on',
            'is_reminder_set',
            'reminder_at',
            'is_completed',
        ]

        read_only_fields = [
            'id',
            'created_by',
            'created_on',
        ]
