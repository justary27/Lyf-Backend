from django.contrib import admin
from .models import LyfUser


@admin.register(LyfUser)
class LyfUserAdmin(admin.ModelAdmin):

    fields = [
        'id',
        'username',
        'password',
        'last_login',

        'start_date',
        
        'is_active',

        'is_superuser',
        
        'is_admin',
        'is_staff',
        'is_pro_user',
        'is_beta_tester',

        'groups',
        'user_permissions',
    ]

    readonly_fields = [
        'id',
        'start_date',
    ]

