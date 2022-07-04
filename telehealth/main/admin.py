"""Configuration of the admin interface for microblogs."""
from django.contrib import admin
from .models import *


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    """Configuration of the admin interface for users."""

    list_display = [
        'email', 'first_name', 'last_name', 'is_active',
    ]


@admin.register(Patient)
class PatientAdmin(UserAdmin):
    pass


@admin.register(Doctor)
class DoctorAdmin(UserAdmin):
    pass


@admin.register(Chat)
class ChatAdmin(UserAdmin):
    pass


@admin.register(Message)
class MessageAdmin(UserAdmin):
    pass
