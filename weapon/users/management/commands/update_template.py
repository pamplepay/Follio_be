from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand

from weapon.insurances.models import CustomerInsurance

User = get_user_model()

# https://docs.djangoproject.com/en/1.9/howto/custom-management-commands/
class Command(BaseCommand):

    def handle(self, *args, **options):
        template_list = CustomerInsurance.objects.filter(customer__isnull=True)
        for template in template_list:
            template.is_template = True
            template.save()
        print(' done ')
