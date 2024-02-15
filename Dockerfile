# Dockerfile
FROM python:3.8

# 작업 디렉토리 설정
WORKDIR /app

# 의존성 파일 복사
COPY requirements.txt ./

# 의존성 설치
RUN pip install -r requirements.txt

# 프로젝트 파일 복사
COPY . .

# 포트 8000 열기
EXPOSE 8000

# Django 서버 실행
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
