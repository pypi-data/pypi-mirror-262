from django.contrib import admin

from .models import ResetButton


@admin.register(ResetButton)
class ResetButtonAdmin(admin.ModelAdmin):
    pass
