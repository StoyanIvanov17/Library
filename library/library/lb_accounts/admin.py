from django.contrib.auth import admin as auth_admin, get_user_model
from django.contrib import admin

from library.lb_accounts.forms import LibraryUserCreationForm, LibraryChangeForm

UserModel = get_user_model()


@admin.register(UserModel)
class LibraryUserAdmin(auth_admin.UserAdmin):
    model = UserModel
    add_form = LibraryUserCreationForm
    form = LibraryChangeForm

    list_display = ('pk', 'email', 'is_staff', 'is_superuser')
    search_fields = ('email',)
    ordering = ('pk',)

    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ()}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login',)}),
    )

    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("email", "password1", "password2"),
            },
        ),
    )
