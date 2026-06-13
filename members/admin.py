# Register your models here.
from django.contrib import admin

from .models import Member


@admin.register(Member)
class MemberAdmin(admin.ModelAdmin):

    search_fields = (
        "name",
        "phone_number",
    )

    list_display = (
        "name",
        "phone_number",
        "created_at",
    )