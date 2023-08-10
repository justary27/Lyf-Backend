from django.contrib import admin
from .models import DiaryEntry

# Register your models here.
@admin.register(DiaryEntry)
class DiaryEntryAdmin(admin.ModelAdmin):

    fields = [
        'id',
        'title',
        'description',
        'created_by',
        'created_on',
        'is_private',
    ]

    readonly_fields = [
        'id',
        'created_by',
        'created_on',
    ]
