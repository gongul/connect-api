from django.contrib import admin
from django.contrib.auth.admin import UserAdmin


from user.models import User

# Register your models here.


@admin.register(User)
class UserAdmin(UserAdmin):
    # The forms to add and change user instances
    # form = UserChangeForm

    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.
    list_display = ('email', 'name',
                    'is_active', 'is_superuser', 'registration_date')
    list_display_links = ('email',)
    list_filter = ('is_superuser', 'is_active')
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('name',)}),
        ('Permissions', {'fields': ('is_active', 'is_verified',
                                    'is_superuser', 'groups', 'user_permissions')}),
    )
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'name', 'password', 'password_confirmation')}
         ),
    )
    search_fields = ('email', 'name')
    ordering = ('-registration_date',)
    filter_horizontal = ('groups', 'user_permissions',)
