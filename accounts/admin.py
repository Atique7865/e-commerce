"""
accounts/admin.py
Admin configuration for user profiles.
"""
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from .models import UserProfile


class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    verbose_name_plural = 'Profile'
    fields = ('phone', 'company_name', 'address', 'bio', 'profile_image')


class UserAdmin(BaseUserAdmin):
    """Extend built-in UserAdmin to show profile inline."""
    inlines = (UserProfileInline,)
    list_display  = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'date_joined')
    list_filter   = ('is_staff', 'is_superuser', 'is_active')
    search_fields = ('username', 'email', 'first_name', 'last_name')


# Re-register User with the extended admin
admin.site.unregister(User)
admin.site.register(User, UserAdmin)


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display  = ('user', 'phone', 'company_name', 'created_at')
    search_fields = ('user__username', 'user__email', 'company_name')
    readonly_fields = ('created_at', 'updated_at')
