from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import Group
from .forms import UserCreationForm, UserChangeForm
from .models import User, AddressModel, RoleModel, RoleUserModel, CurrentAddressModel


class RoleUserInline(admin.TabularInline):
    model = RoleUserModel


class UserAdmin(BaseUserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm

    list_display = ['id', 'first_name', 'last_name', 'email', 'is_admin']
    list_filter = ['is_active']
    readonly_fields = ['last_login']

    fieldsets = (
        (None, {'fields': ('first_name', 'last_name', 'email', 'prefix_number', 'phone_number', 'trn_number', 'company_name',
                           'zoho_customer_id', 'password')}),
        ('Permissions', {'fields': ('is_active', 'is_admin', 'is_superuser',)}),
    )

    add_fieldsets = (
        (None, {'fields': ('first_name', 'last_name', 'email', 'prefix_number', 'phone_number', 'trn_number', 'company_name',
                           'zoho_customer_id', 'password')}),
    )

    search_fields = ['first_name', 'last_name', 'email', 'prefix_number', 'phone_number', 'trn_number', 'company_name',
                     'zoho_customer_id']
    ordering = ['first_name', 'last_name']

    filter_horizontal = ()

    inlines = (RoleUserInline,)


admin.site.register(User, UserAdmin)
admin.site.register(AddressModel)
admin.site.register(RoleModel)
admin.site.register(RoleUserModel)
admin.site.register(CurrentAddressModel)
admin.site.unregister(Group)
