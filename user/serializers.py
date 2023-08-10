from rest_framework import serializers

from .models import LyfUser

class LyfUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = LyfUser

        fields = [
            'id',
            'username',
            'start_date',
            'is_pro_user',
            'is_beta_tester',
            'is_staff',
            'is_admin',
            'is_active'
        ]

        read_only_fields = [
            'start_date',
        ]
