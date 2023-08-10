from django.contrib import admin
from .models import Todo

# Register your models here.
@admin.register(Todo)
class TodoAdmin(admin.ModelAdmin):

    fields = [
        'id',
        'title',
        'description',
        'is_completed',
        'created_by',
        'created_on',
        'is_reminder_set',
        'reminder_at',

    ]

    readonly_fields = [
        'id',
        'created_by',
        'created_on',
    ]

