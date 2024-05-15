from django.contrib import admin
from django.contrib.auth.models import Group
from .models import User


class UserAdmin(admin.ModelAdmin):
    list_display = ('email', 'full_name', 'is_active', 'is_staff')
    list_filter = ('is_staff', 'role')
    ordering = ('email',)
    search_fields = ('email', 'full_name')


admin.site.register(User, UserAdmin)
admin.site.unregister(Group)