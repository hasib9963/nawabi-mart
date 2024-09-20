from django.contrib import admin
from .models import Profile

# Registering the Profile model
@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'first_name', 'last_name', 'email', 'mobile', 'address')
    search_fields = ('user__username', 'first_name', 'last_name', 'email')

    # Optionally, customize how profiles appear and can be filtered
    list_filter = ('user__is_staff', 'user__is_active')
