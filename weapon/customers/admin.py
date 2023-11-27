from django.contrib import admin

from weapon.customers.models import Customer


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    raw_id_fields = ['user']
    list_display = ('id', 'name', 'birth_day', 'created_at', 'updated_at')

