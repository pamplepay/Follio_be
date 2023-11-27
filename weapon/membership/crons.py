import datetime

from django.http import JsonResponse
from django.conf import settings
from pytz import timezone

from .models import UserMembership
from ..accounts.models import PhoneNumber
# from ..alimtalk.alimtalk import make_alimtalk
from ..core.utils import send_email

UTC = timezone("UTC")

def check_membership_done(request):
    is_cron = request.headers.get("X-Appengine-Cron", False)

    if not settings.DEBUG and not is_cron:
        return JsonResponse({"status": "fail"})

    now = datetime.datetime.utcnow().astimezone(UTC)
    user_membership_list = UserMembership.objects.filter(expiry_at__lte=now, is_churned=False, is_send_done_message=False)

    for user_membership in user_membership_list:
        user_membership.is_send_done_message = True
        user = user_membership.user
        phone_number_instance = PhoneNumber.objects.filter(user=user).first()

        if phone_number_instance:
            phone_number = phone_number_instance.phone_number
            username = user.username
            item_name = user_membership.membership.name
            subject = f"[영어독립단어] {item_name}이 종료되었습니다. "

            mail_data = {
                "username": username,
                "item_name": item_name,
            }
            send_email(user.email, subject, "email/membership_done.html", mail_data)

            # 알림톡
            alimtalk_kwargs = {
                "username": username,
                "item_name": item_name,
            }

            # make_alimtalk(
            #     to=phone_number,
            #     template_code="INEN103",
            #     **alimtalk_kwargs
            # )

    UserMembership.objects.bulk_update(user_membership_list, ['is_send_done_message'])

    return JsonResponse({"status": "done"})
