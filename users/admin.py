from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth import get_user_model

from .forms import CustomUserCreateForm, CustomUserChangeForm


User = get_user_model()

class CustomUserAdmin(UserAdmin):

    add_form = CustomUserCreateForm
    form = CustomUserChangeForm
    model = User
    list_display = ['email', 'name']
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal information', {'fields': ('name',)}),
        ('Permissions', {'fields': ('is_active', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'name', 'is_superuser'),
        }),
    )

    search_fields = ('name', 'email' )
    ordering = ('name',)

admin.site.register(User, CustomUserAdmin)
