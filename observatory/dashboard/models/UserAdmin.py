#custom user admin to make the pages usable
from django.contrib import admin

def make_inactive(modeladmin, request, queryset):
    queryset.update(is_active=False)
make_inactive.short_description = 'Make inactive'

class UserAdmin(admin.ModelAdmin):
    list_display    = ('username', 'first_name', 'last_name', 'is_active')
    list_filter     = ('is_active',)
    actions         = (make_inactive,)
