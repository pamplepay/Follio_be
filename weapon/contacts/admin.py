from django.contrib import admin

from weapon.contacts.models import Suggest


@admin.register(Suggest)
class SuggestAdmin(admin.ModelAdmin):
    raw_id_fields = ['user']
    list_display = ('id', 'title', 'user', 'content', 'created_at', 'updated_at')

