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

from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils import timezone
from django.utils.html import strip_tags
import os
from django.core.files.storage import FileSystemStorage
from matplotlib import pyplot as plt
import cv2
import numpy as np
#from paddleocr import PaddleOCR
import uuid
import environ
from pathlib import Path

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
def resize_png_image(file_path, zoom_factor=2):
    if file_path.endswith(".png"):
        try:
            current_path = os.getcwd()
            media_folder = os.path.join(current_path, 'weapon/media')

            # 'media' 폴더 내의 PDF 파일 경로
            img_filepath = os.path.join(media_folder, file_path)

            with Image.open(img_filepath) as img:
                new_img = img.resize([int(zoom_factor * size) for size in img.size])
                os.remove(img_filepath)
                new_img.save(img_filepath)
            
                return img_filepath
        except IOError:
            print(f"Cannot open or resize {img_filepath}")
    
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

# def ocr_process(png_path):
#     # 이미지 기울기 보정
#     image_path = png_path
#     corrected_image = correct_skew(image_path)

#     lstfilename = os.path.basename(image_path).split(".")
#     basedir = "./weapon/media"

#     # 보정된 이미지 저장 (OCR을 위해)
#     corrected_image_file = f'{lstfilename[0]}_corrected.{lstfilename[1]}'
#     corrected_image_path = os.path.join(basedir, corrected_image_file)
#     cv2.imwrite(corrected_image_path, corrected_image)

#     # OCR 처리
#     ocr_korean = PaddleOCR(lang='korean')
#     korean_results = ocr_korean.ocr(corrected_image_path)
#     with open('ocr_results.txt', 'w', encoding='utf-8') as file:
#         for korean_result in korean_results[0]:
#             for result in korean_result:
#                 # result 데이터를 문자열로 변환하여 파일에 씁니다.
#                 file.write(str(result) + '\n')

#     #print(korean_results)

#     # 결과 출력
#     print("Korean OCR Results:")
#     result = group_text_by_lines(korean_results)
#     return result
#     # jhpark_20231221_E

# def group_text_by_lines(ocr_results):
#     lines = {}
#     cnt = 0
#     for line in ocr_results[0]:
#         text = line[1][0]
#         bbox = line[0]
#         top_left = bbox[0]
#         y_coord = top_left[1]

#         if cnt == 4:
#             print(cnt)

#         # 같은 라인에 속하는지 확인
#         found_line = False
#         for existing_y in lines.keys():
#             if abs(y_coord - existing_y) <= 10:  # y 좌표가 5 이하 차이면 같은 라인으로 간주
#                 lines[existing_y].append((text, top_left[0]))
#                 found_line = True
#                 break
        
#         if not found_line:
#             lines[y_coord] = [(text, top_left[0])]
#         cnt = cnt + 1

#     # 각 라인을 x 좌표에 따라 정렬하여 결합
#     combined_lines = []
#     for y in sorted(lines.keys()):
#         line = sorted(lines[y], key=lambda x: x[1])
#         combined_text = ' '.join([text for text, _ in line])
#         combined_lines.append(combined_text)

#     return combined_lines

def correct_skew(image_path):
    # 이미지를 읽기
    image = cv2.imread(image_path)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    _, thresh = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY_INV)

    # 가장자리 검출
    edges = cv2.Canny(thresh, 50, 150, apertureSize=3)
    lines = cv2.HoughLinesP(edges, 1, np.pi/180, 100, minLineLength=100, maxLineGap=10)

    # 기울기 각도 계산
    angles = []
    for line in lines:
        x1, y1, x2, y2 = line[0]
        angle = np.arctan2(y2 - y1, x2 - x1) * 180. / np.pi
        angles.append(angle)

    # 평균 각도로 이미지 회전
    median_angle = np.median(angles)
    rotated = cv2.warpAffine(image, cv2.getRotationMatrix2D((gray.shape[1]//2, gray.shape[0]//2), median_angle, 1.0), (gray.shape[1], gray.shape[0]))

    # 회전된 이미지 반환
    return rotated

def get_filename_without_extension(file_path):
    # 파일명과 확장자를 분리
    file_name, _ = os.path.splitext(file_path)
    return file_name

# 이미지 기울기 보정
def ocr_process(image_path):
    ROOT_DIR = Path(__file__).resolve(strict=True).parent.parent.parent
    env = environ.Env()
    env.read_env(str(ROOT_DIR / ".env"))
    api_url = env.str("OCR_API_URL")
    secret_key = env.str("OCR_SECRET_KEY")

    base_name = os.path.basename(image_path)
    img_folder = os.path.join(ROOT_DIR, 'ocrdata/img')
    img_filename = os.path.join(img_folder, base_name)
    corrected_image = correct_skew(image_path)
    cv2.imwrite(img_filename, corrected_image)

    request_json = {
        'images': [
            {
                'format': 'png',
                'name': 'demo'
            }
        ],
        'requestId': str(uuid.uuid4()),
        'version': 'V2',
        'timestamp': int(round(time.time() * 1000))
    }

    payload = {'message': json.dumps(request_json).encode('UTF-8')}
    files = [
    ('file', open(img_filename,'rb'))
    ]
    headers = {
    'X-OCR-SECRET': secret_key
    }

    # OCR 요청 및 응답
    # 일단 막음. 완료되면 풀을 것 _S
    response = requests.request("POST", api_url, headers=headers, data=payload, files=files)
    utf8_val = response.text.encode('utf8')

    # JSON 데이터 파싱 및 파일 저장
    decoded_str = utf8_val.decode('utf8')
    json_data = json.loads(decoded_str)
    # with open('C:/work/follio/Follio_be/ocrdata/json/result1.json', 'w') as f:
    #     json.dump(json_data, f, indent=4)
    # 일단 막음. 완료되면 풀을 것 _E
    # 임시로 파일로 처리 나중에 막을 것 _S
    # with open('C:/work/follio/Follio_be/ocrdata/json/result1.json', 'r', encoding='utf-8') as file:
    #     json_data = json.load(file)
    # 임시로 파일로 처리 나중에 막을 것 _E

    line_by_line_text = organize_text_by_coordinates_to_list(json_data)
    return line_by_line_text

def are_close(y1, y2, threshold=8):
    return abs(y1 - y2) <= threshold

def organize_text_by_coordinates_to_list(data):
    lines = []
    line_dict = {}

    for image in data.get('images', []):
        for field in image.get('fields', []):
            # Extract the position and text
            position = field.get('boundingPoly', {}).get('vertices', [])
            if position:
                top_left = position[0]
                text = field.get('inferText', '')

                # Find a line with a close enough Y-coordinate or create a new line
                found_line = False
                for line_y in line_dict.keys():
                    if are_close(line_y, top_left.get('y', 0)):
                        line_dict[line_y].append((top_left.get('x', 0), text))
                        found_line = True
                        break
                
                if not found_line:
                    line_dict[top_left.get('y', 0)] = [(top_left.get('x', 0), text)]

    # Sort the lines by their Y-coordinate and texts within each line by their X-coordinate
    for line_y in sorted(line_dict.keys()):
        sorted_texts = sorted(line_dict[line_y], key=lambda x: x[0])  # Sort by X-coordinate
        lines.append(' '.join(text[1] for text in sorted_texts))

    return lines

