from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand

from weapon.utils.cloud_messaging import make_message_all_platforms, send_cloud_push_message, webpush_message, subscribe_to_topic, \
    send_to_topic, send_to_token

User = get_user_model()

# https://docs.djangoproject.com/en/1.9/howto/custom-management-commands/
class Command(BaseCommand):

    def handle(self, *args, **options):
        # subscribe_to_topic('daily_post_push')
        message = make_message_all_platforms()
        # message = webpush_message()
        response = send_cloud_push_message(message)
        print(response)
        # send_to_topic()
        # send_to_token("eOirKoSKQf6CWQWm2qs7oa:APA91bGyGGxpKk2SgnLp5xKNeMxLhf0X-nhpF9sjBgcEoRgGShFUdui2hi0WmqFkPpbt9fAYNjiMJeUkQAIEriRUCFziupN1GyNaCnIXczfM26lCzSoiqSx8OdLLKQpzu2H2Rtl_LYM5")



