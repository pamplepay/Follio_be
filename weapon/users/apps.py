from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class UsersConfig(AppConfig):
    name = "weapon.users"
    verbose_name = _("Users")

    def ready(self):
        try:
            import weapon.users.signals  # noqa F401
        except ImportError:
            pass
