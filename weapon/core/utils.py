import base64
import binascii
import hashlib
import datetime
import hmac
import math
import time

import requests
import json

from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils import timezone
from django.utils.html import strip_tags

from config.settings.base import SMS_SEND_NUMBER

appKey = "apUCapxwHPQFBcld"

ERROR_CODES = {
    # For Accounts
    100000: "유저를 찾을 수 없습니다.",
    100001: "인증코드가 잘못 되었습니다.",
    100002: "인증코드가 이미 발송 되었습니다.",
    100003: "이미 인증된 유저입니다.",
    100004: "The rate limit exceeds",
    100005: "인증하지 않은 번호입니다.",
    100006: "베타테스트가 이미 신청된 번호입니다.",
    100007: "권한이 없습니다.",
    100008: "토큰이 없습니다."
}


def make_error_message(error_code):
    return {
        "detail": ERROR_CODES.get(error_code),
        "code": error_code
    }


def make_kst(date_time):
    pass


def send_email(to, subject, template, value_dict):
    html_message = render_to_string(template, value_dict)
    plain_message = strip_tags(html_message)
    from_email = settings.DEFAULT_FROM_EMAIL
    send_mail(subject, plain_message, from_email, [to], html_message=html_message)


def send_sms(phone_number_list, mesg, title):
    url = f'https://api-sms.cloud.toast.com'
    type = 'sms'
    if len(mesg) > 45:
        type = 'mms'
    uri = f'/sms/v2.4/appKeys/{appKey}/sender/{type}'

    recipientList = []
    for phone_number in phone_number_list:
        recipientList.append({
            "recipientNo": phone_number,
        })
    data = {
        "body": mesg,
        "sendNo": SMS_SEND_NUMBER,
        "recipientList": recipientList
    }

    if type is 'mms' and title:
        data['title'] = title

    headers = {
        "Content-Type": "application/json",
        "charset": "utf-8",
    }

    response = requests.post(url + uri, json=data, headers=headers)
    print(response)


def ncp_v2_make_signature(uri, timestamp, access_key, secret_key):
    method = "POST"

    message = method + " " + uri + "\n" + timestamp + "\n" + access_key
    message = bytes(message, 'UTF-8')

    signingKey = base64.b64encode(hmac.new(secret_key, message, digestmod=hashlib.sha256).digest())
    return signingKey
