from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand

from weapon.core.utils import send_sms

User = get_user_model()

# https://docs.djangoproject.com/en/1.9/howto/custom-management-commands/
class Command(BaseCommand):

    def handle(self, *args, **options):
        print("*** Start to create superuser(ROOT ADMIN).")
        send_sms(['01075481208'], '테스트', '테스트')
