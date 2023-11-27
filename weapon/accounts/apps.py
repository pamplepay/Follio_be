from django.apps import AppConfig


class AccountsConfig(AppConfig):
    name = 'weapon.accounts'
    def ready(self):
        from .signals import create_user_profile
