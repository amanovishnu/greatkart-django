from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Account

# Register your models here.

class AccountAdmin(UserAdmin):
    list_display = ['id','username', 'email', 'first_name', 'last_name', 'last_login',  'date_joined', 'is_superadmin', 'is_active']
    list_display_links = ['username', 'email']
    search_fields = ['username']
    ordering = ['-date_joined']
    readonly_fields = ['last_login', 'last_login', 'date_joined']

    # required fields because of custom user model
    filter_horizontal = []
    list_filter = []
    fieldsets  = []

admin.site.register(Account, AccountAdmin)
