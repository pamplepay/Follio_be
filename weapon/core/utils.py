import base64
import binascii
import hashlib
import datetime
import hmac
import math
import time

import requests
import json
import fitz
from PIL import Image
import easyocr

from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils import timezone
from django.utils.html import strip_tags
import os
from django.core.files.storage import FileSystemStorage
import cv2
from matplotlib import pyplot as plt

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

# jhpark_20231221_S
# pdf 파일을 png 파일로 변경
def convert_pdf_to_png(pdf_path, zoom=2):
    # PDF 파일 열기
    current_path = os.getcwd()
    media_folder = os.path.join(current_path, 'weapon/media')

    # 'media' 폴더 내의 PDF 파일 경로
    pdf_filepath = os.path.join(media_folder, pdf_path)

    # PDF 파일 열기
    doc = fitz.open(pdf_filepath)

    # 각 페이지를 순회
    for page_number in range(len(doc)):
        page = doc.load_page(page_number)  # 페이지 로드

        # 변환할 이미지의 해상도를 설정합니다. zoom 값이 높을수록 이미지의 해상도가 높아집니다.
        mat = fitz.Matrix(zoom, zoom)

        # 페이지를 이미지로 렌더링
        pix = page.get_pixmap(matrix=mat)

        # 이미지 객체로 변환
        img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)

        # 확장자를 제거합니다
        base = os.path.splitext(pdf_filepath)[0]

        # "\\"를 "/"로 변경합니다
        base = base.replace("\\", "/")
        directory_path = os.path.dirname(pdf_filepath)

        # "media/" 이후의 문자열을 추출합니다
        media_index = base.find("media/") + len("media/")
        media_path = base[media_index:]

        # "_"를 기준으로 문자열을 분리하고 첫 번째 부분을 선택합니다
        base_name = media_path.split('_')[0]

        png_path = f"{directory_path}/{base_name}.png"  # 새 확장자로 파일 이름 생성
        fs = FileSystemStorage()
        if fs.exists(png_path):
            fs.delete(png_path)

        # 이미지 저장
        img.save(png_path)

    # PDF 파일 닫기
    doc.close()
    return(png_path)

def ocr_process(png_path):
    # 이미지 로드
    img = cv2.imread(png_path)

    # 이미지가 None인지 확인
    if img is not None:
        # 이미지가 제대로 로드되었다면, 이미지를 화면에 표시
        plt.imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
        plt.show()
    else:
        # 이미지 로드에 실패했다면, 오류 메시지 출력
        print("Failed to load the image. Please check the file path.")

    reader = easyocr.Reader(['ko', 'en'])  # 'ko'는 한국어를 의미함
    print(f"png_path : {os.path.exists(png_path)}")
    result = reader.readtext(png_path)
    print(result)
    return result
# jhpark_20231221_E
